#! /usr/bin/env python3
#
# @file qm.py
# @brief Quine-McCluskey 法を実装したアルゴリズム
# @author Yusuke Matsunaga (松永 裕介)
#
# Copyright (C) 2017 Yusuke Matsunaga
# All rights reserved.

from boolfunc import BoolFunc

## @brief ２つのキューブをマージする．
# @param[in] cube1, cube2 対象のキューブ
# @return 結果のキューブを返す．
#
# cube1 と cube2 が隣接していない場合には None を返す．
# ２つのキューブの大きさは同じと仮定している．
def merge_cube(input_num, cube1, cube2) :
    ans_cube = cube1.copy()
    first = True
    for i in range(0, input_num) :
        if cube1[i] != cube2[i] :
            if first :
                # 異なっている最初の箇所を見つけた．
                # この部分をドントケアにする．
                ans_cube[i] = 0
                first = False
            else :
                # 異なっている箇所が２箇所以上あった．
                return None
    if first :
        # 異なっている箇所がなかった．
        return None
    return ans_cube

## @brief BoolFunc から minterm のリストを作る．
# @param[in] func 対象の関数
def gen_minterm_list(func) :
    nexp = 1 << func.input_num
    for p in range(0, nexp) :
        if func.val(p)
