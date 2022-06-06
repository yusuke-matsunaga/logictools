#! /usr/bin/env python3

"""State の実装ファイル

:file: state.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2019 Yusuke Matsunaga, All rights reserved.
"""


class State:
    """有限状態機械の状態を表すクラス
    """

    def __init__(self, id, name):
        """初期化

        :param id: ID番号
        :param name: 状態名

        状態名と次状態/出力記号の辞書を持つ．
        辞書のキーは入力記号
        """

        self.__id = id
        self.__name = name
        self.__next_func = {}

    def set_next(self, input_val, next_state, output_val):
        """次状態と出力を設定する．

        :param input_val: 入力記号
        :param next_state: 次状態
        :param output_val: 出力記号
        """
        self.__next_func[input_val] = (next_state, output_val)

    @property
    def id(self):
        """ID番号を返す．"""
        return self.__id

    @property
    def name(self):
        """名前を返す．"""
        return self.__name

    def next(self, input_val):
        """
        次状態と出力記号のタプルを返す．

        :param input_val: 入力記号
        """
        return self.__next_func[input_val]
