#! /usr/bin/env python3

### @file fsm.py
### @brief Fsm の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019 Yusuke Matsunaga
### All rights reserved.

import sys
from lctools.state import State

### @brief 有限状態機械を表すクラス
class Fsm :

    ### @brief 初期化
    ### @param[in] input_list 入力記号のリスト
    ### @param[in] output_list 出力記号のリスト
    ### @param[in] state_list 状態のリスト
    def __init__(self, input_list, output_list, state_list) :
        self.__input_list = tuple(input_list)
        self.__output_list = tuple(output_list)
        self.__state_list = tuple(state_list)

    ### @brief 状態遷移表を出力する．
    def print_table(self, fout = sys.stdout) :
        max_i = 0
        for input_val in self.__input_list :
            n = len(input_val)
            if max_i < n :
                max_i = n

        max_o = 0
        for output_val in self.__output_list :
            n = len(output_val)
            if max_o < n :
                max_o = n

        # 状態名の最大長さを求める．
        max_n = 0
        for state in self.__state_list :
            n = len(state.name)
            if max_n < n :
                max_n = n

        max_ino = max_i
        if max_ino < (max_n + max_o + 1) :
            max_ino = max_n + max_o + 1

        fout.write(' ' * max_n)
        for input_val in self.__input_list :
            fout.write('|')
            r = max_ino - len(input_val)
            r2 = r // 2
            fout.write(' ' * r2)
            fout.write(input_val)
            fout.write(' ' * (r - r2))
        fout.write('\n')

        for state in self.__state_list :
            fout.write(state.name)
            n = max_n - len(state.name)
            fout.write(' ' * n)

            for input_val in self.__input_list :
                next_state, output_val = state.next(input_val)
                r1 = max_n - len(next_state.name)
                fout.write('|')
                fout.write(' ' * r1)
                fout.write(next_state.name)
                fout.write('/')
                fout.write(output_val)
                r2 = max_o - len(output_val)
                fout.write(' ' * r2)
            fout.write('\n')


    ### @brief 状態遷移表を LaTeX 形式で出力する．
    def gen_latex_table(self, fout = sys.stdout) :
        fout.write('\\begin{tabular}{|l')
        fout.write('|c' * len(self.__input_list))
        fout.write('|}\n')
        fout.write('\\hline\n')
        for input_val in self.__input_list :
            fout.write(' & ')
            fout.write(input_val)
        fout.write('\\\\\\hline\n')

        for state in self.__state_list :
            fout.write(state.name)
            for input_val in self.__input_list :
                next_state, output_val = state.next(input_val)
                fout.write(' & {}/{}'.format(next_state.name, output_val))
            fout.write('\\\\\\hline\n')

        fout.write('\\end{tabular}\n')


    ### @brief 符号化を行う．
    ### @param[in] input_map 入力の符号割当
    ### @param[in] output_map 出力の符号割当
    ### @param[in] state_map 状態の符号割当
    ### @return 符号化を行った有限状態機械を返す．
    def encode(self, input_map, output_map, state_map) :
        new_input_list = [ input_map[i] for i in self.__input_list ]
        new_output_list = [ output_map[i] for i in self.__output_list ]
        state_dict = {}
        new_state_list = []
        for state in self.__state_list :
            new_state = State(state_map[state.name])
            new_state_list.append(new_state)
            state_dict[state.name] = new_state

        for state in self.__state_list :
            new_state = state_dict[state.name]
            for input_val in self.__input_list :
                next_state, output_val = state.next(input_val)
                new_input_val = input_map[input_val]
                new_next_state = state_dict[next_state.name]
                new_output_val = output_map[output_val]
                new_state.set_next(new_input_val, new_next_state, new_output_val)

        new_fsm = Fsm(new_input_list, new_output_list, new_state_list)

        return new_fsm


if __name__ == '__main__' :

    s0 = State('$S_0$')
    s1 = State('$S_1$')
    s11 = State('$S_{11}$')
    s111 = State('$S_{111}$')

    i_0 = '0'
    i_1 = '1'
    input_list = (i_0, i_1)

    o_a = 'a'
    o_b = 'b'
    o_c = 'c'
    o_d = 'd'
    o_e = 'e'
    o_0 = '$\epsilon$'

    output_list = (o_a, o_b, o_c, o_d, o_e, o_0)

    s0.set_next(i_0, s0, o_b)
    s0.set_next(i_1, s1, o_0)

    s1.set_next(i_0, s0, o_c)
    s1.set_next(i_1, s11, o_0)

    s11.set_next(i_0, s0, o_a)
    s11.set_next(i_1, s111, o_0)

    s111.set_next(i_0, s0, o_d)
    s111.set_next(i_1, s0, o_e)

    state_list = [ s0, s1, s11, s111 ]
    fsm = Fsm(input_list, output_list, state_list)

    fsm.print_table()

    print('')

    fsm.gen_latex_table()

    print('')

    input_map =  { i_0:i_0, i_1:i_1 }
    output_map = { o_a:'001', o_b:'010', o_c:'011', o_d:'100', o_e:'101', o_0:'000' }
    state_map = { s0.name:'00', s1.name:'01', s11.name:'10', s111.name:'11' }

    new_fsm = fsm.encode(input_map, output_map, state_map)

    new_fsm.print_table()

    print('')

    new_fsm.gen_latex_table()
