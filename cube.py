#! /usr/bin/env python3
#
# @file cube.py
# @brief Cube の定義ファイル
# @author Yusuke Matsunaga (松永 裕介)
#
# Copyright (C) 2017 Yusuke Matsunaga
# All rights reserved.

## @class Cube
# @brief キューブを表すクラス
#
# 入力数が高々10程度と仮定して符号なし整数１語で表す．
class Cube :

    ## @brief 空のキューブを作る．
    # @param[in] input_num 入力数
    staticmethod
    def make_empty_cube(input_num) :
        return Cube(input_num)

    ## @brief
    ## @brief 初期化
    # @param[in] input_num 入力数
    #
    # 内容は空のキューブとなる．
    def __init__(self, input_num) :
        self.__input_num = input_num
        self.__body = 0

    ## @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ## @brief pos番目の位置のパタンを返す．
    # @param[in] pos 位置 ( 0 <= pos < input_num )
    # @retval 0 ドントケア
    # @retval 1 positive literal
    # @retval 2 negative literal
    def operator[](self, pos) :
        assert 0 <= pos < self.input_num
        sft = (self.input_num - pos - 1) * 2
        return (self.__body >> sft) & 3
