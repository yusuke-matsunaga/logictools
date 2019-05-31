#! /usr/bin/env python3

### @file boolfunc.py
### @brief BoolFunc の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2017, 2019 Yusuke Matsunaga
### All rights reserved.

import sys

### @class BoolFunc
### @brief Boolean Function を表すクラス
###
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
    ###
    ### 3入力の恒真関数を作るコード
    ### @code
    ### f = BoolFunc.make_const1(3)
    ### @endcode
    @staticmethod
    def make_const1(input_num) :
        nexp = 1 << input_num
        return BoolFunc(input_num, [True for i in range(0, nexp)])

    ### @brief リテラル関数を作る．
    ### @param[in] input_num
    ### @param[in] var_id 変数番号 ( 0 <= var_id < input_num )
    ###
    ### 5入力の0番目の変数のりテラル関数を作るコード
    ### @code
    ### f = BoolFunc.make_literal(5, 0)
    ### @endcode
    ###
    ### 否定のリテラルは否定演算(~)で作る．
    @staticmethod
    def make_literal(input_num, var_id) :
        def literal(p, var_id) :
            return True if p & (1 << (input_num - var_id - 1)) else False
        nexp = 1 << input_num
        return BoolFunc(input_num, [literal(p, var_id) for p in range(0, nexp)])

    ### @brief AND関数を作る．
    ### @param[in] input_num 入力数
    ###
    ### 4入力のAND関数を作るコード
    ### @code
    ### f = BoolFunc.make_and(4)
    ### @endcode
    @staticmethod
    def make_and(input_num) :
        nexp = 1 << input_num
        return BoolFunc(input_num, [True if i == (nexp - 1) else False for i in range(0, nexp)])

    ### @brief NAND関数を作る．
    ### @param[in] input_num 入力数
    ###
    ### 4入力のNAND関数を作るコード
    ### @code
    ### f = BoolFunc.make_nand(4)
    ### @endcode
    @staticmethod
    def make_nand(input_num) :
        nexp = 1 << input_num
        return BoolFunc(input_num, [False if i == (nexp - 1) else True for i in range(0, nexp)])

    ### @brief OR関数を作る．
    ### @param[in] input_num 入力数
    ###
    ### 4入力のOR関数を作るコード
    ### @code
    ### f = BoolFunc.make_or(4)
    ### @endcode
    @staticmethod
    def make_or(input_num) :
        nexp = 1 << input_num
        return BoolFunc(input_num, [False if i == 0 else True for i in range(0, nexp)])

    ### @brief NOR関数を作る．
    ### @param[in] input_num 入力数
    ###
    ### 4入力のNOR関数を作るコード
    ### @code
    ### f = BoolFunc.make_nor(4)
    ### @endcode
    @staticmethod
    def make_nor(input_num) :
        nexp = 1 << input_num
        return BoolFunc(input_num, [True if i == 0 else False for i in range(0, nexp)])

    ### @brief XOR関数を作る．
    ### @param[in] input_num 入力数
    ###
    ### 4入力のXOR関数を作るコード
    ### @code
    ### f = BoolFunc.make_xor(4)
    ### @endcode
    @staticmethod
    def make_xor(input_num) :
        def parity(p, input_num) :
            c = 0
            for i in range(0, input_num) :
                if p & (1 << i) :
                    c += 1
            return (c % 2) == 1
        nexp = 1 << input_num
        return BoolFunc(input_num, [parity(p, input_num) for p in range(0, nexp)])

    ### @brief XNOR関数を作る．
    ### @param[in] input_num 入力数
    ###
    ### 4入力のXNOR関数を作るコード
    ### @code
    ### f = BoolFunc.make_xnor(4)
    ### @endcode
    @staticmethod
    def make_xor(input_num) :
        def parity(p, input_num) :
            c = 0
            for i in range(0, input_num) :
                if p & (1 << i) :
                    c += 1
            return (c % 2) == 0
        nexp = 1 << input_num
        return BoolFunc(input_num, [parity(p, input_num) for p in range(0, nexp)])

    ### @brief 初期化
    ### @param[in] input_num 入力数
    ### @param[in] val_list 値のリスト
    ###
    ### - val_list が省略された場合には恒偽関数となる．
    ### - val_list の長さは 2^input_num でなければならない．
    def __init__(self, input_num, val_list = None) :
        self.__input_num = input_num
        nexp = 1 << input_num
        if val_list :
            assert len(val_list) == nexp
            self.__tv_list = [val_list[i] for i in range(0, nexp)]
        else :
            self.__tv_list = [False for i in range(0, nexp)]

        # デフォルトの変数名マップを作る．
        self.__var_map = {i : 'v{}'.format(i) for i in range(0, input_num)}

    ### @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ### @brief 入力値に対する出力値を返す．
    ### @param[in] ival_list 入力値のリスト
    ###
    ### 結果は bool 型のオブジェクト(True|False)
    def val(self, ival_list) :
        assert len(ival_list) == self.input_num
        pos = 0
        for i in range(0, self.input_num) :
            if ival_list[i] :
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
        return BoolFunc(self.input_num, [not v for v in self.__tv_list])

    ### @brief AND演算子
    ###
    ### @code
    ### f1 = BoolFunc() # 本当は入力数が必要
    ### f2 = BoolFunc() # 本当は入力数が必要
    ### g = f1 & f2
    ### @endcode
    ### という風に使う．
    def __and__(self, other) :
        assert self.input_num == other.__input_num
        nexp = 1 << self.input_num
        return BoolFunc(self.input_num, \
                        [self.__tv_list[p] and other.__tv_list[p] for p in range(0, nexp)])

    ### @brief OR演算子
    ###
    ### @code
    ### f1 = BoolFunc() # 本当は入力数が必要
    ### f2 = BoolFunc() # 本当は入力数が必要
    ### g = f1 | f2
    ### @endcode
    ### という風に使う．
    def __or__(self, other) :
        assert self.input_num == other.__input_num
        nexp = 1 << self.input_num
        return BoolFunc(self.input_num, \
                        [self.__tv_list[p] or other.__tv_list[p] for p in range(0, nexp)])

    ### @brief XOR演算子
    ###
    ### @code
    ### f1 = BoolFunc() # 本当は入力数が必要
    ### f2 = BoolFunc() # 本当は入力数が必要
    ### g = f1 ^ f2
    ### @endcode
    ### という風に使う．
    def __xor__(self, other) :
        def xor(x, y) :
            return (x and (not y)) or ((not x) and y)
        assert self.input_num == other.__input_num
        nexp = 1 << self.input_num
        return BoolFunc(self.input_num, \
                        [xor(self.__tv_list[p], other.__tv_list[p]) for p in range(0, nexp)])

    ### @brief compose 演算
    ### @param[in] ifunc_list 入力関数のリスト
    ###
    ### - 個々の入力を ifunc_list の要素に置き換えた関数を作る．
    ### - ifunc_list の要素数は self.input_num と等しくなければならない．
    ### - ifunc_list の関数は全て同じ入力数でなければならない．
    def compose(self, ifunc_list) :
        assert len(ifunc_list) == self.input_num

        if self.input_num == 0 :
            # 0 入力関数の場合は置き換える変数がない．
            return BoolFunc(0, self.__tv_list)

        new_ni = ifunc_list[0].input_num
        for i in range(1, self.input_num) :
            ifunc = ifunc_list[i]
            assert ifunc.input_num == new_ni

        ans = BoolFunc.make_const0(new_ni)
        nexp = 1 << self.input_num
        for p in range(0, nexp) :
            if self.__tv_list[p] == 0 :
                continue
            p_func = BoolFunc.make_const1(new_ni)
            for i in range(0, self.input_num) :
                if p & (1 << (self.input_num - i - 1)) :
                    p_func &= ifunc_list[i]
                else :
                    p_func &= ~ifunc_list[i]
            ans |= p_func
        return ans

    ### @brief 等価比較演算子
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
        fout.write('| f')
        for i in range(0, self.input_num) :
            fout.write('----')
        fout.write('+--\n')

        # 中身の出力
        for p in range(0, nexp) :
            for i in range(0, self.input_num) :
                ival = '1' if p & (1 << (self.input_num - i - 1)) else '0'
                fout.write('  {:1} '.format(ival))
            oval = '1' if self.__tv_list[p] else '0'
            fout.write('| {:1}\n'.format(oval))

    ### @brief 真理値表をLaTex形式で出力する．
    ### @param[in] fname 関数名
    ### @param[in] var_map 変数名の辞書
    ### @param[in] fout 出力先のファイルオブジェクト
    def print_latex_table(self, fname, *, var_map = None, fout = None) :
        if var_map == None :
            var_map = self.__var_map

        if fout == None :
            fout = sys.stdout

        nexp = 1 << self.input_num

        # ヘッダの出力
        fout.write('\\begin{tabular}{|')
        for i in range(0, self.input_num) :
            fout.write('c')
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
            oval = '1' if self.__tv_list[p] else '0'
            fout.write('{}\\\\\n'.format(oval))

        # フッタの出力
        fout.write('\\hline\n')
        fout.write('\\end{tabular}\n')

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
            print('Too many inputs.', file=fout)

    ### @brief 0変数のカルノー図を出力する．
    def __karnaugh0(self, var_map, fout) :
        fout.write('+-+\n')
        fout.write('|{:1}|\n'.format(self.__tv_list[0]))
        fout.write('+-+\n')

    ## @brief 1変数のカルノー図を出力する．
    def __karnaugh1(self, var_map, fout) :
        fout.write('---+-+\n')
        fout.write(' 0 |{:1}|\n'.format(self.__tv_list[0]))
        print('---+-+', file=fout)
        print(' 1 |{:1}|'.format(self.__tv_list[1]), file=fout)
        print('---+-+', file=fout)

    ## @brief 2変数のカルノー図を出力する．
    def __karnaugh2(self, var_map, fout) :
        print(' {:3}|0|1|'.format(var_map[1]), file=fout)
        print(' \  | | |', file=fout)
        print(' {:3}| | |'.format(var_map[0]), file=fout)
        print('----+-+-+', file=fout)
        print('  0 |{:1}|{:1}'.format(self.__tv_list[0], self.__tv_list[1]), file=fout)
        print('----+-+-+', file=fout)
        print('  1 |{:1}|{:1}'.format(self.__tv_list[2], self.__tv_list[3]), file=fout)

    ## @brief 3変数のカルノー図を出力する．
    def __karnaugh3(self, var_map, fout) :
        print(' {:3}{:3}|00|01|11|10|'.format(var_map[1], var_map[2]), file=fout)
        print('   \   |  |  |  |  |', file=fout)
        print('   {:3} |  |  |  |  |'.format(var_map[0]), file=fout)
        print('-------+--+--+--+--+', file=fout)
        print('   0   | {:1}| {:1}| {:1}| {:1}|'.format(self.__tv_list[0], self.__tv_list[1], \
                                                        self.__tv_list[3], self.__tv_list[2]), \
              file=fout)
        print('-------+--+--+--+--+', file=fout)
        print('   1   | {:1}| {:1}| {:1}| {:1}|'.format(self.__tv_list[4], self.__tv_list[5], \
                                                        self.__tv_list[7], self.__tv_list[6]), \
              file=fout)

    ## @brief 4変数のカルノー図を出力する．
    def __karnaugh4(self, var_map, fout) :
        print(' {:3}{:3}|00|01|11|10|'.format(var_map[2], var_map[3]), file=fout)
        print('   \   |  |  |  |  |', file=fout)
        print(' {:3}{:3}|  |  |  |  |'.format(var_map[0], var_map[1]), file=fout)
        print('-------+--+--+--+--+', file=fout)
        print('  00   | {:1}| {:1}| {:1}| {:1}|'.format(self.__tv_list[0], self.__tv_list[1], \
                                                        self.__tv_list[3], self.__tv_list[2]), \
              file=fout)
        print('-------+--+--+--+--+', file=fout)
        print('  01   | {:1}| {:1}| {:1}| {:1}|'.format(self.__tv_list[4], self.__tv_list[5], \
                                                        self.__tv_list[7], self.__tv_list[6]), \
              file=fout)
        print('-------+--+--+--+--+', file=fout)
        print('  11   | {:1}| {:1}| {:1}| {:1}|'.format(self.__tv_list[12], self.__tv_list[13], \
                                                        self.__tv_list[15], self.__tv_list[14]), \
              file=fout)
        print('-------+--+--+--+--+', file=fout)
        print('  10   | {:1}| {:1}| {:1}| {:1}|'.format(self.__tv_list[8], self.__tv_list[9], \
                                                        self.__tv_list[11], self.__tv_list[10]), \
              file=fout)


if __name__ == '__main__' :

    def print_func(f, f_name, f_desc) :
        print('{} = {}'.format(f_name, f_desc))
        print('')
        print('{}.print_table()'.format(f_name))
        f.print_table()
        print('')
        print('{}.print_latex_table()'.format(f_name))
        f.print_latex_table(f_name)
        print('')
        print('{}.print_karnaugh()'.format(f_name))
        f.print_karnaugh()
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
