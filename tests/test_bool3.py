#! /usr/bin/env python3

"""
lctools.Bool3 のユニットテスト

:file: test_bool3.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import sys
import os.path
sys.path.append(os.pardir)
import pytest
from lctools import Bool3, toBool3


def test_toBool3_good():
    # 変換前の入力と変換後の値のペアのリスト
    io_list = (
        ('0', Bool3._0),
        (0, Bool3._0),
        (False, Bool3._0),

        ('1', Bool3._1),
        (1, Bool3._1),
        (True, Bool3._1),

        ('X', Bool3._d),
        ('x', Bool3._d),
        ('D', Bool3._d),
        ('d', Bool3._d),
        ('*', Bool3._d),
        ('-', Bool3._d)
        )

    for i, o in io_list:
        x = toBool3(i)
        assert x == o

def test_toBool3_bad():
    # 不正な値で例外送出のテスト
    with pytest.raises(ValueError):
        x = toBool3(3)

# invert 演算の期待値データ
@pytest.fixture
def inv_data():
    io_list = (
        ('0', '1'),
        ('1', '0'),
        ('d', 'd')
        )
    return io_list

def test_inv(inv_data):
    # Bool3 の invert 演算のテスト
    for i, o in inv_data:
        i = toBool3(i)
        o = toBool3(o)
        x = ~i
        assert x == o

# and 演算の期待値データ
@pytest.fixture
def and_data():
    io_list = (
        ('0', '0', '0'),
        ('0', '1', '0'),
        ('0', 'd', '0'),

        ('1', '0', '0'),
        ('1', '1', '1'),
        ('1', 'd', 'd'),

        ('d', '0', '0'),
        ('d', '1', 'd'),
        ('d', 'd', 'd')
        )
    return io_list

def test_and(and_data):
    # Bool3 どうしのAND演算のテスト
    for i1, i2, o in and_data:
        i1 = toBool3(i1)
        i2 = toBool3(i2)
        o = toBool3(o)
        x = i1 & i2
        assert x == o

def test_and1(and_data):
    # Bool3 と定数のAND演算のテスト
    for i1, i2, o in and_data:
        i1 = toBool3(i1)
        o = toBool3(o)
        x = i1 & i2
        assert x == o

def test_and2(and_data):
    # 定数と Bool3 のAND演算のテスト
    for i1, i2, o in and_data:
        i2 = toBool3(i2)
        o = toBool3(o)
        x = i1 & i2
        assert x == o

# or 演算の期待値データ
@pytest.fixture
def or_data():
    io_list = (
        ('0', '0', '0'),
        ('0', '1', '1'),
        ('0', 'd', 'd'),

        ('1', '0', '1'),
        ('1', '1', '1'),
        ('1', 'd', '1'),

        ('d', '0', 'd'),
        ('d', '1', '1'),
        ('d', 'd', 'd')
        )
    return io_list

def test_or(or_data):
    # Bool3 どうしのOR演算のテスト
    for i1, i2, o in or_data:
        i1 = toBool3(i1)
        i2 = toBool3(i2)
        o = toBool3(o)
        x = i1 | i2
        assert x == o

def test_or1(or_data):
    # Bool3 と定数のOR演算のテスト
    for i1, i2, o in or_data:
        i1 = toBool3(i1)
        o = toBool3(o)
        x = i1 | i2
        assert x == o

def test_or2(or_data):
    # 定数の Bool3 のOR演算のテスト
    for i1, i2, o in or_data:
        i2 = toBool3(i2)
        o = toBool3(o)
        x = i1 | i2
        assert x == o

# xor 演算の期待値データ
@pytest.fixture
def xor_data():
    io_list = (
        ('0', '0', '0'),
        ('0', '1', '1'),
        ('0', 'd', 'd'),

        ('1', '0', '1'),
        ('1', '1', '0'),
        ('1', 'd', 'd'),

        ('d', '0', 'd'),
        ('d', '1', 'd'),
        ('d', 'd', 'd')
        )
    return io_list

def test_xor(xor_data):
    # Bool3 どうしのXOR演算のテスト
    for i1, i2, o in xor_data:
        i1 = toBool3(i1)
        i2 = toBool3(i2)
        o = toBool3(o)
        x = i1 ^ i2
        assert x == o

def test_xor1(xor_data):
    # Bool3 と定数のXOR演算のテスト
    for i1, i2, o in xor_data:
        i1 = toBool3(i1)
        o = toBool3(o)
        x = i1 ^ i2
        assert x == o

def test_xor2(xor_data):
    # 定数の Bool3 どうしのXOR演算のテスト
    for i1, i2, o in xor_data:
        i2 = toBool3(i2)
        o = toBool3(o)
        x = i1 ^ i2
        assert x == o
