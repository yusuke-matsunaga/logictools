#! /usr/bin/env python3

"""
Cube のテストプログラム

:file: test_cube.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import sys
import os.path
sys.path.append(os.pardir)
import pytest
from lctools import Bool3, toBool3
from lctools import Cube


def test_init1():
    """入力数を指定したCube()のテスト"""
    N = 4
    c = Cube(N)
    assert c.input_num == N
    assert c.literal_num == 0
    len(c) == N
    for i in range(N):
        assert c[i] == Bool3._d

def test_init2():
    """リストを指定したCube()のテスト"""
    # 実は Bool3 へ変換可能な値ならなんでもよい．
    lit_list = [0, '1', Bool3._d]
    c = Cube(lit_list)
    assert c.input_num == len(lit_list)
    assert c.literal_num == len([x for x in lit_list if toBool3(x) != Bool3._d])
    for i in range(c.input_num):
        assert c[i] == toBool3(lit_list[i])

def test_init3():
    """文字列を指定したCube()のテスト"""
    pat_str = "01-"
    c = Cube(pat_str)
    assert c.input_num == len(pat_str)
    assert c.literal_num == len([x for x in pat_str if toBool3(x) != Bool3._d])
    for i in range(c.input_num):
        assert c[i] == toBool3(pat_str[i])

def test_set_posliteral_bad():
    """範囲外のset_posliteral()に対するテスト"""
    c = Cube(4)
    with pytest.raises(AssertionError):
        c.set_posliteral(-1)
    with pytest.raises(AssertionError):
        c.set_posliteral(4)

def test_set_negliteral_bad():
    """範囲外のset_negliteral()に対するテスト"""
    c = Cube(4)
    with pytest.raises(AssertionError):
        c.set_negliteral(-1)
    with pytest.raises(AssertionError):
        c.set_negliteral(4)

def test_clr_literal_bad():
    """範囲外のclr_literal()に対するテスト"""
    c = Cube(4)
    with pytest.raises(AssertionError):
        c.clr_literal(-1)
    with pytest.raises(AssertionError):
        c.clr_literal(4)

def test_set_posliteral():
    """通常のset_posliteral()に対するテスト"""
    c = Cube('01--')
    # 同じ値の上書き
    c.set_posliteral(1)
    assert c[1] == Bool3._1
    # 0 -> 1 の上書き
    c.set_posliteral(0)
    assert c[0] == Bool3._1
    # d -> 1 の上書き
    c.set_posliteral(2)
    assert c[2] == Bool3._1

def test_set_negliteral():
    """通常のset_negliteral()に対するテスト"""
    c = Cube('01--')
    # 同じ値の上書き
    c.set_negliteral(0)
    assert c[0] == Bool3._0
    # 1 -> 0 の上書き
    c.set_negliteral(1)
    assert c[1] == Bool3._0
    # d -> 0 の上書き
    c.set_negliteral(2)
    assert c[2] == Bool3._0

def test_clr_literal():
    """通常のclr_literal()に対するテスト"""
    c = Cube('01--')
    # 同じ値の上書き
    c.clr_literal(2)
    assert c[2] == Bool3._d
    # 0 -> d の上書き
    c.clr_literal(0)
    assert c[0] == Bool3._d
    # 1 -> d の上書き
    c.clr_literal(1)
    assert c[1] == Bool3._d
