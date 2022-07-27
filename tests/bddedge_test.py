#! /usr/bin/env python3

"""BddEdge のテストプログラム

:file: bddedge_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from lctools.bdd.bddedge import BddEdge


def test_BddEdge_zero():
    e = BddEdge.zero()

    assert e.is_zero()
    assert not e.is_one()
    assert e.is_const()
    assert e.node is None
    assert e.inv == False

def test_BddEdge_one():
    e = BddEdge.one()

    assert not e.is_zero()
    assert e.is_one()
    assert e.is_const()
    assert e.node is None
    assert e.inv == True

def test_BddEdge_invert():
    e = BddEdge.zero()

    e1 = ~e
    
    assert not e1.is_zero()
    assert e1.is_one()
    assert e1.is_const()
    assert e1.node is None
    assert e1.inv == True

def test_BddEdge_posi_edge():
    zero = BddEdge.zero()
    one = BddEdge.one()

    e1 = zero.posi_edge()
    e2 = one.posi_edge()

    assert e1 == e2
    assert e1.is_zero()

def test_BddEdge_nega_edge():
    zero = BddEdge.zero()
    one = BddEdge.one()

    e1 = zero.nega_edge()
    e2 = one.nega_edge()

    assert e1 == e2
    assert e1.is_one()

def test_BddEdge_make_positive():
    zero = BddEdge.zero()
    one = BddEdge.one()

    zero.make_positive()
    one.make_positive()

    assert zero == one
    assert zero.is_zero()

def test_BddEdge_make_negative():
    zero = BddEdge.zero()
    one = BddEdge.one()

    zero.make_negative()
    one.make_negative()

    assert zero == one
    assert zero.is_one()

def test_BddEdge_mul():
    zero = BddEdge.zero()

    e1 = zero * True
    e2 = zero * False

    assert e1.is_one()
    assert e2.is_zero()

def test_BddEdge_imul():
    e1 = BddEdge.zero()
    e2 = BddEdge.zero()

    e1 *= True
    e2 *= False

    assert e1.is_one()
    assert e2.is_zero()
