#! /usr/bin/env python3

"""
BoolFunc のテストプログラム

:file: boolfunc_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from lctools import BoolFunc, Bool3


def test_BoolFunc_init1():
    f = BoolFunc("0001")

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._0
    assert f.val([0, 1]) == Bool3._0
    assert f.val([1, 0]) == Bool3._0
    assert f.val([1, 1]) == Bool3._1


def test_BoolFunc_const0():
    f = BoolFunc.make_const0(2)

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._0
    assert f.val([0, 1]) == Bool3._0
    assert f.val([1, 0]) == Bool3._0
    assert f.val([1, 1]) == Bool3._0


def test_BoolFunc_const1():
    f = BoolFunc.make_const1(2)

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._1
    assert f.val([0, 1]) == Bool3._1
    assert f.val([1, 0]) == Bool3._1
    assert f.val([1, 1]) == Bool3._1


def test_BoolFunc_literal1():
    f = BoolFunc.make_literal(2, 0)

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._0
    assert f.val([0, 1]) == Bool3._0
    assert f.val([1, 0]) == Bool3._1
    assert f.val([1, 1]) == Bool3._1


def test_BoolFunc_literal2():
    f = BoolFunc.make_literal(2, 1)

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._0
    assert f.val([0, 1]) == Bool3._1
    assert f.val([1, 0]) == Bool3._0
    assert f.val([1, 1]) == Bool3._1


def test_BoolFunc_not_literal1():
    f = BoolFunc.make_literal(2, 0)
    f = ~f

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._1
    assert f.val([0, 1]) == Bool3._1
    assert f.val([1, 0]) == Bool3._0
    assert f.val([1, 1]) == Bool3._0


def test_BoolFunc_not_literal2():
    f = BoolFunc.make_literal(2, 1)
    f = ~f

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._1
    assert f.val([0, 1]) == Bool3._0
    assert f.val([1, 0]) == Bool3._1
    assert f.val([1, 1]) == Bool3._0


def test_BoolFunc_and():
    x1 = BoolFunc.make_literal(2, 0)
    x2 = BoolFunc.make_literal(2, 1)

    f = x1 & x2

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._0
    assert f.val([0, 1]) == Bool3._0
    assert f.val([1, 0]) == Bool3._0
    assert f.val([1, 1]) == Bool3._1


def test_BoolFunc_or():
    x1 = BoolFunc.make_literal(2, 0)
    x2 = BoolFunc.make_literal(2, 1)

    f = x1 | x2

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._0
    assert f.val([0, 1]) == Bool3._1
    assert f.val([1, 0]) == Bool3._1
    assert f.val([1, 1]) == Bool3._1


def test_BoolFunc_xor():
    x1 = BoolFunc.make_literal(2, 0)
    x2 = BoolFunc.make_literal(2, 1)

    f = x1 ^ x2

    assert f.input_num == 2
    assert f.val([0, 0]) == Bool3._0
    assert f.val([0, 1]) == Bool3._1
    assert f.val([1, 0]) == Bool3._1
    assert f.val([1, 1]) == Bool3._0


def test_BoolFunc_from_string():
    expr_str = "x_1 & x_2 | ~x_3 & ~x_4"
    var_map = {'x_1': 0, 'x_2': 1, 'x_3': 2, 'x_4': 3}
    f = BoolFunc.make_from_string(expr_str, 4, var_map)

    assert f is not None
    assert f.input_num == 4
    assert f.val([1, 1, 0, 0]) == Bool3._1
    assert f.val([0, 0, 1, 1]) == Bool3._0
