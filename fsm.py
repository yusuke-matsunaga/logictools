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
    def __init__(self, input_list, output_list) :
        self.__input_list = tuple(input_list)
        self.__output_list = tuple(output_list)
        self.__state_list = list()


    ### @brief 状態を追加する．
    def new_state(self, name) :
        state = State(len(self.__state_list), name)
        self.__state_list.append(state)
        return state


    ### @brief __mark_dict 用のキーを作る．
    @staticmethod
    def __key(s, t, phase) :
        id1 = s.id
        id2 = t.id
        if id1 > id2 :
            id1 = t.id
            id2 = s.id
        return (id1, id2, phase)


    # 最小化を行う．
    def minimize(self) :
        self.__mark_dict = dict()
        phase = 0
        ns = len(self.__state_list)
        for i1 in range(0, ns - 1) :
            s = self.__state_list[i1]
            for i2 in range(i1 + 1, ns) :
                t = self.__state_list[i2]
                for iv in self.__input_list :
                    s1, o1 = s.next(iv)
                    t1, o2 = t.next(iv)
                    key = Fsm.__key(s, t, phase)
                    if o1 != o2 :
                        self.__mark_dict[key] = False
                        break
                    if s1 != t1 :
                        if key not in self.__mark_dict :
                            self.__mark_dict[key] = list()
                        self.__mark_dict[key].append((s1, t1))
                assert key in self.__mark_dict

        # 二周目以降
        while True :
            phase += 1
            changed = False
            for i1 in range(0, ns - 1) :
                s = self.__state_list[i1]
                for i2 in range(i1 + 1, ns) :
                    t = self.__state_list[i2]
                    key = Fsm.__key(s, t, phase - 1)
                    new_key = Fsm.__key(s, t, phase)
                    if self.__mark_dict[key] == False :
                        self.__mark_dict[new_key] = False
                        continue
                    new_list = list()
                    for s1, t1 in self.__mark_dict[key] :
                        new_list.append((s1, t1))
                        key1 = Fsm.__key(s1, t1, phase - 1)
                        if self.__mark_dict[key1] == False :
                            self.__mark_dict[new_key] = False
                            changed = True
                    if not new_key in self.__mark_dict :
                        self.__mark_dict[new_key] = new_list
            if not changed :
                break
        self.__max_phase = phase + 1

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


    ### @brief 最小化のための両立テーブルを LaTeX 形式で出力する．
    def gen_latex_compatible_table(self, fout = sys.stdout) :
        self.minimize()
        for phase in range(self.__max_phase) :
            fout.write('\\begin{tabular}{|c||')
            n = len(self.__state_list)
            for i in range(0, n - 1) :
                fout.write('c|')
            fout.write('}\n')
            fout.write('\\cline{1-2}\n')
            for i in range(1, n) :
                t = self.__state_list[i]
                fout.write(t.name)
                for j in range(0, i) :
                    fout.write(' & ')
                    s = self.__state_list[j]
                    key = Fsm.__key(s, t, phase)
                    x = self.__mark_dict[key]
                    if x == False :
                        fout.write('---')
                    else :
                        for s1, t1, in x :
                            fout.write(' ({}, {})'.format(s1.name, t1.name))
                if i < n - 1:
                    fout.write(' & \\multicolumn{{{}}}{{|c}}{{}} \\\\ \\cline{{1-{}}}\n'.format(n - i - 1, i + 2))
                else :
                    fout.write(' \\\\ \\hline \\hline\n')
            fout.write(' ')
            for i in range(0, n - 1) :
                s = self.__state_list[i]
                fout.write(' & ')
                fout.write(s.name)
            fout.write('\\\\\n \\hline')
            fout.write('\end{tabular}\n')


    ### @brief 符号化を行う．
    ### @param[in] input_map 入力の符号割当
    ### @param[in] output_map 出力の符号割当
    ### @param[in] state_map 状態の符号割当
    ### @return 符号化を行った有限状態機械を返す．
    def encode(self, input_map, output_map, state_map) :
        new_input_list = [ input_map[i] for i in self.__input_list ]
        new_output_list = [ output_map[i] for i in self.__output_list ]
        new_fsm = Fsm(new_input_list, new_output_list)
        state_dict = {}
        new_state_list = []
        for state in self.__state_list :
            state1 = new_fsm.new_state(state_map[state.name])
            state_dict[state.name] = state1

        for state in self.__state_list :
            state1 = state_dict[state.name]
            for input_val in self.__input_list :
                next_state, output_val = state.next(input_val)
                new_input_val = input_map[input_val]
                new_next_state = state_dict[next_state.name]
                new_output_val = output_map[output_val]
                state1.set_next(new_input_val, new_next_state, new_output_val)

        return new_fsm


if __name__ == '__main__' :

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

    fsm = Fsm(input_list, output_list)
    s0 = fsm.new_state('$S_0$')
    s1 = fsm.new_state('$S_1$')
    s11 = fsm.new_state('$S_{11}$')
    s111 = fsm.new_state('$S_{111}$')

    s0.set_next(i_0, s0, o_b)
    s0.set_next(i_1, s1, o_0)

    s1.set_next(i_0, s0, o_c)
    s1.set_next(i_1, s11, o_0)

    s11.set_next(i_0, s0, o_a)
    s11.set_next(i_1, s111, o_0)

    s111.set_next(i_0, s0, o_d)
    s111.set_next(i_1, s0, o_e)

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

    print()
    new_fsm.gen_latex_compatible_table()
