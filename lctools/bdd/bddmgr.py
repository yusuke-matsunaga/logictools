#! /usr/bin/env python3

"""BddMgr の実装ファイル

:file: bddmgr.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""
from lctools.bdd.bdd import Bdd
from lctools.bdd.bddedge import BddEdge
from lctools.bdd.bddnode import BddNode
from lctools.bdd.truthop import TruthOp
from lctools.bdd.copyop import CopyOp


class BddMgr:

    def __init__(self):
        self._node_count = 0
        self._node_table = {}
        self._and_table = {}
        self._or_table = {}
        self._xor_table = {}

    def copy(self, src):
        """BDDをコピーする．

        :param Bdd src: コピー元のBDD
        """
        if src._mgr != self:
            edge = self.copy_step(src._root)
        else:
            edge = src._root
        return Bdd(self, edge)

    def and_op(self, left, right):
        """AND演算を行う．
        """
        if self != left._mgr:
            ledge = self.copy_step(left._root)
        else:
            ledge = left._root
        if self != right._mgr:
            redge = self.copy_step(right._root)
        else:
            redge = right._root
        self._and_table = {}
        edge = self.and_step(ledge, redge)
        return Bdd(self, edge)

    def or_op(self, left, right):
        """OR演算を行う．
        """
        if self != left._mgr:
            ledge = self.copy_step(left._root)
        else:
            ledge = left._root
        if self != right._mgr:
            redge = self.copy_step(right._root)
        else:
            redge = right._root
        self._or_table = {}
        edge = self.or_step(ledge, redge)
        return Bdd(self, edge)

    def xor_op(self, left, right):
        """XOR演算を行う．
        """
        if self != left._mgr:
            ledge = self.copy_step(left._root)
        else:
            ledge = left._root
        if self != right._mgr:
            redge = self.copy_step(right._root)
        else:
            redge = right._root
        self._xor_table = {}
        edge = self.xor_step(ledge, redge)
        return Bdd(self, edge)
    
    def zero(self):
        """恒偽関数を作る．
        """
        return Bdd(self, BddEdge.zero())

    def one(self):
        """恒真関数を作る．
        """
        return Bdd(self, BddEdge.one())

    def literal(self, var, inv=False):
        """リテラル関数を作る．
        :param int var: 変数番号
        :param bool inv: 反転フラグ
        """
        edge = self.new_node(var, BddEdge.zero(), BddEdge.one())
        assert isinstance(edge, BddEdge)
        return Bdd(self, edge * inv)

    def posi_literal(self, var):
        """肯定のリテラル関数を作る．
        :param int var: 変数番号
        """
        edge = self.new_node(var, BddEdge.zero(), BddEdge.one())
        return Bdd(self, edge)

    def nega_literal(self, var):
        """否定のリテラル関数を作る．
        :param int var: 変数番号
        """
        edge = self.new_node(var, BddEdge.zero(), BddEdge.one())
        return Bdd(self, edge * True)

    def from_truth(self, truth_str):
        """真理値表形式の文字列からBDDを作る．
        :param str truth_str: 真理値表形式の文字列
        """
        # 文字列の長さが正しいかチェックする．
        n = len(truth_str)
        ni = 0
        while (1 << ni) < n:
            ni += 1
        assert (1 << ni) == n
        op = TruthOp(self)
        edge = op.op_step(truth_str, 0)
        return Bdd(self, edge)

    @property
    def node_num(self):
        """ノード数を返す．
        """
        pass

    def copy_step(self, edge):
        """コピーする
        """
        op = CopyOp(self)
        return op.op_step(edge)

    def and_step(self, left, right):
        """ANDを計算する．
        """

        if left.is_zero():
            return BddEdge.zero()
        if right.is_zero():
            return BddEdge.zero()
        if left.is_one():
            return right
        if right.is_one():
            return left
        if left == right:
            return left
        if left.node == right.node:
            # ということは極性違い
            return BddEdge.zero()
        key = left, right
        if key in self._and_table:
            return self._and_table[key]
        top, l0, l1, r0, r1 = BddMgr.decomp(left, right)
        e0 = self.and_step(l0, r0)
        e1 = self.and_step(l1, r1)
        result = self.new_node(top, e0, e1)
        self._and_table[key] = result
        return result

    def or_step(self, left, right):
        """ORを計算する．
        """

        if left.is_one():
            return BddEdge.one()
        if right.is_one():
            return BddEdge.one()
        if left.is_zero():
            return right
        if right.is_zero():
            return left
        if left == right:
            return left
        if left.node == right.node:
            # ということは極性違い
            return BddEdge.one()
        key = left, right
        if key in self._or_table:
            return self._or_table[key]
        top, l0, l1, r0, r1 = BddMgr.decomp(left, right)
        e0 = self.or_step(l0, r0)
        e1 = self.or_step(l1, r1)
        result = self.new_node(top, e0, e1)
        self._or_table[key] = result
        return result

    def xor_step(self, left, right):
        """XORを計算する．
        """

        if left.is_one():
            return ~right
        if right.is_one():
            return ~left
        if left.is_zero():
            return right
        if right.is_zero():
            return left
        if left == right:
            return BddEdge.zero()
        if left.node == right.node:
            # ということは極性違い
            return BddEdge.one()
        key = left, right
        if key in self._xor_table:
            return self._xor_table[key]
        top, l0, l1, r0, r1 = BddMgr.decomp(left, right)
        e0 = self.xor_step(l0, r0)
        e1 = self.xor_step(l1, r1)
        result = self.new_node(top, e0, e1)
        self._xor_table[key] = result
        return result
    
    def new_node(self, index, edge0, edge1):
        """ノードを生成する
        """
        if edge0 == edge1:
            return edge0
        # 極性を正規化する．
        oinv = edge0.inv
        edge0 *= oinv
        edge1 *= oinv

        # ノードテーブルを探す．
        key = (index, edge0, edge1)
        if key in self._node_table:
            return BddEdge(self._node_table[key], oinv)
        # なかったので作る．
        id = self._node_count
        self._node_count += 1
        node = BddNode(id, index, edge0, edge1)
        self._node_table[key] = node
        return BddEdge(node, oinv)

    @staticmethod
    def decomp(left, right):
        """最上位の変数で分解する
        """
        assert not left.is_const()
        assert not right.is_const()

        lnode = left.node
        lindex = lnode.index
        linv = left.inv
        rnode = right.node
        rindex = rnode.index
        rinv = right.inv
        top = min(lindex, rindex)
        if top == lindex:
            l0 = lnode.edge0 * linv
            l1 = lnode.edge1 * linv
        else:
            l0 = l1 = left
        if top == rindex:
            r0 = rnode.edge0 * rinv
            r1 = rnode.edge1 * rinv
        else:
            r0 = r1 = right
        return top, l0, l1, r0, r1

