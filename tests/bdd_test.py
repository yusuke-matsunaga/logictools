#! /usr/bin/env python3

"""Bdd, BddMgr のテストプログラム

:file: bdd_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from lctools import BddMgr, Bdd


def test_BddMgr_zero():
    mgr = BddMgr()

    bdd = mgr.zero()
    assert bdd.is_zero()
    assert not bdd.is_one()
    assert bdd.is_const()

def test_BddMgr_one():
    mgr = BddMgr()

    bdd = mgr.one()
    assert not bdd.is_zero()
    assert bdd.is_one()
    assert bdd.is_const()

def test_BddMgr_literal1():
    mgr = BddMgr()

    vindex = 0
    bdd = mgr.literal(vindex)
    
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

    index, e0, e1 = bdd.root_decomp()

    assert index == vindex
    assert e0.is_zero()
    assert e1.is_one()
    
def test_BddMgr_literal2():
    mgr = BddMgr()

    vindex = 0
    bdd = mgr.literal(vindex, True)
    
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

    index, e0, e1 = bdd.root_decomp()

    assert index == vindex
    assert e0.is_one()
    assert e1.is_zero()
    
def test_BddMgr_posi_literal():
    mgr = BddMgr()

    vindex = 0
    bdd = mgr.posi_literal(vindex)
    
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

    index, e0, e1 = bdd.root_decomp()

    assert index == vindex
    assert e0.is_zero()
    assert e1.is_one()
    
def test_BddMgr_nega_literal():
    mgr = BddMgr()

    vindex = 0
    bdd = mgr.nega_literal(vindex)
    
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

    index, e0, e1 = bdd.root_decomp()

    assert index == vindex
    assert e0.is_one()
    assert e1.is_zero()

def test_BddMgr_from_truth1():
    mgr = BddMgr()

    bdd = mgr.from_truth("1000")
    
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

    index, e0, e1 = bdd.root_decomp()

    assert index == 0
    assert e0.is_zero()
    assert not e0.is_one()
    assert e0.is_const()
    
    index2, e10, e11 = e1.root_decomp()

    assert index2 == 1
    assert e10.is_zero()
    assert e11.is_one()

def test_Bdd_invert():
    mgr = BddMgr()

    bdd = mgr.from_truth("0100")

    bdd1 = ~bdd

    exp_bdd = mgr.from_truth("1011")
    assert bdd1 == exp_bdd
    
def test_Bdd_and1():
    mgr = BddMgr()

    v1 = 0
    v2 = 1
    lit1 = mgr.posi_literal(v1)
    lit2 = mgr.nega_literal(v2)
    bdd = lit1 & lit2
    
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

    index, e0, e1 = bdd.root_decomp()

    assert index == v1
    assert e0.is_zero()
    assert not e0.is_one()
    assert e0.is_const()

    index2, e10, e11 = e1.root_decomp()

    assert index2 == v2
    assert e10.is_one()
    assert e11.is_zero()
    
def test_Bdd_iand1():
    mgr = BddMgr()

    v1 = 0
    v2 = 1
    bdd = mgr.posi_literal(v1)
    lit2 = mgr.nega_literal(v2)
    bdd &= lit2
    
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

    index, e0, e1 = bdd.root_decomp()

    assert index == v1
    assert e0.is_zero()
    assert not e0.is_one()
    assert e0.is_const()

    index2, e10, e11 = e1.root_decomp()

    assert index2 == v2
    assert e10.is_one()
    assert e11.is_zero()
    
def test_Bdd_or1():
    mgr = BddMgr()

    v1 = 0
    v2 = 1
    lit1 = mgr.posi_literal(v1)
    lit2 = mgr.nega_literal(v2)
    bdd = lit1 | lit2
    
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

    index, e0, e1 = bdd.root_decomp()

    assert index == v1
    assert e1.is_one()
    assert not e1.is_zero()
    assert e1.is_const()

    index2, e00, e01 = e0.root_decomp()

    assert index2 == v2
    assert e00.is_one()
    assert e01.is_zero()
    
def test_Bdd_ior1():
    mgr = BddMgr()

    v1 = 0
    v2 = 1
    bdd = mgr.posi_literal(v1)
    lit2 = mgr.nega_literal(v2)
    bdd |= lit2
    
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

    index, e0, e1 = bdd.root_decomp()

    assert index == v1
    assert e1.is_one()
    assert not e1.is_zero()
    assert e1.is_const()

    index2, e00, e01 = e0.root_decomp()

    assert index2 == v2
    assert e00.is_one()
    assert e01.is_zero()
    
def test_Bdd_xor1():
    mgr = BddMgr()

    v1 = 0
    v2 = 1
    lit1 = mgr.posi_literal(v1)
    lit2 = mgr.nega_literal(v2)
    bdd = lit1 ^ lit2

    exp_bdd = mgr.from_truth("1001")

    assert exp_bdd == bdd
    
def test_Bdd_ixor1():
    mgr = BddMgr()

    v1 = 0
    v2 = 1
    bdd = mgr.posi_literal(v1)
    lit2 = mgr.posi_literal(v2)
    bdd ^= lit2

    exp_bdd = mgr.from_truth("0110")

    assert exp_bdd == bdd

def test_Bdd_invalid1():
    bdd = Bdd()

    assert bdd.is_invalid()
    assert not bdd.is_valid()
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()

def test_Bdd_invalid1():
    bdd = Bdd.invalid()

    assert bdd.is_invalid()
    assert not bdd.is_valid()
    assert not bdd.is_zero()
    assert not bdd.is_one()
    assert not bdd.is_const()
    
def test_Bdd_copy_constructor1():
    mgr = BddMgr()

    bdd = mgr.from_truth("0110")

    bdd1 = mgr.copy(bdd)

    assert bdd == bdd1

def test_Bdd_copy_constructor2():
    mgr = BddMgr()

    bdd = mgr.from_truth("0110")

    mgr2 = BddMgr()
    bdd1 = mgr2.copy(bdd)
    
    assert bdd != bdd1
    
    bdd2 = mgr.copy(bdd1)

    assert bdd == bdd2
