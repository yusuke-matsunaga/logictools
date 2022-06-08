#! /usr/bin/env python3

"""Fsm の実装ファイル

:file: fsm.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2019 Yusuke Matsunaga, All rights reserved.
"""

import sys
from lctools.state import State
from lctools.boolfunc import BoolFunc
from lctools.bool3 import Bool3
from graphviz import Digraph
from dot2tex import dot2tex


def label_str(src, label_map):
    """出力用のラベル文字列を得る．

    :param str src: 元の文字列
    :param dict[str, str] label_map: 変換用の辞書

    label_map が None の場合は src を返す．
    """
    if label_map is None:
        return src
    else:
        if src not in label_map:
            print('{} is not found'.format(src))
        return label_map[src]


class Fsm:
    """有限状態機械を表すクラス"""

    def __init__(self, input_list, output_list):
        """初期化

        :param input_list: 入力記号のリスト
        :param output_list: 出力記号のリスト

        この時点では状態をもたない．
        """

        self.__input_list = tuple(input_list)
        self.__output_list = tuple(output_list)
        self.__state_list = list()

    def new_state(self, name):
        """状態を追加する．

        :param name: 追加する状態名
        :return: 追加した状態を返す．
        """
        state = State(len(self.__state_list), name)
        self.__state_list.append(state)
        return state

    @staticmethod
    def __key(s, t, phase):
        """__mark_dict 用のキーを作る．"""
        id1 = s.id
        id2 = t.id
        if id1 > id2:
            id1 = t.id
            id2 = s.id
        return (id1, id2, phase)

    def minimize(self):
        """最小化を行う．

        :return: 最小化した機械を返す．
        """
        self.__mark_dict = dict()
        phase = 0
        ns = len(self.__state_list)
        for i1 in range(0, ns - 1):
            s = self.__state_list[i1]
            for i2 in range(i1 + 1, ns):
                t = self.__state_list[i2]
                key = Fsm.__key(s, t, phase)
                for iv in self.__input_list:
                    s1, o1 = s.next(iv)
                    t1, o2 = t.next(iv)
                    if o1 != o2:
                        self.__mark_dict[key] = False
                        break
                    if s1 != t1:
                        if key not in self.__mark_dict:
                            self.__mark_dict[key] = set()
                        if s1.id > t1.id:
                            s1, t1 = t1, s1
                        self.__mark_dict[key].add((s1, t1))
                assert key in self.__mark_dict

        # 二周目以降
        while True:
            phase += 1
            changed = False
            for i1 in range(0, ns - 1):
                s = self.__state_list[i1]
                for i2 in range(i1 + 1, ns):
                    t = self.__state_list[i2]
                    key = Fsm.__key(s, t, phase - 1)
                    new_key = Fsm.__key(s, t, phase)
                    if not self.__mark_dict[key]:
                        self.__mark_dict[new_key] = False
                        continue
                    self.__mark_dict[new_key] = set()
                    for s1, t1 in self.__mark_dict[key]:
                        self.__mark_dict[new_key].add((s1, t1))
                        key1 = Fsm.__key(s1, t1, phase - 1)
                        if not self.__mark_dict[key1]:
                            self.__mark_dict[new_key] = False
                            changed = True
                            break
            if not changed:
                break
        self.__max_phase = phase + 1

        # 最小化したFSMを作る．
        new_fsm = Fsm(self.__input_list, self.__output_list)
        # 今の機械の状態と新しい状態の対応付けを持つ辞書
        state_map = dict()
        for i1 in range(0, ns - 1):
            s = self.__state_list[i1]
            if s in state_map:
                # 等価状態がある．
                continue
            s1 = new_fsm.new_state(s.name)
            state_map[s] = s1
            for i2 in range(i1 + 1, ns):
                t = self.__state_list[i2]
                key = Fsm.__key(s, t, self.__max_phase - 1)
                if self.__mark_dict[key]:
                    state_map[t] = s1
        for s in self.__state_list:
            s1 = state_map[s]
            for i in self.__input_list:
                t, o = s.next(i)
                t1 = state_map[t]
                s1.set_next(i, t1, o)

        return new_fsm

    def print_table(self, *,
                    input_dict=None,
                    output_dict=None,
                    state_dict=None,
                    fout=sys.stdout):
        """状態遷移表を出力する．

        :param dict[str, str] input_dict: 出力用の入力記号の辞書
        :param dict[str, str] output_dict: 出力用の出力記号の辞書
        :param dict[str, str] state_dict: 出力用の状態名の辞書
        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout が省略されば場合には標準出力を用いる．
        """

        # 入力記号の最大長さを求める．
        max_i = 0
        for input_val in self.__input_list:
            n = len(label_str(input_val, input_dict))
            if max_i < n:
                max_i = n

        # 出力記号の最大長さを求める．
        max_o = 0
        for output_val in self.__output_list:
            n = len(label_str(output_val, output_dict))
            if max_o < n:
                max_o = n

        # 状態名の最大長さを求める．
        max_n = 0
        for state in self.__state_list:
            n = len(label_str(state.name, state_dict))
            if max_n < n:
                max_n = n

        max_ino = max_i
        if max_ino < (max_n + max_o + 1):
            max_ino = max_n + max_o + 1

        # 先頭行の出力
        # 状態名の分の空白
        fout.write(' ' * max_n)
        for input_val in self.__input_list:
            input_label = input_dict[input_val]
            # 各入力記号
            fout.write('|')
            r = max_ino - len(input_label)
            r2 = r // 2
            fout.write(' ' * r2)
            fout.write(input_label)
            fout.write(' ' * (r - r2))
        fout.write('\n')

        for state in self.__state_list:
            state_label = state_dict[state.name]
            fout.write(state_label)
            n = max_n - len(state_label)
            fout.write(' ' * n)

            for input_val in self.__input_list:
                next_state, output_val = state.next(input_val)
                r1 = max_n - len(next_state.name)
                fout.write('|')
                fout.write(' ' * r1)
                fout.write(state_dict[next_state.name])
                fout.write('/')
                fout.write(output_val)
                r2 = max_o - len(output_dict[output_val])
                fout.write(' ' * r2)
            fout.write('\n')

    def gen_latex_table(self, *,
                        input_dict=None,
                        output_dict=None,
                        state_dict=None,
                        state_label='states',
                        input_label='inputs',
                        no_backslash=False,
                        fout=sys.stdout):
        """状態遷移表を LaTeX 形式で出力する．

        :param dict[str, str] input_dict: 出力用の入力記号の辞書
        :param dict[str, str] output_dict: 出力用の出力記号の辞書
        :param dict[str, str] state_dict: 出力用の状態名の辞書
        :param state_label: 左上隅の左下側のラベル
        :param input_label: 左上隅の右上側のラベル．
        :param bool no_backslash: 左上隅のラベルを表示しない時に True にするフラグ
        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout が省略されば場合には標準出力を用いる．
        """

        fout.write('\\begin{tabular}{|l')
        fout.write('|c' * len(self.__input_list))
        fout.write('|}\n')
        fout.write('\\hline\n')
        if not no_backslash:
            fout.write('\\backslashbox{{{}}}{{{}}}'.format(
                state_label, input_label))
        for input_val in self.__input_list:
            fout.write(' & ')
            fout.write(label_str(input_val, input_dict))
        fout.write('\\\\\\hline\n')

        for state in self.__state_list:
            fout.write(label_str(state.name, state_dict))
            for input_val in self.__input_list:
                next_state, output_val = state.next(input_val)
                ns_label = label_str(next_state.name, state_dict)
                o_label = label_str(output_val, output_dict)
                fout.write(' & {}/{}'.format(ns_label, o_label))
            fout.write('\\\\\\hline\n')
        fout.write('\\end{tabular}\n')

    def gen_latex_encoded_table(self, *,
                                input_map,
                                output_map,
                                state_map,
                                state_label='states',
                                input_label='inputs',
                                no_backslash=False,
                                fout=sys.stdout):
        """符号化された状態遷移表を LaTeX 形式で出力する．

        :param dict input_map: 入力記号の符号割当
        :param dict output_map: 出力記号の符号割当
        :param dict state_map: 状態の符号割当
        :param state_label: 左上隅の左下側のラベル
        :param input_label: 左上隅の右上側のラベル．
        :param bool no_backslash: 左上隅のラベルを表示しない時に True にするフラグ
        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout が省略された場合には標準出力を用いる．
        """

        def encoded_str(src, encoding_map):
            vec = encoding_map[src]
            ans = ''
            for b in vec:
                ans += '{}'.format(b)
            return ans

        fout.write('\\begin{tabular}{|l')
        fout.write('|c' * len(self.__input_list))
        fout.write('|}\n')
        fout.write('\\hline\n')
        if not no_backslash:
            fout.write('\\backslashbox{{{}}}{{{}}}'.format(
                state_label, input_label))
        for input_val in self.__input_list:
            fout.write(' & {}'.format(encoded_str(input_val, input_map)))
        fout.write('\\\\\\hline\n')

        for state in self.__state_list:
            fout.write('{}'.format(encoded_str(state.name, state_map)))
            for input_val in self.__input_list:
                next_state, output_val = state.next(input_val)
                ns_str = encoded_str(next_state.name, state_map)
                o_str = encoded_str(output_val, output_map)
                fout.write(' & {}/{}'.format(ns_str, o_str))
            fout.write('\\\\\\hline\n')
        fout.write('\\end{tabular}\n')

    def gen_latex_compatible_table(self, *,
                                   state_dict=None,
                                   fout=sys.stdout):
        """最小化のための両立テーブルを LaTeX 形式で出力する．

        :param dict[str, str] state_dict: 出力用の状態名の辞書
        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout が省略されば場合には標準出力を用いる．
        """
        self.minimize()
        for phase in range(self.__max_phase):
            fout.write('\n')
            fout.write('\\vspace{1cm}')
            fout.write('Step\#{}\n'.format(phase + 1))
            fout.write('\n')
            fout.write('\\begin{tabular}{|c||')
            n = len(self.__state_list)
            for i in range(0, n - 1):
                fout.write('c|')
            fout.write('}\n')
            fout.write('\\cline{1-2}\n')
            for i in range(1, n):
                t = self.__state_list[i]
                fout.write(label_str(t.name, state_dict))
                for j in range(0, i):
                    fout.write(' & ')
                    s = self.__state_list[j]
                    key = Fsm.__key(s, t, phase)
                    x = self.__mark_dict[key]
                    if x:
                        for s1, t1, in x:
                            s1_label = label_str(s1, state_dict)
                            t1_label = label_str(t1, state_dict)
                            fout.write(' ({}, {})'.format(s1_label, t1_label))
                    else:
                        fout.write('---')
                if i < n - 1:
                    fout.write(
                        ' & \\multicolumn{{{}}}{{|c}}{{}} \\\\ \\cline{{1-{}}}\n'.format(n - i - 1, i + 2))
                else:
                    fout.write(' \\\\ \\hline \\hline\n')
            fout.write(' ')
            for i in range(0, n - 1):
                s = self.__state_list[i]
                fout.write(' & ')
                fout.write(label_str(s.name, stat_dict))
            fout.write('\\\\\n \\hline')
            fout.write('\\end{tabular}\n')

    def extract_functions(self, *,
                          input_map,
                          output_map,
                          state_map):
        """符号割当を行って次状態関数，出力関数を取り出す．

        :param input_map: 入力の符号割当
        :param output_map: 出力の符号割当
        :param state_map: 状態の符号割当
        :return 次状態関数，出力関数のリストを返す．
        """

        # 入力，出力，状態のビット長を得る．
        input_vec = input_map[self.__input_list[0]]
        ni = len(input_vec)
        output_vec = output_map[self.__output_list[0]]
        no = len(output_vec)
        state_vec = state_map[self.__state_list[0].name]
        ns = len(state_vec)

        # 状態遷移関数，出力関数を作る．
        nfi = ni + ns
        nfi_exp = 1 << nfi
        delta_val_list = [
            [Bool3._d for i in range(nfi_exp)] for j in range(ns)]
        lambda_val_list = [
            [Bool3._d for i in range(nfi_exp)] for j in range(no)]
        for state in self.__state_list:
            state_vec = state_map[state.name]
            pos0 = 0
            for b in state_vec:
                pos0 <<= 1
                pos0 += b
            for input_val in self.__input_list:
                input_vec = input_map[input_val]
                pos = pos0
                for b in input_vec:
                    pos <<= 1
                    pos += b
                next_state, output_val = state.next(input_val)
                next_vec = state_map[next_state.name]
                output_vec = output_map[output_val]
                for i in range(ns):
                    if next_vec[i]:
                        delta_val_list[i][pos] = Bool3._1
                    else:
                        delta_val_list[i][pos] = Bool3._0
                for i in range(no):
                    if output_vec[i]:
                        lambda_val_list[i][pos] = Bool3._1
                    else:
                        lambda_val_list[i][pos] = Bool3._0
        delta_list = [BoolFunc(delta_val_list[i]) for i in range(ns)]
        lambda_list = [BoolFunc(lambda_val_list[i]) for i in range(no)]
        return delta_list, lambda_list

    def encode(self, input_map, output_map, state_map):
        """符号化を行う．

        :param input_map: 入力の符号割当
        :param output_map: 出力の符号割当
        :param state_map: 状態の符号割当
        :return: 符号化を行った有限状態機械を返す．
        """
        new_input_list = [input_map[i] for i in self.__input_list]
        new_output_list = [output_map[i] for i in self.__output_list]
        new_fsm = Fsm(new_input_list, new_output_list)
        state_dict = {}
        for state in self.__state_list:
            state1 = new_fsm.new_state(state_map[state.name])
            state_dict[state.name] = state1

        for state in self.__state_list:
            state1 = state_dict[state.name]
            for input_val in self.__input_list:
                next_state, output_val = state.next(input_val)
                new_input_val = input_map[input_val]
                new_next_state = state_dict[next_state.name]
                new_output_val = output_map[output_val]
                state1.set_next(new_input_val, new_next_state, new_output_val)

        return new_fsm

    def gen_dot_diagram(self, *, fout=sys.stdout):
        """GraphVizを使って状態遷移図を表す dot コードを出力する．

        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout が省略された場合，標準出力が使用される．
        """

        dotcode = self._dot_code()
        fout.write(dotcode)

    def gen_latex_diagram(self, *,
                          input_dict=None,
                          output_dict=None,
                          state_dict=None,
                          fout=sys.stdout):
        """GraphVizを使って状態遷移図を表す latex コードを出力する．

        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout が省略された場合，標準出力が使用される．
        """

        dotcode = self._dot_code(input_dict=input_dict,
                                 output_dict=output_dict,
                                 state_dict=state_dict)
        texcode = dot2tex(dotcode, texmode='raw')
        fout.write(texcode)

    def _dot_code(self, *,
                  input_dict=None,
                  output_dict=None,
                  state_dict=None):
        """Graphviz を使って状態遷移図を表すdotコードを作る．

        :param dict[str, str] input_dict: 出力用の入力記号の辞書
        :param dict[str, str] output_dict: 出力用の出力記号の辞書
        :param dict[str, str] state_dict: 出力用の状態名の辞書
        :return: dot コードを表す文字列を返す．
        """

        # 対象のグラフを作る．
        g = Digraph()

        # 状態を表すノードを作る．
        for state in self.__state_list:
            g.node(state.name, texlbl=label_str(state.name, state_dict))

        # 状態遷移を表す枝を作る．
        for state in self.__state_list:
            for input_val in self.__input_list:
                next_state, output_val = state.next(input_val)
                input_label = label_str(input_val, input_dict)
                output_label = label_str(output_val, output_dict)
                label = '{}/{}'.format(input_label, output_label)
                g.edge(state.name, next_state.name, "dummy", texlbl=label)

        return g.source


if __name__ == '__main__':

    i_0 = '0'
    i_1 = '1'
    input_list = (i_0, i_1)

    o_a = 'a'
    o_b = 'b'
    o_c = 'c'
    o_d = 'd'
    o_e = 'e'
    o_0 = '$\\epsilon$'

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

    input_map = {i_0: i_0, i_1: i_1}
    output_map = {o_a: '001', o_b: '010', o_c: '011',
                  o_d: '100', o_e: '101', o_0: '000'}
    state_map = {s0.name: '00', s1.name: '01', s11.name: '10', s111.name: '11'}

    new_fsm = fsm.encode(input_map, output_map, state_map)

    new_fsm.print_table()

    print('')

    new_fsm.gen_latex_table()

    print()
    new_fsm.gen_latex_compatible_table()

    new_fsm.gen_latex_diagram()
