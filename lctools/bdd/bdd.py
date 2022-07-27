#! /usr/bin/env python3

"""Bdd の実装ファイル

:file: bdd.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from lctools.bdd.dispop import DispOp
from lctools.bdd.dotgen import DotGen


class Bdd:

    def __init__(self, mgr, root):
        self._mgr = mgr
        self._root = root

    @staticmethod
    def invalid():
        """不正値を返す．
        """
        return Bdd(None, None)

    def __invert__(self):
        """否定する．
        """
        return Bdd(self._mgr, ~self._root)

    def __and__(self, other):
        """論理積を返す．
        """
        if not isinstance(other, Bdd):
            raise NotImplementedError
        return self._mgr.and_op(self, other)

    def __iand__(self, other):
        """論理積計算して代入する．
        """
        if not isinstance(other, Bdd):
            raise NotImplementedError
        rbdd = self._mgr.and_op(self, other)
        self._root = rbdd._root
        return self

    def __or__(self, other):
        """論理積を返す．
        """
        if not isinstance(other, Bdd):
            raise NotImplementedError
        return self._mgr.or_op(self, other)

    def __ior__(self, other):
        """論理積計算して代入する．
        """
        if not isinstance(other, Bdd):
            raise NotImplementedError
        rbdd = self._mgr.or_op(self, other)
        self._root = rbdd._root
        return self

    def __xor__(self, other):
        """排他的論理積を返す．
        """
        if not isinstance(other, Bdd):
            raise NotImplementedError
        return self._mgr.xor_op(self, other)

    def __ixor__(self, other):
        """排他的論理積計算して代入する．
        """
        if not isinstance(other, Bdd):
            raise NotImplementedError
        rbdd = self._mgr.xor_op(self, other)
        self._root = rbdd._root
        return self

    def __eq__(self, other):
        """等価比較を行う．
        """
        if not isinstance(other, Bdd):
            raise NotImplementedError
        return self._mgr == other._mgr and self._root == other._root
    
    def is_valid(self):
        return not self.is_invalid()
    
    def is_invalid(self):
        return self._mgr is None
    
    def is_zero(self):
        if self.is_invalid():
            return False
        return self._root.is_zero()
    
    def is_one(self):
        if self.is_invalid():
            return False
        return self._root.is_one()
    
    def is_const(self):
        if self.is_invalid():
            return False
        return self._root.is_const()
    
    def root_decomp(self):
        if self.is_invalid():
            return None, None, None
        if self.is_const():
            return None, None, None
        node = self._root.node
        inv = self._root.inv
        edge0 = node.edge0 * inv
        edge1 = node.edge1 * inv
        index = node.index
        bdd0 = Bdd(self._mgr, edge0)
        bdd1 = Bdd(self._mgr, edge1)
        return index, bdd0, bdd1

    def display(self, *, fout=None):
        if self._mgr is None:
            fout.write("--invalid--\n")
        else:
            op = DispOp(fout=fout)
            op.display(self._root)

    def gen_dot(self, *, attr_dict={}, fout=None):
        if self._mgr is None:
            return

        gen = DotGen(attr_dict=attr_dict, fout=fout)
        gen.write(self._root)
