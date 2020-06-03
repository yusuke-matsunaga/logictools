#! /usr/bin/env python3

### @file boolfunc.py
### @brief BoolFunc の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2017, 2019 Yusuke Matsunaga
### All rights reserved.

import sys
from lctools.bool3 import Bool3
from lctools.cube import Cube

### @class BoolFunc
### @brief Boolean Function を表すクラス
###
### * 実際には不完全指定論理関数を表すので出力値は Bool3 型となる．
### * 入力数が高々10程度と仮定して真理値表で表す．
### * 変数名のリストを持つ．
class BoolFunc :

    ### @brief 恒偽関数を作る．
    ### @param[in] input_num 入力数
    ###
    ### 4入力の恒偽関数を作るコード
    ### @code
    ### f = BoolFunc.make_const0(4)
    ### @endcode
    @staticmethod
    def make_const0(input_num) :
        return BoolFunc(input_num)

    ### @brief 恒真関数を作る．
    ### @param[in] input_num 入力数
    ### @param[in] var_map 変数名の辞書
    ###
    ### 3入力の恒真関数を作るコード
    ### @code
    ### f = BoolFunc.make_const1(3)
    ### @endcode
    @staticmethod
    def make_const1(input_num, *, var_map = None) :
        nexp = 1 << input_num
        return BoolFunc(input_num,
                        val_list = [ Bool3._1 for i in range(0, nexp)],
                        var_map = var_map)

    ### @brief リテラル関数を作る．
    ### @param[in] input_num
    ### @param[in] var_id 変数番号 ( 0 <= var_id < input_num )
    ### @param[in] var_map 変数名の辞書
    ###
    ### 5入力の0番目の変数のりテラル関数を作るコード
    ### @code
    ### f = BoolFunc.make_literal(5, 0)
    ### @endcode
    ###
    ### 否定のリテラルは否定演算(~)で作る．
    @staticmethod
    def make_literal(input_num, var_id, *, var_map = None) :
        def val(p, var_id) :
            return Bool3._1 if p & (1 << (input_num - var_id - 1)) else Bool3._0
        nexp = 1 << input_num
        return BoolFunc(input_num,
                        val_list = [ val(p, var_id) for p in range(0, nexp)],
                        var_map = var_map)

    ### @brief AND関数を作る．
    ### @param[in] input_num 入力数
    ### @param[in] var_map 変数名の辞書
    ###
    ### 4入力のAND関数を作るコード
    ### @code
    ### f = BoolFunc.make_and(4)
    ### @endcode
    @staticmethod
    def make_and(input_num, *, var_map = None) :
        nexp = 1 << input_num
        def val(p, nexp) :
            if p == (nexp - 1) :
                return Bool3._1
            else :
                return Bool3._0
        return BoolFunc(input_num,
                        val_list = [ val(p, nexp) for p in range(0, nexp)],
                        var_map = var_map)

    ### @brief NAND関数を作る．
    ### @param[in] input_num 入力数
    ### @param[in] var_map 変数名の辞書
    ###
    ### 4入力のNAND関数を作るコード
    ### @code
    ### f = BoolFunc.make_nand(4)
    ### @endcode
    @staticmethod
    def make_nand(input_num, *, var_map = None) :
        nexp = 1 << input_num
        def val(p, nexp) :
            if p == (nexp - 1) :
                return Bool3._0
            else :
                return Bool3._1
        return BoolFunc(input_num,
                        val_list = [ val(p, nexp - 1) for p in range(0, nexp)],
                        var_map = var_map)

    ### @brief OR関数を作る．
    ### @param[in] input_num 入力数
    ### @param[in] var_map 変数名の辞書
    ###
    ### 4入力のOR関数を作るコード
    ### @code
    ### f = BoolFunc.make_or(4)
    ### @endcode
    @staticmethod
    def make_or(input_num, *, var_map = None) :
        nexp = 1 << input_num
        def val(p, nexp) :
            if p == 0 :
                return Bool3._0
            else :
                return Bool3._1
        return BoolFunc(input_num,
                        val_list = [ val(p, nexp) for p in range(0, nexp)],
                        var_map = var_map)

    ### @brief NOR関数を作る．
    ### @param[in] input_num 入力数
    ### @param[in] var_map 変数名の辞書
    ###
    ### 4入力のNOR関数を作るコード
    ### @code
    ### f = BoolFunc.make_nor(4)
    ### @endcode
    @staticmethod
    def make_nor(input_num, *, var_map = None) :
        nexp = 1 << input_num
        def val(p, nexp) :
            if p == 0 :
                return Bool3._1
            else :
                return Bool3._0
        return BoolFunc(input_num,
                        val_list = [ val(p, nexp) for p in range(0, nexp)],
                        var_map = var_map)

    ### @brief XOR関数を作る．
    ### @param[in] input_num 入力数
    ### @param[in] var_map 変数名の辞書
    ###
    ### 4入力のXOR関数を作るコード
    ### @code
    ### f = BoolFunc.make_xor(4)
    ### @endcode
    @staticmethod
    def make_xor(input_num, *, var_map = None) :
        def parity(p, input_num) :
            c = 0
            for i in range(0, input_num) :
                if p & (1 << i) :
                    c += 1
            if (c % 2) == 1 :
                return Bool3._1
            else :
                return Bool3._0
        nexp = 1 << input_num
        return BoolFunc(input_num,
                        val_list = [ parity(p, input_num) for p in range(0, nexp) ],
                        var_map = var_map)

    ### @brief XNOR関数を作る．
    ### @param[in] input_num 入力数
    ### @param[in] var_map 変数名の辞書
    ###
    ### 4入力のXNOR関数を作るコード
    ### @code
    ### f = BoolFunc.make_xnor(4)
    ### @endcode
    @staticmethod
    def make_xor(input_num, *, var_map = None) :
        def parity(p, input_num) :
            c = 0
            for i in range(0, input_num) :
                if p & (1 << i) :
                    c += 1
            if (c % 2) == 0 :
                return Bool3._1
            else :
                return Bool3._0
        nexp = 1 << input_num
        return BoolFunc(input_num,
                        val_list = [ parity(p, input_num) for p in range(0, nexp) ],
                        var_map = var_map)

    ### @brief 初期化
    ### @param[in] input_num 入力数
    ### @param[in] val_list 値のリスト
    ### @param[in] val_str 値のリストを表す文字列
    ### @param[in] var_map 変数名の辞書
    ###
    ### * val_list と val_str はどちらか一方しか指定できない．
    ### * val_list と val_str が両方とも省略された場合には恒偽関数となる．
    ### * val_list の長さは 2^input_num でなければならない．
    ### * val_str の長さは 2^input_num でなければならない．
    ### * val_str で使える文字は'0', '1', '*', 'd', '-'
    def __init__(self, input_num, *, val_list = None, val_str = None, var_map = None) :
        assert val_list == None or val_str == None
        self.__input_num = input_num
        nexp = 1 << input_num

        # 真理値表のテーブル(0, 1, dのリスト)を作る．
        if val_list :
            assert len(val_list) == nexp
            self.__tv_list = list(val_list)
        elif val_str :
            assert len(val_str) == nexp
            def val(val_str, p) :
                pat = val_str[p]
                if pat == '0' :
                    return Bool3._0
                elif pat == '1' :
                    return Bool3._1
                elif pat == '*' or pat == '-' or pat == 'd' :
                    return Bool3._d
                else :
                    assert False
            self.__tv_list = [ val(val_str, p) for p in range(0, nexp) ]
        else :
            self.__tv_list = [ Bool3._0 for p in range(0, nexp)]

        # 変数名マップを作る．
        if var_map :
            self.__var_map = {i : var_map[i] for i in range(0, input_num)}
        else :
            # デフォルトの変数名マップを作る．
            self.__var_map = {i : 'x_{}'.format(i + 1) for i in range(0, input_num)}

    ### @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ### @brief 入力変数名を返す
    ### @param[in] pos 変数番号 ( 0 <= pos < input_num )．
    def input_var(self, pos) :
        assert 0 <= pos < self.input_num
        return self.__var_map[pos]

    ### @brief 入力値に対する出力値を返す．
    ### @param[in] ival_list 入力値のリスト
    def val(self, ival_list) :
        assert len(ival_list) == self.input_num
        pos = 0
        for i in range(0, self.input_num) :
            if ival_list[i] == Bool3._1 :
                pos += (1 << (self.input_num - i - 1))
        return self.__tv_list[pos]

    ### @brief 変数名の辞書を返す．
    @property
    def var_map(self) :
        return self.__var_map

    ### @brief 自身の否定を返す単項演算子
    ###
    ### @code
    ### f = BoolFunc(n) # n は入力数
    ### ...
    ### g = ~f
    ### @endcode
    ### という風に使う．
    def __invert__(self) :
        return BoolFunc(self.input_num,
                        val_list = [ ~v for v in self.__tv_list],
                        var_map = self.__var_map)

    ### @brief AND演算子
    ###
    ### @code
    ### f1 = BoolFunc() # 本当は入力数が必要
    ### f2 = BoolFunc() # 本当は入力数が必要
    ### g = f1 & f2
    ### @endcode
    ### という風に使う．
    def __and__(self, other) :
        def val(f1, f2, p) :
            ival1 = f1.__tv_list[p]
            ival2 = f2.__tv_list[p]
            return ival1 & ival2
        assert self.input_num == other.__input_num
        nexp = 1 << self.input_num
        return BoolFunc(self.input_num,
                        val_list = [ val(self, other, p) for p in range(0, nexp)],
                        var_map = self.__var_map)

    ### @brief OR演算子
    ###
    ### @code
    ### f1 = BoolFunc() # 本当は入力数が必要
    ### f2 = BoolFunc() # 本当は入力数が必要
    ### g = f1 | f2
    ### @endcode
    ### という風に使う．
    def __or__(self, other) :
        def val(f1, f2, p) :
            ival1 = f1.__tv_list[p]
            ival2 = f2.__tv_list[p]
            return ival1 | ival2
        assert self.input_num == other.__input_num
        nexp = 1 << self.input_num
        return BoolFunc(self.input_num,
                        val_list = [ val(self, other, p) for p in range(0, nexp)],
                        var_map = self.__var_map)

    ### @brief XOR演算子
    ###
    ### @code
    ### f1 = BoolFunc() # 本当は入力数が必要
    ### f2 = BoolFunc() # 本当は入力数が必要
    ### g = f1 ^ f2
    ### @endcode
    ### という風に使う．
    def __xor__(self, other) :
        def val(f1, f2, p) :
            ival1 = f1.__tv_list[p]
            ival2 = f2.__tv_list[p]
            return ival1 ^ ival2
        assert self.input_num == other.__input_num
        nexp = 1 << self.input_num
        return BoolFunc(self.input_num,
                        val_list = [ val(self, other, p) for p in range(0, nexp)],
                        var_map = self.__var_map)

    ### @brief compose 演算
    ### @param[in] ifunc_list 入力関数のリスト
    ###
    ### - 個々の入力を ifunc_list の要素に置き換えた関数を作る．
    ### - self は完全指定関数でなければならない．
    ### - ifunc_list の要素数は self.input_num と等しくなければならない．
    ### - ifunc_list の関数は全て同じ入力数でなければならない．
    def compose(self, ifunc_list) :
        assert len(ifunc_list) == self.input_num

        if self.input_num == 0 :
            # 0 入力関数の場合は置き換える変数がない．
            return BoolFunc(0, val_list = self.__tv_list, var_map = self.__var_map)

        # 新しい関数の入力数をチェックする．
        new_ni = ifunc_list[0].input_num
        for i in range(1, self.input_num) :
            ifunc = ifunc_list[i]
            assert ifunc.input_num == new_ni

        # 最初は恒偽関数に初期化しておく．
        ans = BoolFunc.make_const0(new_ni)
        nexp = 1 << self.input_num
        for p in range(0, nexp) :
            if self.__tv_list[p] == Bool3._1 :
                p_func = BoolFunc.make_const1(new_ni)
                for i in range(0, self.input_num) :
                    if p & (1 << (self.input_num - i - 1)) :
                        p_func &= ifunc_list[i]
                    else :
                        p_func &= ~ifunc_list[i]
                ans |= p_func
        return ans

    ### @brief 等価比較演算子
    ###
    ### @code
    ### f1 = BoolFunc() # 本当は入力数が必要
    ### f2 = BoolFunc() # 本当は入力数が必要
    ### if f1 == f2 :
    ###    ...
    ### @endcode
    ### という風に使う．
    def __eq__(self, other) :
        assert self.input_num == other.input_num

        nexp = 1 << self.input_num
        for p in range(0, nexp) :
            if self.__tv_list[p] != other.__tv_list[p] :
                return False
        return True

    ### @brief BoolFunc から onset, dcset, offset のリストを作る．
    def gen_minterm_list(self) :
        nexp = 1 << self.input_num
        onset = []
        dcset = []
        offset = []
        for p in range(0, nexp) :
            minterm = Cube(input_num = self.input_num)
            ival_list = []
            for i in range(self.input_num) :
                if p & (1 << i) :
                    ival = Bool3._1
                else :
                    ival = Bool3._0
                minterm[i] = ival
                ival_list.append(ival)
            oval = self.val(ival_list)
            if oval == Bool3._1 :
                onset.append(minterm)
            elif oval == Bool3._d :
                dcset.append(minterm)
            elif oval == Bool3._0 :
                offset.append(minterm)

        return onset, dcset, offset

    ### @brief 真理値表の形式で出力する．
    ### @param[in] var_map 変数名の辞書
    ### @param[in] fout 出力先のファイルオブジェクト
    def print_table(self, *, var_map = None, fout = None) :
        if var_map == None :
            var_map = self.__var_map

        if fout == None :
            fout = sys.stdout

        nexp = 1 << self.input_num

        # ヘッダの出力
        for i in range(0, self.input_num) :
            fout.write(' {:3}'.format(var_map[i]))
        fout.write('| f\n')
        for i in range(0, self.input_num) :
            fout.write('----')
        fout.write('+--\n')

        # 中身の出力
        for p in range(0, nexp) :
            for i in range(0, self.input_num) :
                ival = '1' if p & (1 << (self.input_num - i - 1)) else '0'
                fout.write('  {:1} '.format(ival))
            oval = self.__tv_list[p]
            fout.write('| {:1}\n'.format(oval))

    ### @brief カルノー図の形式で出力する．
    ### @param[in] var_map 変数名の辞書
    ### @param[in] fout 出力先のファイルオブジェクト
    ###
    ### 4入力関数まで対応している．
    def print_karnaugh(self, *, var_map = None, fout = None) :
        if var_map == None :
            var_map = self.__var_map

        if fout == None :
            fout = sys.stdout

        if self.input_num == 0 :
            self.__karnaugh0(var_map, fout)
        elif self.input_num == 1 :
            self.__karnaugh1(var_map, fout)
        elif self.input_num == 2 :
            self.__karnaugh2(var_map, fout)
        elif self.input_num == 3 :
            self.__karnaugh3(var_map, fout)
        elif self.input_num == 4 :
            self.__karnaugh4(var_map, fout)
        else :
            fout.write('Too many inputs.\n')

    ### @brief 0変数のカルノー図を出力する．
    def __karnaugh0(self, var_map, fout) :
        fout.write('+-+\n')
        fout.write('|{:1}|\n'.format(self.__tv_list[0]))
        fout.write('+-+\n')

    ### @brief 1変数のカルノー図を出力する．
    def __karnaugh1(self, var_map, fout) :
        fout.write('---+-+\n')
        fout.write(' 0 |{:1}|\n'.format(self.__tv_list[0]))
        fout.write('---+-+\n')
        fout.write(' 1 |{:1}|\n'.format(self.__tv_list[1]))
        fout.write('---+-+\n')

    ### @brief 2変数のカルノー図を出力する．
    def __karnaugh2(self, var_map, fout) :
        fout.write(' {:3}|0|1|\n'.format(var_map[1]))
        fout.write(' \  | | |\n')
        fout.write(' {:3}| | |\n'.format(var_map[0]))
        fout.write('----+-+-+\n')
        fout.write('  0 |{:1}|{:1}\n'.format(self.__tv_list[0], self.__tv_list[1]))
        fout.write('----+-+-+\n')
        fout.write('  1 |{:1}|{:1}\n'.format(self.__tv_list[2], self.__tv_list[3]))

    ### @brief 3変数のカルノー図を出力する．
    def __karnaugh3(self, var_map, fout) :
        fout.write(' {:3}{:3}|00|01|11|10|\n'.format(var_map[1], var_map[2]))
        fout.write('   \   |  |  |  |  |\n')
        fout.write('   {:3} |  |  |  |  |\n'.format(var_map[0]))
        fout.write('-------+--+--+--+--+\n')
        fout.write('   0   | {:1}| {:1}| {:1}| {:1}|\n'.format(self.__tv_list[0], self.__tv_list[1], \
                                                        self.__tv_list[3], self.__tv_list[2]))
        fout.write('-------+--+--+--+--+\n')
        fout.write('   1   | {:1}| {:1}| {:1}| {:1}|\n'.format(self.__tv_list[4], self.__tv_list[5], \
                                                        self.__tv_list[7], self.__tv_list[6]))

    ### @brief 4変数のカルノー図を出力する．
    def __karnaugh4(self, var_map, fout) :
        fout.write(' {:3}{:3}|00|01|11|10|\n'.format(var_map[2], var_map[3]))
        fout.write('   \   |  |  |  |  |\n')
        fout.write(' {:3}{:3}|  |  |  |  |\n'.format(var_map[0], var_map[1]))
        fout.write('-------+--+--+--+--+\n')
        fout.write('  00   | {:1}| {:1}| {:1}| {:1}|\n'.format(self.__tv_list[0], self.__tv_list[1], \
                                                               self.__tv_list[3], self.__tv_list[2]))
        fout.write('-------+--+--+--+--+\n')
        fout.write('  01   | {:1}| {:1}| {:1}| {:1}|\n'.format(self.__tv_list[4], self.__tv_list[5], \
                                                               self.__tv_list[7], self.__tv_list[6]))
        fout.write('-------+--+--+--+--+\n')
        fout.write('  11   | {:1}| {:1}| {:1}| {:1}|\n'.format(self.__tv_list[12], self.__tv_list[13], \
                                                               self.__tv_list[15], self.__tv_list[14]))
        fout.write('-------+--+--+--+--+\n')
        fout.write('  10   | {:1}| {:1}| {:1}| {:1}|\n'.format(self.__tv_list[8], self.__tv_list[9], \
                                                               self.__tv_list[11], self.__tv_list[10]))

    ### @brief 積和標準形をLaTex形式で出力する．
    ### @param[in] varmap 変数名の辞書
    ### @param[in] fout 出力先のファイルオブジェクト
    def gen_latex_minterm_sop(self, *, var_map = None, fout = None) :
        if var_map == None :
            var_map = self.__var_map

        if fout == None :
            fout = sys.stdout

        nexp = 1 << self.input_num

        sop = "$"
        plus = ""
        for p in range(0, nexp) :
            if self.__tv_list[p] == Bool3._1 :
                term = ""
                for i in range(0, self.input_num) :
                    if p & (1 << i) :
                        term += "{}".format(var_map[i])
                    else :
                        term += "\\bar{{{}}}".format(var_map[i])
                sop += plus + term
                plus = " + "
        sop += "$\n"
        fout.write(sop)


    ### @brief 真理値表をLaTex形式で出力する．
    ### @param[in] fname 関数名
    ### @param[in] var_map 変数名の辞書
    ### @param[in] fout 出力先のファイルオブジェクト
    def gen_latex_table(self, fname, *, var_map = None, fout = None) :
        if var_map == None :
            var_map = self.__var_map

        if fout == None :
            fout = sys.stdout

        nexp = 1 << self.input_num

        # ヘッダの出力
        fout.write('\\begin{tabular}{|')
        fout.write('c' * self.input_num)
        fout.write('|c|}\n')
        fout.write('\\hline\n')
        for i in range(0, self.input_num) :
            fout.write('${}$ & '.format(var_map[i]))
        fout.write(' ${}$\\\\\n'.format(fname))
        fout.write('\\hline \\hline\n')

        # 中身の出力
        for p in range(0, nexp) :
            for i in range(0, self.input_num) :
                ival = '1' if p & (1 << (self.input_num - i - 1)) else '0'
                fout.write('{} & '.format(ival))
            v = self.__tv_list[p]
            if v == Bool3._1 :
                oval = '1'
            elif v == Bool3._0 :
                oval = '0'
            elif v == Bool3._d :
                oval = '$\\ast$'
            else :
                assert False
            fout.write('{}\\\\\n'.format(oval))

        # フッタの出力
        fout.write('\\hline\n')
        fout.write('\\end{tabular}\n')

    ### @brief 複数の関数を表す真理値表を LaTeX 形式で出力する．
    ### @param[in] func_list 関数のリスト
    ### @param[in] fname_list 関数名のリスト
    ### @param[in] var_map 変数名の辞書
    ### @param[in] fout 出力先のファイルオブジェクト
    ###
    ### * func_list は最低1つは要素を持たなければならない．
    ### * fname_list の要素数は func_list の要素数と同じでなければならない．
    @staticmethod
    def gen_latex_tables(func_list, fname_list, *, var_map = None, fout = None) :
        nf = len(func_list)
        assert nf > 0
        assert len(fname_list) == nf

        if var_map == None :
            var_map = func_list[0].__var_map

        if fout == None :
            fout = sys.stdout

        ni = func_list[0].input_num
        nexp = 1 << ni

        for f in func_list :
            assert f.input_num == ni

        # ヘッダの出力
        fout.write('\\begin{tabular}{|')
        fout.write('c' * ni)
        fout.write('|')
        fout.write('c' * nf)
        fout.write('|}\n')
        fout.write('\\hline\n')
        for i in range(0, ni) :
            fout.write('${}$ & '.format(var_map[i]))
        for i in range(0, nf) :
            fout.write(' ${}$'.format(fname_list[i]))
            if i < (nf - 1) :
                fout.write(' & ')
        fout.write('\\\\\n')
        fout.write('\\hline \\hline\n')

        def oval_str(val) :
            if val == Bool3._1 :
                return '1'
            elif v == Bool3._0 :
                return '0'
            elif v == Bool3._d :
                return '$\\ast$'
            else :
                assert False
            return None

        # 中身の出力
        for p in range(0, nexp) :
            for i in range(0, ni) :
                ival = '1' if p & (1 << (ni - i - 1)) else '0'
                fout.write('{} & '.format(ival))
            for i in range(0, nf) :
                v = func_list[i].__tv_list[p]
                oval = oval_str(v)
                fout.write('{}'.format(oval))
                if i < (nf - 1) :
                    fout.write(' & ')
            fout.write('\\\\\n')

        # フッタの出力
        fout.write('\\hline\n')
        fout.write('\\end{tabular}\n')


    ### @brief カルノー図をLaTex形式で出力する．
    ### @param[in] implicant_list インプリカントのリスト
    ### @param[in] var_map 変数名の辞書
    ### @param[in] fout 出力先のファイルオブジェクト
    def gen_latex_karnaugh(self, *, implicant_list = None, var_map = None, fout = None) :
        if var_map == None :
            var_map = self.__var_map

        if fout == None :
            fout = sys.stdout

        nexp = 1 << self.input_num

        # ヘッダの出力
        fout.write('\\begin{karnaugh-map}')
        if self.input_num == 0 :
            fout.write('[1][1][1][][]\n')
        elif self.input_num == 1 :
            fout.write('[1][2][1][][${}$]\n'.format(var_map[0]))
        elif self.input_num == 2 :
            fout.write('[2][2][1][${}$][${}$]\n'.format(var_map[0], var_map[1]))
        elif self.input_num == 3 :
            fout.write('[2][4][1][${}$][${}{}$]\n'.format(var_map[0], var_map[1], var_map[2]))
        elif self.input_num == 4 :
            fout.write('[4][4][1][${}{}$][${}{}$]\n'.format(var_map[0], var_map[1], var_map[2], var_map[3]))
        elif self.input_num == 5 :
            fout.write('Too many inputs.\n')
            return
        elif self.input_num == 6 :
            fout.write('Too many inputs.\n')
            return
        else :
            fout.write('Too many inputs.\n')
            return

        minterm_list = [ p for p in range(0, nexp) if self.__tv_list[p] == Bool3._1 ]
        fout.write('\\minterms{')
        comma = ''
        for p in minterm_list :
            fout.write('{}{}'.format(comma, p))
            comma = ','
        fout.write('}\n')

        maxterm_list = [ p for p in range(0, nexp) if self.__tv_list[p] == Bool3._0 ]
        fout.write('\\maxterms{')
        comma = ''
        for p in maxterm_list :
            fout.write('{}{}'.format(comma, p))
            comma = ','
        fout.write('}\n')

        fout.write('\\autoterms[$\\ast$]\n')

        if implicant_list :
            for cube in implicant_list :
                impl_str = self.gen_implicant_str(cube)
                fout.write(impl_str)
                fout.write('\n')

        fout.write('\end{karnaugh-map}\n')

    def gen_implicant_str(self, cube) :
        if self.input_num == 0 :
            # 無条件で決まる．
            return '\\implicant{0}'
        elif self.input_num == 1 :
            if cube[0] == Bool3._d :
                return '\\implicant{0}{1}'
            elif cube[0] == Bool3._1 :
                return '\\implicant{1}{1}'
            elif cube[0] == Bool3._0 :
                return '\\implicant{0}{0}'
        elif self.input_num == 2 :
            if cube[0] == Bool3._d :
                pat0 = 0b1111
            elif cube[0] == Bool3._1 :
                pat0 = 0b1100
            elif cube[0] == Bool3._0 :
                pat0 = 0b0011
            else :
                assert False

            if cube[1] == Bool3._d :
                pat1 = 0b1111
            elif cube[1] == Bool3._1 :
                pat1 = 0b1010
            elif cube[1] == Bool3._0 :
                pat1 = 0b0101
            else :
                assert False

            pat = pat0 & pat1

            for i in (0, 1, 2, 3) :
                if pat & (0b0001 << i) :
                    ul = i
                    break
            else :
                assert False

            for i in (3, 2, 1, 0) :
                if pat & (0b0001 << i) :
                    dr = i
                    break
            else :
                assert False

            return '\\implicant{{{}}}{{{}}}'.format(ul, dr)
        elif self.input_num == 3 :
            if cube[0] == Bool3._d :
                pat0 = 0b11111111
            elif cube[0] == Bool3._1 :
                pat0 = 0b11110000
            elif cube[0] == Bool3._0 :
                pat0 = 0b00001111
            else :
                assert False

            if cube[1] == Bool3._d :
                pat1 = 0b11111111
            elif cube[1] == Bool3._1 :
                pat1 = 0b11001100
            elif cube[1] == Bool3._0 :
                pat1 = 0b00110011
            else :
                assert False

            if cube[2] == Bool3._d :
                pat2 = 0b11111111
            elif cube[2] == Bool3._1 :
                pat2 = 0b10101010
            elif cube[2] == Bool3._0 :
                pat2 = 0b01010101
            else :
                assert False

            pat = pat0 & pat1 & pat2

            # implicantedge タイプの特例
            if pat == 0b00000101 :
                return '\\implicantedge{0}{0}{2}{2}'
            if pat == 0b01010101 :
                return '\\implicantedge{0}{4}{2}{6}'
            if pat == 0b01010000 :
                return '\\implicantedge{4}{4}{6}{6}'

            # 一般形
            for i in (0, 1, 3, 2, 4, 5, 7, 6) :
                if pat & (0b00000001 << i) :
                    ul = i
                    break
            else :
                assert False

            for i in (6, 7, 5, 4, 2, 3, 1, 0) :
                if pat & (0b00000001 << i) :
                    dr = i
                    break
            else :
                assert False

            return '\\implicant{{{}}}{{{}}}'.format(ul, dr)

        elif self.input_num == 4 :
            if cube[0] == Bool3._d :
                pat0 = 0b1111111111111111
            elif cube[0] == Bool3._1 :
                pat0 = 0b1111111100000000
            elif cube[0] == Bool3._0 :
                pat0 = 0b0000000011111111
            else :
                assert False

            if cube[1] == Bool3._d :
                pat1 = 0b1111111111111111
            elif cube[1] == Bool3._1 :
                pat1 = 0b1111000011110000
            elif cube[1] == Bool3._0 :
                pat1 = 0b0000111100001111
            else :
                assert False

            if cube[2] == Bool3._d :
                pat2 = 0b1111111111111111
            elif cube[2] == Bool3._1 :
                pat2 = 0b1100110011001100
            elif cube[2] == Bool3._0 :
                pat2 = 0b0011001100110011
            else :
                assert False

            if cube[3] == Bool3._d :
                pat3 = 0b1111111111111111
            elif cube[3] == Bool3._1 :
                pat3 = 0b1010101010101010
            elif cube[3] == Bool3._0 :
                pat3 = 0b0101010101010101
            else :
                assert False

            pat = pat0 & pat1 & pat2 & pat3

            # implicantcorer の特例
            if pat == 0b0000010100000101 :
                return '\\implicantcorer'

            # implicantedge の特例
            if pat & 0b0000000000001111 == 0b0000000000000101 :
                r0 = True
            else :
                r0 = False
            if pat & 0b0000000011110000 == 0b0000000001010000 :
                r1 = True
            else :
                r1 = False
            if pat & 0b0000111100000000 == 0b0000010100000000 :
                r3 = True
            else :
                r3 = False
            if pat & 0b1111000000000000 == 0b0101000000000000 :
                r2 = True
            else :
                r2 = False
            if r0 and r1 and r2 and r3 :
                return '\\implicantedge{0}{8}{2}{10}'
            elif r0 and r1 :
                return '\\implicantedge{0}{4}{2}{6}'
            elif r1 and r2 :
                return '\\implicantedge{4}{12}{6}{14}'
            elif r2 and r3 :
                return '\\implicantedge{12}{8}{14}{10}'
            elif r0 :
                return '\\implicantedge{0}{0}{2}{2}'
            elif r1 :
                return '\\implicantedge{4}{4}{6}{6}'
            elif r2 :
                return '\\implicantedge{12}{12}{14}{14}'
            elif r3 :
                return '\\implicantedge{8}{8}{10}{10}'

            if pat & 0b0000111100001111 == 0b0000000100000001 :
                c0 = True
            else :
                c0 = False
            if pat & 0b0000111100001111 == 0b0000001000000010 :
                c1 = True
            else :
                c1 = False
            if pat & 0b0000111100001111 == 0b0000100000001000 :
                c2 = True
            else :
                c2 = False
            if pat & 0b0000111100001111 == 0b0000010000000100 :
                c3 = True
            else :
                c3 = False
            if c0 and c1 and c2 and c3 :
                return '\\implicantedge{0}{2}{8}{10}'
            elif c0 and c1 :
                return '\\implicantedge{0}{1}{8}{9}'
            elif c1 and c2 :
                return '\\implicantedge{1}{3}{9}{11}'
            elif c2 and c3 :
                return '\\implicantedge{3}{2}{11}{12}'
            elif c0 :
                return '\\implicantedge{0}{0}{8}{8}'
            elif c1 :
                return '\\implicantedge{1}{1}{9}{9}'
            elif c2 :
                return '\\implicantedge{3}{3}{11}{11}'
            elif c3 :
                return '\\implicantedge{2}{2}{10}{10}'

            # 一般形
            for i in (0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10) :
                if pat & (0b0000000000000001 << i) :
                    ul = i
                    break
            else :
                assert False

            for i in (10, 11, 9, 8, 14, 15, 13, 12, 6, 7, 5, 4, 2, 3, 1, 0) :
                if pat & (0b0000000000000001 << i) :
                    dr = i
                    break
            else :
                assert False

            return '\\implicant{{{}}}{{{}}}'.format(ul, dr)


    ### @brief 幾何学表現（ハイパーキューブ）用のdpicソースを出力する．
    ### @param[in] fout 出力先のファイルオブジェクト
    def gen_dpic_hypercube(self, *, fout = None) :
        if fout == None :
            fout = sys.stdout

        nexp = 1 << self.input_num

        for p in range(0, nexp) :
            cube_pat = ''
            for i in range(0, self.input_num) :
                if p & (1 << (self.input_num - i - 1)) :
                    pat = '1'
                else :
                    pat = '0'
                cube_pat += pat
            if self.__tv_list[p] == Bool3._1 :
                color = "black"
            else :
                color = "white"
            fout.write('HC_VERTEX({}, "{}")\n'.format(cube_pat, color))



if __name__ == '__main__' :

    def print_func(f, f_name, f_desc) :
        var_map = { 0: 'x_0',
                    1: 'x_1',
                    2: 'x_2',
                    3: 'x_3' }
        print('{} = {}'.format(f_name, f_desc))
        print('')
        print('{}.print_table()'.format(f_name))
        f.print_table()
        print('')
        print('{}.print_karnaugh()'.format(f_name))
        f.print_karnaugh()
        print('')
        print('{}.gen_latex_table()'.format(f_name))
        f.gen_latex_table(f_name, var_map = var_map)
        print('')
        print('{}.gen_latex_karnaugh()'.format(f_name))
        f.gen_latex_karnaugh(var_map = var_map)
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
