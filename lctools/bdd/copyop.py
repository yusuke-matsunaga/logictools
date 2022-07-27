#! /usr/bin/env python3

"""コピーを行うクラス

:file: copyop.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from lctools.bdd.bddedge import BddEdge


class CopyOp:

    def __init__(self, mgr):
        self._mgr = mgr
        self._table = {}

    def op_step(self, edge):
        if edge.is_const():
            # 定数ならそのまま返す．
            return edge
        if edge in self._table:
            return self._table[edge]
        node = edge.node
        inv = edge.inv
        index = node.index
        edge0 = self.op_step(node.edge0)
        edge1 = self.op_step(node.edge1)
        result = self._mgr.new_node(index, edge0, edge1)
        result *= inv
        self._table[edge] = result
        return result
        
