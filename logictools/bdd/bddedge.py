#! /usr/bin/env python3

"""BddEdge の実装ファイル

:file: bddedge.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from logictools.bdd.bddnode import BddNode


class BddEdge:
    """Bdd のノードを指す枝を表すクラス

    通常はただのノードを指すポインタだが，
    反転属性を持つ．
    """

    def __init__(self, node, inv=False):
        assert node is None or isinstance(node, BddNode)
        self._node = node
        self._inv = inv

    @staticmethod
    def zero():
        """定数0を表す枝を返す．
        """
        return BddEdge(None, False)

    @staticmethod
    def one():
        """定数1を表す枝を返す．
        """
        return BddEdge(None, True)

    def is_zero(self):
        """定数0の時 True を返す．
        """
        return self.is_const() and not self._inv

    def is_one(self):
        """定数1の時 True を返す．
        """
        return self.is_const() and self._inv

    def is_const(self):
        """定数の時 True を返す．
        """
        return self._node is None

    @property
    def node(self):
        """ノードを取り出す．
        """
        return self._node

    @property
    def inv(self):
        """極性を取り出す．
        """
        return self._inv

    def __invert__(self):
        """反転させる．
        """
        return BddEdge(self._node, not self._inv)

    def posi_edge(self):
        """正極性の枝を返す．
        """
        return BddEdge(self._node, False)

    def nega_edge(self):
        """負極性の枝を返す．
        """
        return BddEdge(self._node, True)

    def make_positive(self):
        """自身を正極性にする．
        """
        self._inv = False

    def make_negative(self):
        """自身を負極性にする．
        """
        self._inv = True

    def __mul__(self, other):
        """極性をかけ合わせる
        """
        if not isinstance(other, bool):
            raise NotImplementedError
        return BddEdge(self._node, self._inv ^ other)

    def __imul__(self, other):
        """極性をかけ合わせて代入する．
        """
        if not isinstance(other, bool):
            raise NotImplementedError
        self._inv ^= other
        return self

    def __hash__(self):
        """ハッシュ関数
        """
        if self._node is None:
            return int(self._inv)
        return self._node.id * 2 + int(self._inv)
        
    def __eq__(self, other):
        """等価比較演算
        """
        if not isinstance(other, BddEdge):
            raise NotImplementedError
        return self._node == other._node and self._inv == other._inv
