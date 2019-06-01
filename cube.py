#! /usr/bin/env python3

### @file cube.py
### @brief Cube の定義ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2017, 2019 Yusuke Matsunaga
### All rights reserved.

### @class Cube
### @brief キューブを表すクラス
###
### 入力数が高々10程度と仮定して符号なし整数１語で表す．
class Cube :

    ### @brief
    ### @brief 初期化
    ### @param[in] input_num 入力数
    ### @param[in] pat_str パタン文字列
    ###
    ### * input_num と pat_str のどちらか一方は指定されなければならない．
    ### * input_num と pat_str の両方が指定された場合，pat_str の長さは
    ###   input_num と等しくなければならない．
    ### * pat_str は '0'，'1'，'-' からなる．
    def __init__(self, *, input_num = None, pat_str = None) :
        assert input_num != None or pat_str != None
        if input_num != None and pat_str != None :
            assert len(pat_str) == input_num
        if input_num == None :
            input_num = len(pat_str)
        self.__input_num = input_num
        self.__body = 0

    ### @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ### @brief pos番目の位置のパタンを返す．
    ### @param[in] pos 位置 ( 0 <= pos < input_num )
    ### @retval 0 ドントケア
    ### @retval 1 positive literal
    ### @retval 2 negative literal
    def operator[](self, pos) :
        assert 0 <= pos < self.input_num
        sft = (self.input_num - pos - 1) * 2
        return (self.__body >> sft) & 3
