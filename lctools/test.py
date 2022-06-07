#! /usr/bin/env python3

"""

:file: test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

from lctools import BoolFunc

expr_str = "x & y | ~z & ~w"
var_map = {0: 'x', 1: 'y', 2: 'z', 3: 'w'}
f = BoolFunc.make_from_string(expr_str, 4, var_map)

if f:
    f.print_table()
