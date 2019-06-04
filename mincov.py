#! /usr/bin/env python3

### @file mincov.py
### @brief MinCov の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019 Yusuke Matsunaga
### All rights reserved.

import sys

### @brief minimum covering を行うクラス
class MinCov :

    ### @brief 初期化
    ### @param[in] nelem 要素数
    def __init__(self, nelem) :
        self.__nelem = nelem
        self.__clause_list = []

    ### @brief 要素数を返す．
    @property
    def nelem(self) :
        return self.__nelem

    ### @brief 条件を追加する．
    def add_clause(elem_list) :
        self.__clause_list.append(elem_list)

    ### @brief 内容を表示する．
    def print(fout = None) :
        if fout == None :
            fout = sys.stdout
        for clause in self.__clause_list :
            for elem in clause :
                fout.write(' {}'.format(elem))
            fout.write('\n')


if __name__ == '__main__' :
    m = MinCov(10)
    m.add_clause( [0, 1, 2] )
    m.add_clause( [0, 4] )
    m.add_clause( [1, 3] )

    m.print()
