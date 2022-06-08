#! /usr/bin/env python3

"""BoolFunc の実装ファイル

:file: boolfunc.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2017, 2019, 2020 Yusuke Matsunaga, All rights reserved.
"""

import sys
from lctools.bool3 import Bool3, toBool3
from lctools.cube import Cube
import lctools.qm as qm


class BoolFunc:
    """Boolean Function を表すクラス

    * 実際には不完全指定論理関数を表すので出力値は Bool3 型となる．
    * 入力数が高々10程度と仮定して真理値表で表す．
    * 真理値表は x0, x1, x2, ... の順に並べる．
    """

    @staticmethod
    def make_const0(input_num):
        """恒偽関数を作る．

        :param input_num: 入力数

        4入力の恒偽関数を作るコード例
        ::

          f = BoolFunc.make_const0(4)
        """
        nexp = 1 << input_num
        val_list = [Bool3._0 for _ in range(nexp)]
        return BoolFunc(val_list)

    @staticmethod
    def make_const1(input_num):
        """恒真関数を作る．

        :param input_num: 入力数

        3入力の恒真関数を作るコード例
        ::

          f = BoolFunc.make_const1(3)
        """
        nexp = 1 << input_num
        val_list = [Bool3._1 for _ in range(nexp)]
        return BoolFunc(val_list)

    @staticmethod
    def make_literal(input_num, var_id):
        """リテラル関数を作る．

        :param input_num: 入力数
        :param var_id: 変数番号 ( 0 <= var_id < input_num )

        5入力の0番目の変数のりテラル関数を作るコード例
        ::

          f = BoolFunc.make_literal(5, 0)

        否定のリテラルは否定演算(~)で作る．
        """
        def val(p, var_id):
            cond = p & (1 << (input_num - var_id - 1))
            return Bool3._1 if cond else Bool3._0

        nexp = 1 << input_num
        val_list = [val(p, var_id) for p in range(0, nexp)]
        return BoolFunc(val_list)

    @staticmethod
    def make_and(input_num):
        """AND関数を作る．

        param input_num: 入力数

        4入力のAND関数を作るコード例
        ::

          f = BoolFunc.make_and(4)
        """
        nexp = 1 << input_num

        def val(p, nexp):
            if p == (nexp - 1):
                return Bool3._1
            else:
                return Bool3._0

        val_list = [val(p, nexp) for p in range(0, nexp)]
        return BoolFunc(val_list)

    @staticmethod
    def make_nand(input_num):
        """NAND関数を作る．

        :param input_num: 入力数

        4入力のNAND関数を作るコード例
        ::

          f = BoolFunc.make_nand(4)
        """
        nexp = 1 << input_num

        def val(p, nexp):
            if p == (nexp - 1):
                return Bool3._0
            else:
                return Bool3._1

        val_list = [val(p, nexp - 1) for p in range(0, nexp)]
        return BoolFunc(val_list)

    @staticmethod
    def make_or(input_num):
        """OR関数を作る．

        :param input_num: 入力数

        4入力のOR関数を作るコード例
        ::

          f = BoolFunc.make_or(4)
        """
        nexp = 1 << input_num

        def val(p, nexp):
            if p == 0:
                return Bool3._0
            else:
                return Bool3._1

        val_list = [val(p, nexp) for p in range(0, nexp)]
        return BoolFunc(val_list)

    @staticmethod
    def make_nor(input_num):
        """NOR関数を作る．

        :param input_num: 入力数

        4入力のNOR関数を作るコード例
        ::

          f = BoolFunc.make_nor(4)
        """
        nexp = 1 << input_num

        def val(p, nexp):
            if p == 0:
                return Bool3._1
            else:
                return Bool3._0

        val_list = [val(p, nexp) for p in range(0, nexp)]
        return BoolFunc(val_list)

    @staticmethod
    def make_xor(input_num):
        """XOR関数を作る．

        :param input_num: 入力数

        4入力のXOR関数を作るコード例
        ::

          f = BoolFunc.make_xor(4)
        """
        def parity(p, input_num):
            c = 0
            for i in range(0, input_num):
                if p & (1 << i):
                    c += 1
            if (c % 2) == 1:
                return Bool3._1
            else:
                return Bool3._0

        nexp = 1 << input_num
        val_list = [parity(p, input_num) for p in range(0, nexp)]
        return BoolFunc(val_list)

    @staticmethod
    def make_xnor(input_num):
        """XNOR関数を作る．

        :param input_num: 入力数

        4入力のXNOR関数を作るコード例
        ::

          f = BoolFunc.make_xnor(4)
        """
        def parity(p, input_num):
            c = 0
            for i in range(0, input_num):
                if p & (1 << i):
                    c += 1
            if (c % 2) == 0:
                return Bool3._1
            else:
                return Bool3._0

        nexp = 1 << input_num
        val_list = [parity(p, input_num) for p in range(0, nexp)]
        return BoolFunc(val_list)

    @staticmethod
    def make_from_string(expr_string, input_num, var_map):
        """論理式を表す文字列から関数を作る．

        :param expr_string: 論理式を表す文字列
        :param input_numm: 入力数
        :param var_map: 変数名の辞書
        """
        from lctools.parser import Parser

        parser = Parser(input_num, var_map)
        f = parser(expr_string)
        if not f:
            parser.print_emsg()
        return f

    def __init__(self, arg):
        """初期化

        :param arg: 入力パラメータ

        * arg には Bool3 のリスト(シーケンス)か文字列を指定する．
        * リストの長さは 2^input_num でなければならない(input_numは入力数)．
        * 文字列の長さは 2^input_num でなければならない(input_numは入力数)．
        * 文字列の個々の文字は Bool3 へ変換可能でなければならない．
        """
        if isinstance(arg, list) or isinstance(arg, tuple) or isinstance(arg, str):
            val_list = [toBool3(x) for x in arg]
        else:
            raise TypeError()

        # 入力数を求める．
        input_num = 0
        n = len(val_list)
        while True:
            nexp = 1 << input_num
            if nexp == n:
                break
            if nexp > n:
                raise
            input_num += 1

        self.__input_num = input_num
        self.__tv_list = val_list

    @property
    def input_num(self):
        """入力数を返す．"""
        return self.__input_num

    def val(self, ival_list):
        """入力値に対する出力値を返す．

        :param ival_list: 入力値のリスト
        """
        assert len(ival_list) == self.input_num
        pos = 0
        for i in range(0, self.input_num):
            if ival_list[i] == Bool3._1:
                pos += (1 << (self.input_num - i - 1))
        return self.__tv_list[pos]

    def __invert__(self):
        """not演算子

        :return: self の否定を表す論理関数を返す．

        使用例
        ::

          # f は BoolFunc オブジェクト
          g = ~f
        """
        return BoolFunc([~v for v in self.__tv_list])

    def __and__(self, other):
        """AND演算子

        :param other: 他方のオペランド
        :return: self と other の論理積を表す関数を返す．

        other.input_num は self.input_num と等しくなければならない．

        使用例
        ::

          # f1, f2 は BoolFunc オブジェクト
          g = f1 & f2
        """
        other = toBoolFunc(other)
        assert self.input_num == other.__input_num
        return BoolFunc([v1 & v2 for v1, v2 in zip(self.__tv_list,
                                                   other.__tv_list)])

    def __or__(self, other):
        """OR演算子

        :param other: 他方のオペランド
        :return: self と other の論理和を表す関数を返す．

        other.input_num は self.input_num と等しくなければならない．

        ::

          # f1, f2 は BoolFunc オブジェクト
          g = f1 | f2
        """
        other = toBoolFunc(other)
        assert self.input_num == other.__input_num
        return BoolFunc([v1 | v2 for v1, v2 in zip(self.__tv_list,
                                                   other.__tv_list)])

    def __xor__(self, other):
        """XOR演算子

        :param other: 他方のオペランド
        :return: self と other の排他的論理和を表す関数を返す．

        other.input_num は self.input_num と等しくなければならない．

        ::

          # f1, f2 は BoolFunc オブジェクト
          g = f1 ^ f2
        """
        other = toBoolFunc(other)
        assert self.input_num == other.__input_num
        return BoolFunc([v1 ^ v2 for v1, v2 in zip(self.__tv_list,
                                                   other.__tv_list)])

    def compose(self, ifunc_list):
        """compose 演算

        :param ifunc_list: 入力関数のリスト
        :return: 個々の入力を ifunc_list の要素に置き換えた関数を返す．

        - self は完全指定関数でなければならない．
        - ifunc_list の要素数は self.input_num と等しくなければならない．
        - ifunc_list の関数は全て同じ入力数でなければならない．
        """
        assert len(ifunc_list) == self.input_num
        ifunc_list - [toBoolFunc(ifunc) for ifunc in ifunc_list]

        if self.input_num == 0:
            # 0 入力関数の場合は置き換える変数がない．
            return BoolFunc(self.__tv_list)

        # 新しい関数の入力数をチェックする．
        new_ni = ifunc_list[0].input_num
        for i in range(1, self.input_num):
            ifunc = ifunc_list[i]
            assert ifunc.input_num == new_ni

        # 最初は恒偽関数に初期化しておく．
        ans = BoolFunc.make_const0(new_ni)
        nexp = 1 << self.input_num
        for p in range(0, nexp):
            if self.__tv_list[p] == Bool3._1:
                p_func = BoolFunc.make_const1(new_ni)
                for i in range(0, self.input_num):
                    if p & (1 << (self.input_num - i - 1)):
                        p_func &= ifunc_list[i]
                    else:
                        p_func &= ~ifunc_list[i]
                ans |= p_func
        return ans

    def __eq__(self, other):
        """等価比較演算子

        :param other: 他方のオペランド
        :return: self と other が同じ関数の時 True を返す．

        ::

          # f1, f2 は BoolFunc オブジェクト
          if f1 == f2:
             ...

        という風に使う．
        """
        other = toBoolFunc(other)
        assert self.input_num == other.input_num

        for v1, v2 in zip(self.__tv_list, other.__tv_list):
            if v1 != v2:
                return False
        return True

    def gen_minterm_list(self):
        """BoolFunc から onset, dcset, offset の最小項のリストを作る．"""
        nexp = 1 << self.input_num
        onset = []
        dcset = []
        offset = []
        for p in range(0, nexp):
            minterm = Cube(self.input_num)
            ival_list = []
            for i in range(self.input_num):
                if p & (1 << i):
                    ival = Bool3._1
                else:
                    ival = Bool3._0
                minterm[i] = ival
                ival_list.append(ival)
            oval = self.val(ival_list)
            if oval == Bool3._1:
                onset.append(minterm)
            elif oval == Bool3._d:
                dcset.append(minterm)
            elif oval == Bool3._0:
                offset.append(minterm)
        return onset, dcset, offset

    @staticmethod
    def gen_primes(onset):
        """オンセットから主項のリストを作る．

        :param list[Cube] onset: オンセットを表す最小項の Cube のリスト
        :return: 主項の Cube のリストを返す．

        対象が不完全指定論理関数の場合には onset にドントケアセットも含める必要がある．
        """
        return qm.gen_primes(onset)

    def gen_minimum_cover(self):
        """最簡積和形論理式を返す．
        :return: 最簡積和形論理式を表す Cover のリストを返す．

        最簡形が一つしかない場合でも結果はリストの形で返される．
        """

        on, dc, off = self.gen_minterm_list()
        primes = qm.gen_primes(on + dc)
        return qm.gen_minimum_cover(on, primes)

    def print_table(self, *, var_map=None, fout=sys.stdout):
        """真理値表の形式で出力する．

        :param var_map: 変数名の辞書(名前付きパラメータ)
        :param fout: 出力先のファイルオブジェクト(名前付きパラメータ)

        fout を省略した場合には標準出力が用いられる．
        """
        var_map = self.__default_var_map(var_map)

        nexp = 1 << self.input_num

        # ヘッダの出力
        for i in range(0, self.input_num):
            fout.write(' {:3}'.format(var_map[i]))
        fout.write('| f\n')
        for i in range(0, self.input_num):
            fout.write('----')
        fout.write('+--\n')

        # 中身の出力
        for p in range(0, nexp):
            for i in range(0, self.input_num):
                ival = '1' if p & (1 << (self.input_num - i - 1)) else '0'
                fout.write('  {:1} '.format(ival))
            oval = self.__tv_list[p]
            fout.write('| {:1}\n'.format(oval))

    def print_karnaugh(self, *, var_map=None, fout=sys.stdout):
        """カルノー図の形式で出力する．

        :param var_map: 変数名の辞書(名前付きのオプション引数)
        :param fout: 出力先のファイルオブジェクト(名前付きのオプション引数)

        4入力関数まで対応している．

        fout を省略した場合には標準出力が用いられる．
        """
        from lctools.karnaugh import karnaugh0, karnaugh1
        from lctools.karnaugh import karnaugh2, karnaugh3, karnaugh4

        var_map = self.__default_var_map(var_map)

        if self.input_num == 0:
            karnaugh0(self, var_map, fout)
        elif self.input_num == 1:
            karnaugh1(self, var_map, fout)
        elif self.input_num == 2:
            karnaugh2(self, var_map, fout)
        elif self.input_num == 3:
            karnaugh3(self, var_map, fout)
        elif self.input_num == 4:
            karnaugh4(self, var_map, fout)
        else:
            fout.write('Too many inputs.\n')

    def gen_latex_minterm_sop(self, *, var_map=None, fout=sys.stdout):
        """積和標準形をLaTex形式で出力する．

        :param varmap: 変数名の辞書(名前付きのオプション引数)
        :param fout: 出力先のファイルオブジェクト(名前付きのオプション引数)

        fout を省略した場合には標準出力が用いられる．
        """
        var_map = self.__default_var_map(var_map)

        nexp = 1 << self.input_num

        sop = ""
        plus = ""
        for p in range(0, nexp):
            if self.__tv_list[p] == Bool3._1:
                term = ""
                for i in range(0, self.input_num):
                    if p & (1 << (self.input_num - i - 1)):
                        term += "{}".format(var_map[i])
                    else:
                        term += "\\bar{{{}}}".format(var_map[i])
                sop += plus + term
                plus = " + "
        sop += "\n"
        fout.write(sop)

    def gen_latex_maxterm_pos(self, *, var_map=None, fout=sys.stdout):
        """和積標準形をLaTex形式で出力する．

        :param varmap: 変数名の辞書(名前付きのオプション引数)
        :param fout: 出力先のファイルオブジェクト(名前付きのオプション引数)

        fout を省略した場合には標準出力が用いられる．
        """
        var_map = self.__default_var_map(var_map)

        nexp = 1 << self.input_num

        pos = ""
        for p in range(0, nexp):
            if self.__tv_list[p] == Bool3._0:
                term = "("
                plus = ""
                for i in range(0, self.input_num):
                    if p & (1 << (self.input_num - i - 1)):
                        term += plus + "\\bar{{{}}}".format(var_map[i])
                    else:
                        term += plus + "{}".format(var_map[i])
                    plus = " + "
                term += ")"
                pos += term
        pos += "\n"
        fout.write(pos)

    def gen_latex_table(self, fname, *, var_map=None, fout=sys.stdout):
        """真理値表をLaTex形式で出力する．

        :param fname: 関数名
        :param var_map: 変数名の辞書(名前付きオプションパラメータ)
        :param fout: 出力先のファイルオブジェクト(名前付きオプションパラメータ)

        fout を省略した場合には標準出力が用いられる．
        """
        var_map = self.__default_var_map(var_map)

        nexp = 1 << self.input_num

        # ヘッダの出力
        fout.write('\\begin{tabular}{|')
        fout.write('c' * self.input_num)
        fout.write('|c|}\n')
        fout.write('\\hline\n')
        for i in range(0, self.input_num):
            fout.write('${}$ & '.format(var_map[i]))
        fout.write(' ${}$\\\\\n'.format(fname))
        fout.write('\\hline \\hline\n')

        # 中身の出力
        for p in range(0, nexp):
            for i in range(0, self.input_num):
                ival = '1' if p & (1 << (self.input_num - i - 1)) else '0'
                fout.write('{} & '.format(ival))
            v = self.__tv_list[p]
            if v == Bool3._1:
                oval = '1'
            elif v == Bool3._0:
                oval = '0'
            elif v == Bool3._d:
                oval = '$\\ast$'
            else:
                assert False
            fout.write('{}\\\\\n'.format(oval))

        # フッタの出力
        fout.write('\\hline\n')
        fout.write('\\end{tabular}\n')

    @staticmethod
    def gen_latex_tables(func_list, fname_list, *,
                         var_map=None,
                         fout=sys.stdout):
        """複数の関数を表す真理値表を LaTeX 形式で出力する．

        :param func_list: 関数のリスト
        :param fname_list: 関数名のリスト
        :param var_map: 変数名の辞書(名前付きオプションパラメータ)
        :param fout: 出力先のファイルオブジェクト(名前付きオプションパラメータ)

        * func_list は最低1つは要素を持たなければならない．
        * fname_list の要素数は func_list の要素数と同じでなければならない．
        * fout を省略した場合には標準出力が用いられる．
        """
        nf = len(func_list)
        assert nf > 0
        assert len(fname_list) == nf

        ni = func_list[0].input_num
        for f in func_list:
            assert f.input_num == ni

        var_map = func_list[0].__default_var_map(var_map)

        nexp = 1 << ni

        # ヘッダの出力
        fout.write('\\begin{tabular}{|')
        fout.write('c' * ni)
        fout.write('|')
        fout.write('c' * nf)
        fout.write('|}\n')
        fout.write('\\hline\n')
        for i in range(0, ni):
            fout.write('${}$ & '.format(var_map[i]))
        for i in range(0, nf):
            fout.write(' ${}$'.format(fname_list[i]))
            if i < (nf - 1):
                fout.write(' & ')
        fout.write('\\\\\n')
        fout.write('\\hline \\hline\n')

        def oval_str(val):
            if val == Bool3._1:
                return '1'
            elif v == Bool3._0:
                return '0'
            elif v == Bool3._d:
                return '$\\ast$'
            else:
                assert False
            return None

        # 中身の出力
        for p in range(0, nexp):
            for i in range(0, ni):
                ival = '1' if p & (1 << (ni - i - 1)) else '0'
                fout.write('{} & '.format(ival))
            for i in range(0, nf):
                v = func_list[i].__tv_list[p]
                oval = oval_str(v)
                fout.write('{}'.format(oval))
                if i < (nf - 1):
                    fout.write(' & ')
            fout.write('\\\\\n')

        # フッタの出力
        fout.write('\\hline\n')
        fout.write('\\end{tabular}\n')

    def gen_latex_karnaugh(self, *,
                           implicant_list=None,
                           var_map=None, fout=sys.stdout):
        """カルノー図をLaTex形式で出力する．

        :param implicant_list: インプリカントのリスト(名前付きオプション引数)
        :param var_map: 変数名の辞書(名前付きオプション引数)
        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout を省略した場合には標準出力が用いられる．
        """
        from lctools.latex_karnaugh import latex_karnaugh

        var_map = self.__default_var_map(var_map)

        latex_karnaugh(self, implicant_list, var_map, fout)

    def gen_dpic_hypercube(self, *,
                           var_map=None,
                           fout=sys.stdout):
        """幾何学表現（ハイパーキューブ）用のdpicソースを出力する．

        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout を省略した場合には標準出力が用いられる．
        """
        from lctools.dpic_hc import dpic_hc

        var_map = self.__default_var_map(var_map)

        dpic_hc(self, var_map=var_map, fout=fout)

    def __default_var_map(self, var_map):
        """デフォルトのvar_mapを作る．"""
        if var_map is None:
            return {i: 'x_{}'.format(i + 1) for i in range(self.input_num)}
        else:
            return var_map


def toBoolFunc(arg):
    """BoolFunc型へ変換する．

    :param arg: 入力パラメータ
    :return: BoolFunc のオブジェクトを返す．

    arg が BooleFunc 以外の型の場合にはリストか文字列から
    BoolFunc型へ変換する．
    """
    if isinstance(arg, BoolFunc):
        return arg
    return toBoolFunc(arg)


if __name__ == '__main__':

    import sys
    import os
    sys.path.append(os.pardir)

    def print_func(f, f_name, f_desc):
        var_map = {0: 'x_0',
                   1: 'x_1',
                   2: 'x_2',
                   3: 'x_3'}
        print('{} = {}'.format(f_name, f_desc))
        print('')
        print('{}.print_table()'.format(f_name))
        f.print_table()
        print('')
        print('{}.print_karnaugh()'.format(f_name))
        f.print_karnaugh()
        print('')
        print('{}.gen_latex_table()'.format(f_name))
        f.gen_latex_table(f_name, var_map=var_map)
        print('')
        print('{}.gen_latex_karnaugh()'.format(f_name))
        f.gen_latex_karnaugh(var_map=var_map)
        print('')

    f0 = BoolFunc.make_const0(0)
    print_func(f0, 'f0', 'make_const0(0)')

    f1 = BoolFunc.make_const1(2)
    print_func(f1, 'f1', 'make_const1(2)')

    f3 = BoolFunc.make_and(3)
    print_func(f3, 'f3', 'make_and(3)')

    f4 = BoolFunc.make_or(4)
    print_func(f4, 'f4', 'make_or(4)')

    f5 = BoolFunc.make_xor(4)
    print_func(f5, 'f5', 'make_xor(4)')

    f6 = BoolFunc.make_literal(4, 2)
    print_func(f6, 'f6', 'make_literal(4, 2)')

    f7 = f5 & f6
    print_func(f7, 'f7', 'f5 & f6')

    f8 = f5 | f6
    print_func(f8, 'f8', 'f5 | f6')

    f9 = f5 ^ f6
    print_func(f9, 'f9', 'f5 ^ f6')

    f10 = f4
    f10 &= f7
    print_func(f10, 'f10', 'f4 &= f7')

    f11 = f4
    f11 |= f7
    print_func(f11, 'f11', 'f4 |= f7')

    f12 = f4
    f12 ^= f7
    print_func(f12, 'f12', 'f4 ^= f7')

    f13 = ~f3
    print_func(f13, 'f13', '~f3')

    BoolFunc.gen_latex_tables([f10, f11, f12], ['f10', 'f11', 'f12'])
