#! /usr/bin/env python3

"""
Bool3 の実装ファイル

:file: bool3.py
:author: Yusuke Matsunaga (松永 裕介)

:copyright: Copyright (C) 2019 Yusuke Matsunaga, All rights reserved.
"""

from enum import Enum


class Bool3(Enum):
    """
    3値のブール値を表すクラス
    """
    _d = 0
    _1 = 1
    _0 = 2

    def __invert__(self):
        """反転した値を返す．"""
        if self == Bool3._d:
            return Bool3._d
        elif self == Bool3._0:
            return Bool3._1
        elif self == Bool3._1:
            return Bool3._0
        else:
            assert False

    def __and__(self, other):
        """AND 演算子"""
        assert isinstance(other, Bool3)
        if self == Bool3._0 or other == Bool3._0:
            return Bool3._0
        elif self == Bool3._1 and other == Bool3._1:
            return Bool3._1
        else:
            return Bool3._d

    def __or__(self, other):
        """OR 演算子"""
        assert isinstance(other, Bool3)
        if self == Bool3._1 or other == Bool3._1:
            return Bool3._1
        elif self == Bool3._0 and other == Bool3._0:
            return Bool3._0
        else:
            return Bool3._d

    def __xor__(self, other):
        """XOR 演算子"""
        assert isinstance(other, Bool3)
        if self == Bool3._0 and other == Bool3._0:
            return Bool3._0
        elif self == Bool3._0 and other == Bool3._1:
            return Bool3._1
        elif self == Bool3._1 and other == Bool3._0:
            return Bool3._1
        elif self == Bool3._1 and other == Bool3._1:
            return Bool3._0
        else:
            return Bool3._d

    def __str__(self):
        """内容を表す文字列を返す．"""
        if self == Bool3._d:
            return 'd'
        elif self == Bool3._0:
            return '0'
        elif self == Bool3._1:
            return '1'
        else:
            assert False

    def __lt__(self, other):
        """小なり比較演算子"""
        return self.value < other.value

    def __gt__(self, other):
        """大なり比較演算子"""
        return self.value > other.value

    def __le__(self, other):
        """小なりイコール比較演算子"""
        return self.value <= other.value

    def __ge__(self, other):
        """大なりイコール比較演算子"""
        return self.value >= other.value


if __name__ == '__main__':
    # テストコード

    b3_list = [Bool3._d, Bool3._0, Bool3._1]

    print('invert(~) 演算')
    for val in b3_list:
        print('~({}) = {}'.format(val, ~val))

    print('')
    print('and(&) 演算')
    for val1 in b3_list:
        for val2 in b3_list:
            print('{} & {} = {}'.format(val1, val2, val1 & val2))

    print('')
    print('or(|) 演算')
    for val1 in b3_list:
        for val2 in b3_list:
            print('{} | {} = {}'.format(val1, val2, val1 | val2))

    print('')
    print('xor(^) 演算')
    for val1 in b3_list:
        for val2 in b3_list:
            print('{} ^ {} = {}'.format(val1, val2, val1 ^ val2))
