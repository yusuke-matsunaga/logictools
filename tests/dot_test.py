#! /usr/bin/env python3

"""

:file: dot_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

import sys
from logictools import BddMgr


mgr = BddMgr()

filename = sys.argv[1]

attr_dict = {}
attr_dict["edge0:color"] = "blue"
attr_dict["edge1:color"] = "red"
attr_dict["node:color"] = "green"
attr_dict["node:style"] = "filled"
attr_dict["terminal:style"] = "filled"
attr_dict["terminal0:color"] = "blue"
attr_dict["terminal1:color"] = "red"
with open(filename, "r") as fin:
    for line in fin:
        line = line.rstrip("\n\r")
        bdd = mgr.from_truth(line)
        bdd.gen_dot(attr_dict=attr_dict)
