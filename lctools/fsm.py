#! /usr/bin/env python3

"""Fsm の実装ファイル

:file: fsm.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2019 Yusuke Matsunaga, All rights reserved.
"""

import sys
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

    def __init__(self, *,
                 input_list,
                 output_list,
                 state_list):
        """初期化

        :param list[str] input_list: 入力記号のリスト
        :param list[str] output_list: 出力記号のリスト
        :param list[str] state_list: 状態名のリスト

        この時点では状態遷移をもたない．
        """

        # 入力記号のリストと辞書を作る．
        self.__input_list = tuple(input_list)
        self.__input_dict = dict()
        for i, val in enumerate(self.__input_list):
            self.__input_dict[val] = i
        self.__ni = len(self.__input_list)
        # 出力記号のリストと辞書を作る．
        self.__output_list = tuple(output_list)
        self.__output_dict = dict()
        for i, val in enumerate(self.__output_list):
            self.__output_dict[val] = i
        self.__no = len(self.__output_list)
        # 状態名のリストと辞書を作る．
        self.__state_list = tuple(state_list)
        self.__state_dict = dict()
        for i, val in enumerate(self.__state_list):
            self.__state_dict[val] = i
        self.__ns = len(self.__state_list)
        # 状態遷移表を表す(1次元の)リストを作る．
        self.__transition_array = [None for _ in range(self.__ni * self.__ns)]

    def add_transition(self, from_name, input_val, next_name, output_val):
        """状態遷移を追加する．

        :param str from_name: 遷移元の状態名
        :param str input_val: 入力記号
        :param str next_name: 遷移先の状態名
        :param str output_val: 出力記号
        """
        assert input_val in self.__input_dict
        assert output_val in self.__output_dict
        assert from_name in self.__state_dict
        assert next_name in self.__state_dict
        input_id = self.__input_dict[input_val]
        from_id = self.__state_dict[from_name]
        next_id = self.__state_dict[next_name]
        output_id = self.__output_dict[output_val]
        self.__add_transition(from_id, input_id, next_id, output_id)

    def __add_transition(self, from_id, input_id, next_id, output_id):
        key = from_id * self.__ni + input_id
        assert self.__transition_array[key] is None
        self.__transition_array[key] = (next_id, output_id)

    def get_transition(self, from_name, input_val):
        """状態遷移の情報を得る．

        :param str from_name: 遷移元の状態名
        :param str input_val: 入力
        :return: (遷移先の状態名, 出力) のタプルを返す．
        """
        assert from_name in self.__state_dict
        assert input_val in self.__input_dict
        input_id = self.__input_dict[input_val]
        from_id = self.__state_dict[from_name]
        next_id, output_id = self.__get_transition(from_id, input_id)
        next_name = self.__state_list[next_id]
        output_val = self.__output_list[output_id]
        return next_name, output_val

    def __get_transition(self, s, i):
        key = s * self.__ni + i
        return self.__transition_array[key]

    def minimize(self):
        """最小化を行う．

        :return: 最小化した機械を返す．
        """
        self.__mark_dict = dict()
        phase = 0
        for s in range(self.__ns - 1):
            for t in range(s + 1, self.__ns):
                key = (s, t, phase)
                for i in range(self.__ni):
                    s1, o1 = self.__get_transition(s, i)
                    t1, o2 = self.__get_transition(t, i)
                    if o1 != o2:
                        self.__mark_dict[key] = False
                        break
                    if s1 != t1:
                        if key not in self.__mark_dict:
                            self.__mark_dict[key] = set()
                        if s1 > t1:
                            s1, t1 = t1, s1
                        self.__mark_dict[key].add((s1, t1))
                assert key in self.__mark_dict

        # 二周目以降
        while True:
            phase += 1
            changed = False
            for s in range(self.__ns - 1):
                for t in range(s + 1, self.__ns):
                    key = (s, t, phase - 1)
                    new_key = (s, t, phase)
                    if not self.__mark_dict[key]:
                        self.__mark_dict[new_key] = False
                        continue
                    self.__mark_dict[new_key] = set()
                    for s1, t1 in self.__mark_dict[key]:
                        self.__mark_dict[new_key].add((s1, t1))
                        key1 = (s1, t1, phase - 1)
                        if not self.__mark_dict[key1]:
                            self.__mark_dict[new_key] = False
                            changed = True
                            break
            if not changed:
                break
        self.__max_phase = phase + 1

        # 最小化したFSMを作る．
        state_map = dict()
        new_state_list = list()
        new_state_id_list = list()
        for s in range(self.__ns):
            if s in state_map:
                # 等価状態がある．
                continue
            s_name = self.__state_list[s]
            new_id = len(new_state_list)
            new_state_list.append(s_name)
            new_state_id_list.append(s)
            state_map[s] = new_id
            for t in range(s + 1, self.__ns):
                key = (s, t, self.__max_phase - 1)
                if self.__mark_dict[key]:
                    state_map[t] = new_id
        new_fsm = Fsm(input_list=self.__input_list,
                      output_list=self.__output_list,
                      state_list=new_state_list)
        for s in new_state_id_list:
            s1 = state_map[s]
            for i in range(self.__ni):
                t, o = self.__get_transition(s, i)
                t1 = state_map[t]
                new_fsm.__add_transition(s1, i, t1, o)
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
            n = len(label_str(state, state_dict))
            if max_n < n:
                max_n = n

        max_ino = max_i
        if max_ino < (max_n + max_o + 1):
            max_ino = max_n + max_o + 1

        # 先頭行の出力
        # 状態名の分の空白
        fout.write(' ' * max_n)
        for input_val in self.__input_list:
            input_label = label_str(input_val, input_dict)
            # 各入力記号
            fout.write('|')
            r = max_ino - len(input_label)
            r2 = r // 2
            fout.write(' ' * r2)
            fout.write(input_label)
            fout.write(' ' * (r - r2))
        fout.write('\n')

        for from_name in self.__state_list:
            from_label = label_str(from_name, state_dict)
            fout.write(from_label)
            n = max_n - len(from_label)
            fout.write(' ' * n)

            for input_val in self.__input_list:
                next_name, output_val = self.get_transition(
                    from_name, input_val)
                next_label = label_str(next_name, state_dict)
                output_label = label_str(output_val, output_dict)
                r1 = max_n - len(next_label)
                fout.write('|')
                fout.write(' ' * r1)
                fout.write(next_label)
                fout.write('/')
                fout.write(output_label)
                r2 = max_o - len(output_label)
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

        for from_name in self.__state_list:
            fout.write(label_str(from_name, state_dict))
            for input_val in self.__input_list:
                next_name, output_val = self.get_transition(
                    from_name, input_val)
                ns_label = label_str(next_name, state_dict)
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
            fout.write('{}'.format(encoded_str(state, state_map)))
            for input_val in self.__input_list:
                next_state, output_val = state.next(input_val)
                ns_str = encoded_str(next_state, state_map)
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
            for i in range(0, self.__ns - 1):
                fout.write('c|')
            fout.write('}\n')
            fout.write('\\cline{1-2}\n')
            for i in range(1, self.__ns):
                t = self.__state_list[i]
                fout.write(label_str(t, state_dict))
                for j in range(0, i):
                    fout.write(' & ')
                    s = self.__state_list[j]
                    key = (j, i, phase)
                    x = self.__mark_dict[key]
                    if x:
                        for s1_id, t1_id, in x:
                            s1 = self.__state_list[s1_id]
                            t1 = self.__state_list[t1_id]
                            s1_label = label_str(s1, state_dict)
                            t1_label = label_str(t1, state_dict)
                            fout.write(' ({}, {})'.format(s1_label, t1_label))
                    else:
                        fout.write('---')
                if i < self.__ns - 1:
                    fmt_str = ' & \\multicolumn{{{}}}{{|c}}{{}} \\\\ \\cline{{1-{}}}\n'
                    fout.write(fmt_str.format(self.__ns - i - 1, i + 2))
                else:
                    fout.write(' \\\\ \\hline \\hline\n')
            fout.write(' ')
            for i in range(0, self.__ns - 1):
                s = self.__state_list[i]
                fout.write(' & ')
                fout.write(label_str(s, state_dict))
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
        :return: 次状態関数，出力関数のリストを返す．
        """

        # 入力，出力，状態のビット長を得る．
        input_vec = input_map[self.__input_list[0]]
        ni = len(input_vec)
        output_vec = output_map[self.__output_list[0]]
        no = len(output_vec)
        state_vec = state_map[self.__state_list[0]]
        ns = len(state_vec)

        # 状態遷移関数，出力関数を作る．
        nfi = ni + ns
        nfi_exp = 1 << nfi
        delta_val_list = [
            [Bool3._d for i in range(nfi_exp)] for j in range(ns)]
        lambda_val_list = [
            [Bool3._d for i in range(nfi_exp)] for j in range(no)]
        for state in self.__state_list:
            state_vec = state_map[state]
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
                next_state, output_val = self.get_transition(state, input_val)
                next_vec = state_map[next_state]
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

    def encode(self, *, input_map, output_map, state_map):
        """符号化を行う．

        :param input_map: 入力の符号割当
        :param output_map: 出力の符号割当
        :param state_map: 状態の符号割当
        :return: 符号化を行った有限状態機械を返す．
        """
        new_input_list = [input_map[i] for i in self.__input_list]
        new_output_list = [output_map[i] for i in self.__output_list]
        new_state_list = [state_map[i] for i in self.__state_list]
        new_fsm = Fsm(input_list=new_input_list,
                      output_list=new_output_list,
                      state_list=new_state_list)

        for state in self.__state_list:
            new_state = state_map[state]
            for input_val in self.__input_list:
                next_state, output_val = self.get_transition(state, input_val)
                new_input_val = input_map[input_val]
                new_next_state = state_map[next_state]
                new_output_val = output_map[output_val]
                new_fsm.add_transition(new_state, new_input_val,
                                       new_next_state, new_output_val)
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

        :param dict[str, str] input_dict: 出力用の入力記号の辞書
        :param dict[str, str] output_dict: 出力用の出力記号の辞書
        :param dict[str, str] state_dict: 出力用の状態名の辞書
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
            g.node(state, texlbl=label_str(state, state_dict))

        # 状態遷移を表す枝を作る．
        for state in self.__state_list:
            for input_val in self.__input_list:
                next_state, output_val = self.get_transition(state, input_val)
                input_label = label_str(input_val, input_dict)
                output_label = label_str(output_val, output_dict)
                label = '{}/{}'.format(input_label, output_label)
                g.edge(state, next_state, "dummy", texlbl=label)

        return g.source


if __name__ == '__main__':

    fsm = Fsm(input_list=('0', '1'),
              output_list=('0', 'a', 'b', 'c', 'd', 'e'),
              state_list=('s0', 's1', 's2', 's3'))
    fsm.add_transition('s0', '0', 's0', 'b')
    fsm.add_transition('s0', '1', 's1', '0')
    fsm.add_transition('s1', '0', 's0', 'c')
    fsm.add_transition('s1', '1', 's2', '0')
    fsm.add_transition('s2', '0', 's0', 'a')
    fsm.add_transition('s2', '1', 's3', '0')
    fsm.add_transition('s3', '0', 's0', 'd')
    fsm.add_transition('s3', '1', 's0', 'e')

    fsm.print_table()

    print('')

    output_map = {'a': '$a$', 'b': '$b$', 'c': '$c$',
                  'd': '$d$', 'e': '$e$', '0': '$\epsilon$'}
    state_map = {'s0': '$S_{abcde}$', 's1': '$S_{acde}$',
                 's2': '$S_{ade}$', 's3': '$S_{de}$'}
    fsm.gen_latex_table(output_dict=output_map,
                        state_dict=state_map)

    print('')

    output_map = {'a': '$a$', 'b': '$b$', 'c': '$c$',
                  'd': '$d$', 'e': '$e$', '0': '$\epsilon$'}
    state_map = {'s0': '$S_{abcde}$', 's1': '$S_{acde}$',
                 's2': '$S_{ade}$', 's3': '$S_{de}$'}
    fsm.gen_latex_diagram(output_dict=output_map,
                          state_dict=state_map)

    print('')

    input_map = {'0': '0', '1': '1'}
    output_map = {'a': '001', 'b': '010', 'c': '011',
                  'd': '100', 'e': '101', '0': '000'}
    state_map = {'s0': '00', 's1': '01', 's2': '10', 's3': '11'}

    new_fsm = fsm.encode(input_map=input_map,
                         output_map=output_map,
                         state_map=state_map)

    new_fsm.print_table()

    print('')

    new_fsm.gen_latex_table()

    print()
    new_fsm.gen_latex_compatible_table()
