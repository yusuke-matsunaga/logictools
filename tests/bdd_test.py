#! /usr/bin/env python3

"""Bdd, BddMgr のテストプログラム

:file: bdd_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from lctools import BddMgr


def test_BddMgr_zero():
    mgr = BddMgr()

    bdd = mgr.zero()
    assert bdd.is_zero()
    assert not bdd.is_one()
    assert bdd.is_const()
