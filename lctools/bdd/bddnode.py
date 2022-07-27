#! /usr/bin/env python3

"""BDDのノードを表すクラス

:file: bddnode.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""


class BddNode:

    def __init__(self, id, index, edge0, edge1):
        self._id = id
        self._index = index
        self._edge0 = edge0
        self._edge1 = edge1

    @property
    def id(self):
        return self._id
    
    @property
    def index(self):
        return self._index

    @property
    def edge0(self):
        return self._edge0

    @property
    def edge1(self):
        return self._edge1
