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
    def add_clause(self, clause ) :
        self.__clause_list.append( clause )

    ### @brief 被覆解をすべて求める．
    def solve(self) :
        def key(clause) :
            return len(clause)
        self.__clause_list.sort(key = key)
        ans_list = []
        selected = [ False for i in range(self.__nelem) ]
        unselected = [ False for i in range(self.__nelem) ]
        self.__solve_sub(0, selected, unselected, ans_list)
        return ans_list

    def __solve_sub(self, pos, selected, unselected, ans_list) :
        if pos >= len(self.__clause_list) :
            # 現在の選択を解に追加する．
            tmp = []
            for i in range(self.__nelem) :
                if selected[i] :
                    tmp.append(i)
            ans_list.append(tmp)
            return

        clause = self.__clause_list[pos]
        sat = False
        for elem in clause :
            if selected[elem] :
                sat = True
                break
        if sat :
            # この clause は被覆されている．
            self.__solve_sub(pos + 1, selected, unselected, ans_list)
        else :
            unselected1 = list(unselected)
            for elem in clause :
                if unselected[elem] :
                    continue
                selected1 = list(selected)
                selected1[elem] = True
                self.__solve_sub(pos + 1, selected1, unselected1, ans_list)
                unselected1[elem] = True


    ### @brief 内容を表示する．
    def print(self, fout = None) :
        if fout == None :
            fout = sys.stdout
        for clause in self.__clause_list :
            for elem in clause :
                fout.write(' {}'.format(elem))
            fout.write('\n')


if __name__ == '__main__' :
    m = MinCov(5)
    m.add_clause( (0, 1, 2) )
    m.add_clause( (0, 4) )
    m.add_clause( (1, 3) )

    ans_list = m.solve()

    for ans in ans_list :
        print(ans)
