#! /usr/bin/env python3
#
# @file qm.py
# @brief Quine-McCluskey 法を実装したアルゴリズム
# @author Yusuke Matsunaga (松永 裕介)
#
# Copyright (C) 2017 Yusuke Matsunaga
# All rights reserved.

from lctools.cover import Cover
from lctools.mincov import MinCov


### @brief 全てのプライムインプリカントを求める．
def gen_primes(minterm_list) :
    all_cubes = set()
    used_cubes = set()
    src_list = minterm_list
    for cube in src_list :
        all_cubes.add(cube)
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
def gen_minimum_cover(onset, prime_list) :
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

    # 被覆解を求める．
    mincov = MinCov(np)
    for j in range(no) :
        for i in cover_list[j] :
            mincov.add_clause(cover_list[j])

    def compare(n1, n2, min_n1, min_n2) :
        if min_n1 > n1 :
            return -1
        elif min_n2 < n1 :
            return 1
        elif min_n2 > n2 :
            return -1
        elif min_n2 < n2 :
            return 1
        else :
            return 0

    # 最小解のみを取り出す．
    ans_list = mincov.solve()
    cover_list = []
    min_n1 = np + 1
    min_n2 = 0
    for ans in ans_list :
        cover = Cover([ prime_list[i] for i in ans ])
        n1 = cover.cube_num
        n2 = cover.literal_num
        c = compare(n1, n2, min_n1, min_n2)
        if c < 0 :
            min_n1 = n1
            min_n2 = n2
            cover_list = []
        if c <= 0 :
            cover_list.append(cover)

    return cover_list


if __name__ == '__main__' :

    f = BoolFunc(4, val_str = "10*1*****0100*01")

    f.gen_latex_table('$f$')

    # onset, dcset, offset の最小項を作る．
    onset, dcset, offset = f.gen_minterm_list()

    # 主項を求める．
    prime_list = gen_primes(onset + dcset)

    f.gen_latex_karnaugh(implicant_list = prime_list)

    cover_list = gen_minimum_cover(onset, prime_list)

    for cover in cover_list :
        print(cover.latex_str())

        print('minimum cover')
        f.gen_latex_karnaugh(implicant_list = cover.cube_list)
