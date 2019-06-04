#! /usr/bin/env python3

### @file boolfunc.py
### @brief BoolFunc の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2017, 2019 Yusuke Matsunaga
### All rights reserved.

import sys
from bool3 import Bool3

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
            self.__var_map = {i : 'v{}'.format(i) for i in range(0, input_num)}

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
            fout.write('{} & '.format(var_map[i]))
        fout.write(' {}\\\\\n'.format(fname))
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

    ### @brief カルノー図をLaTex形式で出力する．
    ### @param[in] var_map 変数名の辞書
    ### @param[in] fout 出力先のファイルオブジェクト
    def gen_latex_karnaugh(self, *, var_map = None, fout = None) :
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
            fout.write('[1][2][1][][{}]\n'.format(var_map[0]))
        elif self.input_num == 2 :
            fout.write('[2][2][1][{}][{}]\n'.format(var_map[0], var_map[1]))
        elif self.input_num == 3 :
            fout.write('[2][4][1][{}][{}{}]\n'.format(var_map[0], var_map[1], var_map[2]))
        elif self.input_num == 4 :
            fout.write('[4][4][1][{}{}][{}{}]\n'.format(var_map[0], var_map[1], var_map[2], var_map[3]))
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
        fout.write('\end{karnaugh-map}\n')


if __name__ == '__main__' :

    def print_func(f, f_name, f_desc) :
        var_map = { 0: '$x_0$',
                    1: '$x_1$',
                    2: '$x_2$',
                    3: '$x_3$' }
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
