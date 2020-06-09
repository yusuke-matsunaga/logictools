#! /usr/bin/env python3

### @file state.py
### @brief State の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019 Yusuke Matsunaga
### All rights reserved.

### @brief 有限状態機械の状態を表すクラス
###
### 状態名と次状態/出力記号の辞書を持つ．
### 辞書のキーは入力記号
class State :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] name 状態名
    def __init__(self, id, name) :
        self.__id = id
        self.__name = name
        self.__next_func = {}

    ### @brief 次状態と出力を設定する．
    ### @param[in] input_val 入力記号
    ### @param[in] next_state 次状態
    ### @param[in] output_val 出力記号
    def set_next(self, input_val, next_state, output_val) :
        self.__next_func[input_val] = (next_state, output_val)

    ### @brief ID番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief 名前を返す．
    @property
    def name(self) :
        return self.__name

    ### @brief 次状態と出力記号のタプルを返す．
    ### @param[in] input_val 入力記号
    def next(self, input_val) :
        return self.__next_func[input_val]
