#! /usr/bin/env python3

"""Cube の定義ファイル

:file: cube.py
:author: Yusuke Matsunaga (松永 裕介)
:Copyright: (C) 2017, 2019 Yusuke Matsunaga, All rights reserved.
"""

from logictools.bool3 import Bool3, toBool3


class Cube:
    """キューブを表すクラス

    意味的には Bool3 の列(シーケンス)
    入力数が高々10程度と仮定して符号なし整数１語で表す．
    """

    def __init__(self, arg):
        """初期化

        :param arg: パラメータ

        arg は以下の３種類のうちいずれか
        * int: 入力数を指定する．内容はすべてドントケアとなる．
        * Bool3 のリスト:
        * 文字列: 個々の文字は Bool3 に変換可能でなければならない．
        値が `Bool3._0` の要素は否定のリテラル，
        `Bool3._1` の要素は肯定のリテラルに対応する．
        `Bool3._d` の要素はこのキューブで用いられていないことを示す．
        """
        if isinstance(arg, int):
            input_num = arg
            lits = [Bool3._d for _ in range(input_num)]
        elif isinstance(arg, list) or isinstance(arg, tuple) or isinstance(arg, str):
            input_num = len(arg)
            lits = [toBool3(x) for x in arg]
        else:
            raise TypeError

        self.__input_num = input_num
        self.__body = 0
        for i in range(input_num):
            lit = lits[i]
            if lit == Bool3._0:
                self.set_negliteral(i)
            elif lit == Bool3._1:
                self.set_posliteral(i)
            elif lit == Bool3._d:
                self.clr_literal(i)
            else:
                assert False

    def set_posliteral(self, pos):
        """pos 番目の変数を正のリテラルに設定する．

        :param pos: 変数番号 ( 0 <= pos < input_num )
        """
        self[pos] = Bool3._1

    def set_negliteral(self, pos):
        """pos 番目の変数を負のリテラルに設定する．

        :param pos: 変数番号 ( 0 <= pos < input_num )
        """
        self[pos] = Bool3._0

    def clr_literal(self, pos):
        """pos 番目の変数をドントケアに設定する．

        :param pos: 変数番号 ( 0 <= pos < input_num )
        """
        self[pos] = Bool3._d

    def contain(self, other):
        """ 包含関係を調べる．"""
        other = toCube(other)
        assert self.input_num == other.input_num
        for i in range(self.input_num):
            val_a = self[i]
            val_b = other[i]
            if val_a == Bool3._1 and val_b != Bool3._1:
                return False
            elif val_a == Bool3._0 and val_b != Bool3._0:
                return False
        return True

    @property
    def input_num(self):
        """入力数を返す．"""
        return self.__input_num

    @property
    def literal_num(self):
        """リテラル数を返す．"""
        n = 0
        for i in range(self.input_num):
            if self[i] != Bool3._d:
                n += 1
        return n

    def __len__(self):
        """input_num の別名"""
        return self.__input_num

    def __getitem__(self, pos):
        """pos番目の位置のパタンを返す．

        :param pos: 位置 ( 0 <= pos < input_num )
        :retrun: Bool3._d ドントケア
                 Bool3._1 positive literal
                 Bool3._0 negative literal
        """
        assert 0 <= pos < self.input_num
        sft = self.__shift(pos)
        val = (self.__body >> sft) & 3
        if val == 0:
            return Bool3._d
        elif val == 1:
            return Bool3._1
        elif val == 2:
            return Bool3._0

    def __setitem__(self, pos, val):
        """pos 番目の変数のリテラルを設定する．

        :param pos: 変数番号 ( 0 <= pos < input_num )
        :param val: 値 ( Bool3 )
        """
        assert 0 <= pos < self.input_num
        val = toBool3(val)
        sft = self.__shift(pos)
        msk = 3 << sft
        self.__body &= ~msk
        if val == Bool3._0:
            self.__body |= (2 << sft)
        elif val == Bool3._1:
            self.__body |= (1 << sft)
        elif val == Bool3._d:
            pass
        else:
            assert False

    def __or__(self, other):
        """隣接したキューブをマージする．

        :return: 結果のキューブを返す．

        2つのキューブが隣接していなかった場合，None を返す．
        純粋な論理和ではないので注意
        """
        other = toCube(other)
        assert self.input_num == other.input_num
        nd = 0
        ans_pat = ""
        for i in range(self.input_num):
            val_a = self[i]
            val_b = other[i]
            if val_a ^ val_b == Bool3._1:
                nd += 1
                ans_pat += '-'
            elif val_a == val_b:
                if val_a == Bool3._0:
                    ans_pat += '0'
                elif val_a == Bool3._1:
                    ans_pat += '1'
                else:
                    ans_pat += '-'
            else:
                return None
        if nd == 1:
            return Cube(ans_pat)
        else:
            return None

    def __eq__(self, other):
        """等価比較演算子"""
        other = toCube(other)
        assert self.input_num == other.input_num
        for i in range(self.input_num):
            val_a = self[i]
            val_b = other[i]
            if val_a != val_b:
                return False
        return True

    def __lt__(self, other):
        """小なり比較演算子

        各入力について Bool3._d < Bool3._1 < Bool3._0
        の順で比較を行う．
        """
        return self.__comp(other) == -1

    def __gt__(self, other):
        """大なり比較演算子

        各入力について Bool3._d < Bool3._1 < Bool3._0
        の順で比較を行う．
        """
        return self.__comp(other) == 1

    def __le__(self, other):
        """小なりイコール比較演算子

        各入力について Bool3._d < Bool3._1 < Bool3._0
        の順で比較を行う．
        """
        return self.__comp(other) <= 0

    def __ge__(self, other):
        """大なりイコール比較演算子

        各入力について Bool3._d < Bool3._1 < Bool3._0
        の順で比較を行う．
        """
        return self.__comp(other) >= 0

    def __comp(self, other):
        """比較関数"""
        other = toCube(other)
        assert self.input_num == other.input_num
        for i in range(self.input_num):
            val_a = self[i]
            val_b = other[i]
            if val_a < val_b:
                return -1
            elif val_a > val_b:
                return 1
        return 0

    def __hash__(self):
        """ハッシュ関数"""
        return self.__body

    def latex_str(self, *, var_map=None):
        """内容を表すLaTex文字列を作る．

        :param var_map: 変数名の辞書(名前つきのオプション引数)
        """
        if var_map is None:
            var_map = self.__default_varmap()
        cube_str = ""
        for i in range(self.input_num):
            val = self[i]
            var = var_map[i]
            cube_str += Cube.__latex_lit(val, var)
        if cube_str == '':
            cube_str = '1'
        return cube_str

    def DeMorgan_latex_str(self, *, var_map=None):
        """DeMorgan の法則で否定した和積形論理式を表すLaTex文字列を作る．

        :param var_map: 変数名の辞書(名前付きのオプション引数)
        """
        if var_map is None:
            var_map = self.__default_varmap()
        lit_list = []
        for i in range(self.input_num):
            val = self[i]
            if val != Bool3._d:
                var = var_map[i]
                lit = Cube.__latex_lit(~val, var)
                lit_list.append(lit)
        if len(lit_list) == 0:
            return '0'

        return '(' + ' + '.join(lit_list) + ')'

    def __str__(self):
        """内容を表す文字列を作る．"""
        ans = ""
        for i in range(self.input_num):
            val = self[i]
            if val == Bool3._0:
                ans += '0'
            elif val == Bool3._1:
                ans += '1'
            elif val == Bool3._d:
                ans += '-'
        return ans

    @staticmethod
    def __latex_lit(val, var):
        """LaTeX用のリテラルを表す文字列を作る．

        :param val: 値(Bool3)
        :param var: 変数名(str)
        :return: リテラル用の文字列を返す．

        val が Bool3._d の時は空文字列を返す．
        """
        if val == Bool3._0:
            return '\\bar{{{}}}'.format(var)
        elif val == Bool3._1:
            return var
        else:
            return ''

    def __default_varmap(self):
        """デフォルトのvar_mapを作る．"""
        return {i: 'x_{}'.format(i + 1) for i in range(self.input_num)}

    def __shift(self, pos):
        """__body 中のシフト量を計算する．"""
        return (self.input_num - pos - 1) * 2


def toCube(arg):
    """Cube型へ変換する

    変換できない時は TypeError 例外を送出する．
    """
    if isinstance(arg, Cube):
        return arg
    return Cube(arg)


if __name__ == '__main__':

    c1 = Cube(4)
    print('c1 = {}: {}'.format(c1, c1.latex_str()))

    c2 = Cube('01--')
    print('c2 = {}: {}'.format(c2, c2.latex_str()))

    var_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd'}
    print('c2\' = {}'.format(c2.latex_str(var_map=var_map)))

    print('\\bar{{c2}} = {}'.format(c2.DeMorgan_latex_str()))

    c3 = Cube('-1--')
    c23 = c2 | c3
    print('c2 | c3 = {}'.format(c23))

    c4 = Cube('11--')
    c24 = c2 | c4
    print('c2 | c4 = {}'.format(c24))
