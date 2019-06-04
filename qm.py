#! /usr/bin/env python3
#
# @file qm.py
# @brief Quine-McCluskey 法を実装したアルゴリズム
# @author Yusuke Matsunaga (松永 裕介)
#
# Copyright (C) 2017 Yusuke Matsunaga
# All rights reserved.

from bool3 import Bool3
from boolfunc import BoolFunc
from cube import Cube

### @brief BoolFunc から onset, dcset, offset のリストを作る．
### @param[in] func 対象の関数
def gen_minterm_list(func) :
    nexp = 1 << func.input_num
    onset = []
    dcset = []
    offset = []
    for p in range(0, nexp) :
        minterm = Cube(input_num = func.input_num)
        ival_list = []
        for i in range(func.input_num) :
            if p & (1 << i) :
                ival = Bool3._1
            else :
                ival = Bool3._0
            minterm[i] = ival
            ival_list.append(ival)
        oval = func.val(ival_list)
        if oval == Bool3._1 :
            onset.append(minterm)
        elif oval == Bool3._d :
            dcset.append(minterm)
        elif oval == Bool3._0 :
            offset.append(minterm)

    return onset, dcset, offset


### @brief 全てのプライムインプリカントを求める．
def gen_primes(onset, dcset) :
    all_cubes = set()
    used_cubes = set()
    src_list = onset + dcset
    while True :
        n = len(src_list)
        dst_list = []
        for i1 in range(n - 1) :
            cube1 = src_list[i1]
            for i2 in range(i1 + 1, n) :
                cube2 = src_list[i2]
                new_cube = cube1 | cube2
                if new_cube :
                    used_cubes.add(cube1)
                    used_cubes.add(cube2)
                    if new_cube not in all_cubes :
                        all_cubes.add(new_cube)
                        dst_list.append(new_cube)
        if dst_list == [] :
            break
        src_list = dst_list

    primes = [ cube for cube in all_cubes if cube not in used_cubes ]
    primes.sort()
    return primes


### @brief 最簡積和形論理式を求める．
def gen_minimum_cover(func) :
    # onset, dcset, offset の最小項を作る．
    onset, dcset, offset = gen_minterm_list(func)

    # 主項を求める．
    prime_list = gen_primes(onset, dcset)

    # 各主項がカバーする最小項を求める．
    np = len(prime_list)
    minterm_list = [ [] for i in range(np) ]
    no = len(onset)
    cover_list = [ [] for i in range(no) ]
    for i in range(np) :
        prime = prime_list[i]

        for j in range(no) :
            minterm = onset[j]
            if prime.contain(minterm) :
                minterm_list[i].append(j)
                cover_list[j].append(i)

    # 必須主項を求める．
    essential_primes = []
    for j in range(no) :
        if len(cover_list[i]) == 1 :
            i = cover_list[i][0]
            if i not in essential_primes :
                essential_primes.append(i)

    # 被覆表
    for i in range(np) :
        prime = prime_list[i]
        print('{}:'.format(prime), end = '')
        for j in minterm_list[i] :
            print(' {}'.format(j), end = '')
        print('')

    for j in range(no) :
        print('m{}:'.format(j), end = '')
        for i in cover_list[j] :
            print(' {}'.format(i), end = '')
        print('')


if __name__ == '__main__' :

    f = BoolFunc(4, val_str = "10*1*****0100*01")

    gen_minimum_cover(f)
