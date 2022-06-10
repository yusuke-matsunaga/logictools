#! /usr/bin/env python3

"""
有限状態機械の等価状態対の状態を表すクラス

:file: eqtable.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""


class EqTable:
    """有限状態機械の等価状態対の情報を格納するテーブル

    2つの状態番号とステップ番号をキーとして，
    以下の情報を持つ．
    - 等価な場合は条件となる状態対の集合
    - 等価でない場合はその印

    等価な場合に条件が空の場合があるので等価でない場合は
    set() ではなく None を持つ．
    """

    def __init__(self):
        """初期化
        """

        self.__marks = dict()
        self.__max_step = 0

    def get(self, s, t, step=None):
        """内容を取り出す．

        :param int s, t: 状態番号
        :param int step: ステップ
        :return: 対応する状態対の set を返す．

        step が指定されなかった場合には max_step が用いられる．
        """
        if step is None:
            step = self.__max_step
        if s < t:
            key = (s, t, step)
        else:
            key = (t, s, step)
        if key in self.__marks:
            return self.__marks[key]
        else:
            return None

    def get_all_pairs(self):
        """等価状態対を全て取り出す．

        :return: 等価状態対のリストを返す．
        """

        ans_list = list()
        for s, t, step in self.__marks.keys():
            if step == self.__max_step:
                ans_list.append((s, t))
        return ans_list

    def get_all_groups(self):
        """等価状態グループをすべて取り出す．
        """
        rep_dict = {}
        state_set = set()
        for s, t, step in self.__marks.keys():
            if step == self.__max_step:
                assert s < t
                state_set.add(s)
                state_set.add(t)
                if s not in rep_dict:
                    rep_dict[s] = s
                elif rep_dict[s] > s:
                    rep_dict[s] = s
                if t not in rep_dict:
                    rep_dict[t] = s
                elif rep_dict[t] > s:
                    rep_dict[t] = s
        group_dict = {}
        for s in state_set:
            r = rep_dict[s]
            if r not in group_dict:
                group_dict[r] = list()
            group_dict[r].append(s)
        ans_list = list()
        for s_list in group_dict.values():
            ans_list.append(s_list)
        return ans_list

    def put(self, s, t, step, cond_set):
        """内容を追加する．

        :param int s, t: 状態番号
        :param int step: ステップ
        :param set cond_set: 条件を表す状態対のセット

        """
        if s < t:
            key = (s, t, step)
        else:
            key = (t, s, step)
        self.__marks[key] = cond_set
        if self.__max_step < step:
            self.__max_step = step

    @property
    def max_step(self):
        """step の最大値を返す．
        """
        return self.__max_step
