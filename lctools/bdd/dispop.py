#! /usr/bin/env python3

"""Bdd の内容を出力するクラス

:file: dispop.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

import sys
from lctools.bdd.bddedge import BddEdge
from lctools.bdd.nodecollector import NodeCollector


class DispOp(NodeCollector):

    def __init__(self, *, fout=None):
        if fout is None:
            fout = sys.stdout
        self._fout = fout

    def display(self, edge_list):
        if isinstance(edge_list, BddEdge):
            edge_list = [edge_list]
        
        for edge in edge_list:
            self.get_node(edge)

        for i, edge in enumerate(edge_list):
            self._fout.write("Root{:2d}: ".format(i + 1))
            self.disp_edge(edge)
            self._fout.write('\n')

        for node in self.node_list:
            self._fout.write("Node#{:3d}: L{:2d}: ".format(node.id, node.index))
            self.disp_edge(node.edge0)
            self._fout.write(": ")
            self.disp_edge(node.edge1)
            self._fout.write('\n')

    def disp_edge(self, edge):
        if edge.is_zero():
            self._fout.write("ZERO")
        elif edge.is_one():
            self._fout.write(" ONE")
        else:
            node = edge.node
            inv = edge.inv
            if inv:
                inv_char = "~"
            else:
                inv_char = " "
            self._fout.write("{:1}{:3d}".format(inv_char, node.id))
            
