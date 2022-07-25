#! /usr/bin/env python3

"""Bdd の実装ファイル

:file: bdd.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""


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

    def is_valid(self):
        return not is_invalid()
    
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
        return index, edge0, edge1
