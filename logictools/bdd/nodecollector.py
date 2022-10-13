#! /usr/bin/env python3

"""NodeCollector の実装クラス

:file: nodecollector.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""


class NodeCollector:
    """Bdd のノードを DFS で集めるためのクラス
    """

    def __init__(self):
        self._node_list = []
        self._indexed_node_list = []

    def get_node(self, edge):
        """edge を根とする部分グラフをDFSにたどり
        ノードを node_list に入れる．
        """
        if edge.is_const():
            return

        node = edge.node
        if node in self._node_list:
            return

        self._node_list.append(node)
        index = node.index
        while len(self._indexed_node_list) <= index:
            self._indexed_node_list.append([])
        self._indexed_node_list[index].append(node)
        self.get_node(node.edge0)
        self.get_node(node.edge1)

    @property
    def node_list(self):
        """ノードリストを返す．
        """
        for node in self._node_list:
            yield node

    @property
    def max_index(self):
        """インデックスの最大値を返す．
        """
        return len(self._indexed_node_list)
    
    def indexed_node_list(self, index):
        """インデックスごとのノードリストを返す．
        """
        for node in self._indexed_node_list[index]:
            yield node
        
