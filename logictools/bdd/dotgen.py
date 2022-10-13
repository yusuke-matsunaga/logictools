#! /usr/bin/env python3

"""Bdd の内容を dot 形式で出力するクラス

:file: bdddotgen.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

import sys
from logictools.bdd.bddedge import BddEdge
from logictools.bdd.nodecollector import NodeCollector


class DotGen(NodeCollector):

    def __init__(self, *, attr_dict={}, fout=None):
        super().__init__()
        if fout is None:
            fout = sys.stdout
        self._fout = fout
        
        self._graph_attr = {"rankdir":"TB"}
        self._root_attr = {"shape":"box"}
        self._node_attr = {}
        self._terminal_attr = {"shape":"box"}
        self._terminal0_attr = {"label":'"0"'}
        self._terminal1_attr = {"label":'"1"'}
        self._edge_attr = {}
        self._edge0_attr = {"style":"dotted"}
        self._edge1_attr = {}
        for key, value in attr_dict.items():
            pos = key.find(':')
            if pos == -1:
                # 全てのタイプに設定する．
                self._root_attr[key] = value
                self._terminal_attr[key] = value
                self._edge_attr[key] = value
            else:
                attr_type = key[:pos]
                attr_name = key[pos + 1:]
                if attr_type == 'graph':
                    self._graph_attr[attr_name] = value
                elif attr_type == 'root':
                    self._root_attr[attr_name] = value
                elif attr_type == 'node':
                    self._node_attr[attr_name] = value
                elif attr_type == 'terminal':
                    self._terminal_attr[attr_name] = value
                elif attr_type == 'terminal0':
                    self._terminal0_attr[attr_name] = value
                elif attr_type == 'terminal1':
                    self._terminal1_attr[attr_name] = value
                elif attr_type == 'edge':
                    self._edge_attr[attr_name] = value
                elif attr_type == 'edge0':
                    self._edge0_attr[attr_name] = value
                elif attr_type == 'edge1':
                    self._edge1_attr[attr_name] = value
                else:
                    raise exception()
        self._attr_str = ""
        
    def write(self, root_list):
        if isinstance(root_list, BddEdge):
            root_list = [root_list]

        for edge in root_list:
            self.get_node(edge)

        # グラフ全体の記述
        self._fout.write("digraph bdd {\n")
        self._fout.write("  graph")
        self._attr_begin()
        self._attr_add_list(self._graph_attr)
        self._attr_end()

        # 根のノードの定義
        for i, edge in enumerate(root_list):
            self._fout.write("  root{}".format(i + 1))
            self._attr_begin()
            self._attr_add_list(self._root_attr)
            label = '"BDD#{}"'.format(i + 1)
            self._attr_add("label", label)
            self._attr_end()

        # ノードの定義
        for node in self.node_list:
            self._fout.write("  node{}".format(node.id))
            self._attr_begin()
            label = '"{}"'.format(node.index)
            self._attr_add("label", label);
            self._attr_add_list(self._node_attr)
            self._attr_end()

        # 終端の定義
        self._write_terminal(0)
        self._write_terminal(1)

        # 根の枝の定義
        for i, edge in enumerate(root_list):
            self._fout.write("  root{}".format(i + 1))
            self._write_edge(edge, False)

        # 枝の定義
        for node in self.node_list:
            self._fout.write("  node{}".format(node.id))
            self._write_edge(node.edge0, True)
            self._fout.write("  node{}".format(node.id))
            self._write_edge(node.edge1, False)

        # 根のランクの設定
        self._fout.write("  { rank = same;")
        for i in range(len(root_list)):
            self._fout.write(" root{};".format(i + 1))
        self._fout.write("}\n")

        # ノードランクの設定
        for i in range(self.max_index):
            self._fout.write("  { rank = same;")
            for node in self.indexed_node_list(i):
                self._fout.write(" node{};".format(node.id))
            self._fout.write("}\n")

        # dot の終了
        self._fout.write("}\n")
        
    def _write_terminal(self, one):
        self._fout.write("  const{}".format(one))

        self._attr_begin()
        self._attr_add_list(self._terminal_attr)
        if one:
            self._attr_add_list(self._terminal1_attr)
        else:
            self._attr_add_list(self._terminal0_attr)
        self._attr_end()
        
    def _write_edge(self, edge, zero):
        self._fout.write(" -> ")
        inv = False
        if edge.is_zero():
            self._fout.write("const0")
        elif edge.is_one():
            self._fout.write("const1")
        else:
            inv = edge.inv
            node = edge.node
            self._fout.write("node{}".format(node.id))

        self._attr_begin()
        self._attr_add_list(self._edge_attr)
        if zero:
            self._attr_add_list(self._edge0_attr)
        else:
            self._attr_add_list(self._edge1_attr)
        if inv:
            self._attr_add("dir", "both")
            self._attr_add("arrowtail", "odot")
        self._attr_end()

    def _attr_begin(self):
        self._attr_str = " ["

    def _attr_add_list(self, attr_list):
        for key, value in attr_list.items():
            self._attr_add(key, value)

    def _attr_add(self, key, value):
        if value is None:
            return

        self._fout.write(self._attr_str)
        self._attr_str = ", "
        self._fout.write('{} = {}'.format(key, value))

    def _attr_end(self):
        if self._attr_str == ", ":
            self._fout.write("]")
        self._fout.write('\n')
