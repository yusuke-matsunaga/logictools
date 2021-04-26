#! /usr/bin/env python3

"""
MinCov の実装ファイル

:file: mincov.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2019 Yusuke Matsunaga, All rights reserved.
"""

import sys


class MinCov:
    """minimum covering を行うクラス

    :param nelem: 要素数

    最小被覆問題とは要素の集合と，
    その集合の部分集合族が与えられた時に，
    すべての部分集合族について最低１つの要素を含むような
    解集合(被覆解と呼ぶ)のなかで要素数最小のものを求める問題である．

    最小被覆問題はNP困難問題であり，厳密最小解を求める効率の良いアルゴリズム
    は見つかっていない．
    ここでは小さな問題に対して解を全列挙する方式で最小解を求めている．
    """

    def __init__(self, nelem):
        self.__nelem = nelem
        self.__clause_list = []

    @property
    def nelem(self):
        """要素数を返す．"""
        return self.__nelem

    def add_clause(self, clause):
        """
        条件を追加する．

        :param clause: 追加する条件

        clause は要素のリストの形で与える．
        """
        self.__clause_list.append(clause)

    def solve(self):
        """
        最小被覆解をすべて求める．
        """
        ans_list = self.all_cover()
        min_num = self.__nelem
        # 最小解の要素数を求める．
        for ans in ans_list:
            n = len(ans)
            if min_num > n:
                min_num = n
        return [ans for ans in ans_list if len(ans) == min_num]

    def all_cover(self):
        """
        被覆解をすべて求める．
        """

        def key(clause):
            return len(clause)

        self.__clause_list.sort(key=key)
        ans_list = []
        selected = [False for i in range(self.__nelem)]
        unselected = [False for i in range(self.__nelem)]
        self.__solve_sub(0, selected, unselected, ans_list)
        return ans_list

    def __solve_sub(self, pos, selected, unselected, ans_list):
        if pos >= len(self.__clause_list):
            # 現在の選択を解に追加する．
            tmp = []
            for i in range(self.__nelem):
                if selected[i]:
                    tmp.append(i)
            ans_list.append(tmp)
            return

        clause = self.__clause_list[pos]
        sat = False
        for elem in clause:
            if selected[elem]:
                sat = True
                break
        if sat:
            # この clause は被覆されている．
            self.__solve_sub(pos + 1, selected, unselected, ans_list)
        else:
            unselected1 = list(unselected)
            for elem in clause:
                if unselected[elem]:
                    continue
                selected1 = list(selected)
                selected1[elem] = True
                self.__solve_sub(pos + 1, selected1, unselected1, ans_list)
                unselected1[elem] = True

    def print(self, fout=sys.stdout):
        """
        内容を表示する．

        :param fout: 出力先のファイルオブジェクト

        fout が省略された時は標準出力を用いる．
        """
        for clause in self.__clause_list:
            for elem in clause:
                fout.write(' {}'.format(elem))
            fout.write('\n')


if __name__ == '__main__':
    m = MinCov(5)
    m.add_clause((0, 1, 2))
    m.add_clause((0, 4))
    m.add_clause((1, 3))

    ans_list = m.solve()

    for ans in ans_list:
        print(ans)
