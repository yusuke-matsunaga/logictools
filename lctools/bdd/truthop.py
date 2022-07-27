#! /usr/bin/env python3

"""truth 形式の文字列から Bdd を作るためのクラス

:file: truthop.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from lctools.bdd.bddedge import BddEdge


class TruthOp:

    def __init__(self, mgr):
        self._mgr = mgr
        self._table = {}

    def op_step(self, truth_str, index):
        if truth_str == "0":
            return BddEdge.zero()
        if truth_str == "1":
            return BddEdge.one()
        if truth_str in self._table:
            return self._table[truth_str]

        n = len(truth_str)
        nh = n // 2
        truth_str1 = truth_str[:nh]
        truth_str0 = truth_str[nh:]
        e0 = self.op_step(truth_str0, index + 1)
        e1 = self.op_step(truth_str1, index + 1)
        r = self._mgr.new_node(index, e0, e1)
        self._table[truth_str] = r
        return r
