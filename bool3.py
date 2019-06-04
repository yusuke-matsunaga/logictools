#! /usr/bin/env python3

### @file bool3.py
### @brief Bool3 の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019 Yusuke Matsunaga
### All rights reserved.

from enum import Enum


### @brief 3値のブール値を表すクラス
###
### * _d: ドントケア
### * _0: 0
### * _1: 1
class Bool3(Enum) :
    _d = 0
    _1 = 1
    _0 = 2

    ### @brief 値を反転させる．
    def __invert__(self) :
        if self == Bool3._d :
            return Bool3._d
        elif self == Bool3._0 :
            return Bool3._1
        elif self == Bool3._1 :
            return Bool3._0
        else :
            assert False

    ### @brief AND 演算子
    def __and__(self, other) :
        assert isinstance(other, Bool3)
        if self == Bool3._0 or other == Bool3._0 :
            return Bool3._0
        elif self == Bool3._1 and other == Bool3._1 :
            return Bool3._1
        else :
            return Bool3._d

    ### @brief OR 演算子
    def __or__(self, other) :
        assert isinstance(other, Bool3)
        if self == Bool3._1 or other == Bool3._1 :
            return Bool3._1
        elif self == Bool3._0 and other == Bool3._0 :
            return Bool3._0
        else :
            return Bool3._d

    ### @brief XOR 演算子
    def __xor__(self, other) :
        assert isinstance(other, Bool3)
        if self == Bool3._0 and other == Bool3._0 :
            return Bool3._0
        elif self == Bool3._0 and other == Bool3._1 :
            return Bool3._1
        elif self == Bool3._1 and other == Bool3._0 :
            return Bool3._1
        elif self == Bool3._1 and other == Bool3._1 :
            return Bool3._0
        else :
            return Bool3._d

    ### @brief 内容を表す文字列を返す．
    def __str__(self) :
        if self == Bool3._d :
            return 'd'
        elif self == Bool3._0 :
            return '0'
        elif self == Bool3._1 :
            return '1'
        else :
            assert False

    ### @brief 小なり比較演算子
    def __lt__(self, other) :
        return self.value < other.value

    ### @brief 大なり比較演算子
    def __gt__(self, other) :
        return self.value > other.value

    ### @brief 小なりイコール比較演算子
    def __le__(self, other) :
        return self.value <= other.value

    ### @brief 大なりイコール比較演算子
    def __ge__(self, other) :
        return self.value >= other.value

if __name__ == '__main__' :
    b3_list = [ Bool3._d, Bool3._0, Bool3._1]

    print('invert(~) 演算')
    for val in b3_list :
        print('~({}) = {}'.format(val, ~val))

    print('')
    print('and(&) 演算')
    for val1 in b3_list :
        for val2 in b3_list :
            print('{} & {} = {}'.format(val1, val2, val1 & val2))

    print('')
    print('or(|) 演算')
    for val1 in b3_list :
        for val2 in b3_list :
            print('{} | {} = {}'.format(val1, val2, val1 | val2))

    print('')
    print('xor(^) 演算')
    for val1 in b3_list :
        for val2 in b3_list :
            print('{} ^ {} = {}'.format(val1, val2, val1 ^ val2))
