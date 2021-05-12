#! /usr/bin/env python3

"""
Bool3 の実装ファイル

:file: bool3.py
:author: Yusuke Matsunaga (松永 裕介)

:copyright: Copyright (C) 2019 Yusuke Matsunaga, All rights reserved.
"""

from enum import Enum


class Bool3(Enum):
    """3値のブール値を表すクラス

    _0 と _1 および _d を要素とする列挙型．
    _1 と _0 は Python3 の組み込み型の True と False に対応する．
    このクラスでは第３の値として _d (don't care) が定義されている．
    _d は _0 もしくは _1 のどちらかの値を取るという意味で，
    _d を含んだ演算の結果が不定の場合には結果も _d となる．
    _0 との AND のように結果が決まる場合には _d との演算でも
    結果が _0 または _1 に定まる場合もある．

    もちろん，この３値の代数系はBool代数の基本律を満たしている．

    文字列や数値からの変換関数 toBool3() を用いて Bool3 型へ変換
    することもできる．

    通常の論理演算子 \~, \&, \|, \^ を用いてBool3どうしの論理演算を行なう
    ことができる．また，右辺か左辺のどちらか一方でも Bool3 型ならば，
    上記の文字列や数値から Bool3 に変換を行って論理演算を行なうことができる．
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
        other = toBool3(other)
        if self == Bool3._0 or other == Bool3._0:
            return Bool3._0
        elif self == Bool3._1 and other == Bool3._1:
            return Bool3._1
        else:
            return Bool3._d

    def __rand__(self, other):
        """AND 演算子(右辺がBool3)"""
        other = toBool3(other)
        if self == Bool3._0 or other == Bool3._0:
            return Bool3._0
        elif self == Bool3._1 and other == Bool3._1:
            return Bool3._1
        else:
            return Bool3._d

    def __or__(self, other):
        """OR 演算子"""
        other = toBool3(other)
        if self == Bool3._1 or other == Bool3._1:
            return Bool3._1
        elif self == Bool3._0 and other == Bool3._0:
            return Bool3._0
        else:
            return Bool3._d

    def __ror__(self, other):
        """OR 演算子(右辺がBool3)"""
        other = toBool3(other)
        if self == Bool3._1 or other == Bool3._1:
            return Bool3._1
        elif self == Bool3._0 and other == Bool3._0:
            return Bool3._0
        else:
            return Bool3._d

    def __xor__(self, other):
        """XOR 演算子"""
        other = toBool3(other)
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

    def __rxor__(self, other):
        """XOR 演算子(右辺がBool3)"""
        other = toBool3(other)
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
        assert isinstance(other, Bool3)
        return self.value < other.value

    def __gt__(self, other):
        """大なり比較演算子"""
        assert isinstance(other, Bool3)
        return self.value > other.value

    def __le__(self, other):
        """小なりイコール比較演算子"""
        assert isinstance(other, Bool3)
        return self.value <= other.value

    def __ge__(self, other):
        """大なりイコール比較演算子"""
        assert isinstance(other, Bool3)
        return self.value >= other.value


def toBool3(arg):
    """Bool3型へ変換する．

    _0: 文字列'0'，数値0，ブール値False
    _1: 文字列'1'，数値1，ブール値True
    _d: 文字列'X'，'x'，'D'，'d'，'*'，'-'

    それ以外の場合には例外(ValueError)が送出される．
    """
    if isinstance(arg, Bool3):
        return arg
    if arg == '0' or arg == 0 or arg is False:
        return Bool3._0
    if arg == '1' or arg == 1 or arg is True:
        return Bool3._1
    if arg == 'X' or arg == 'x':
        return Bool3._d
    if arg == 'D' or arg == 'd':
        return Bool3._d
    if arg == '*' or arg == '-':
        return Bool3._d
    raise ValueError()
