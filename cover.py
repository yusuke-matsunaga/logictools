#! /usr/bin/env python3

### @file cover.py
### @brief Cover の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019 Yusuke Matsunaga
### All rights reserved.

import sys

### @brief カバー(キューブの集合)を表すクラス
class Cover :

    ### @brief 初期化
    ### @param[in] cube_list キューブのリスト
    def __init__(self, cube_list = None) :
        if cube_list :
            self.__cube_list = cube_list
        else :
            self.__cube_list = []

    ### @brief キューブを追加する．
    def add_cube(self, cube) :
        self.__cube_list.append(cube)

    ### @brief キューブ数を返す．
    @property
    def cube_num(self) :
        return len(self.__cube_list)

    ### @brief リテラル数を返す．
    @property
    def literal_num(self) :
        ans = 0
        for cube in self.__cube_list :
            ans += cube.literal_num
        return ans

    ### @brief キューブのリストを返す．
    @property
    def cube_list(self) :
        return self.__cube_list

    ### @brief 要素のキューブを取り出す．
    def __getitem__(self, pos) :
        assert 0 <= pos < self.cube_num
        return self.__cube_list[pos]

    ### @brief 積和形論理式を表す LaTeX 文字列を返す．
    ### @param[in] var_map 変数名の辞書
    def latex_str(self, *, var_map = None) :
        ans = ''
        plus = ''
        for cube in self.__cube_list :
            ans += plus
            plus = ' + '
            ans += cube.latex_str(var_map = var_map)
        return ans

    ### @brief 内容を出力する．
    def print(self, *, fout = None) :
        if fout == None :
            fout = sys.stdout
        for cube in self.__cube_list :
            print(cube, file = fout)
