#! /usr/bin/env python3

"""Fsm の実装ファイル

:file: fsm.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2019 Yusuke Matsunaga, All rights reserved.
"""

import sys
from lctools.boolfunc import BoolFunc
from lctools.bool3 import Bool3
from lctools.eqtable import EqTable
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

    def make_eqtable(self):
        """等価状態のテーブルを得る．

        :return: EqTable を返す．
        """

        table = EqTable()
        step = 0
        for s_id in range(self.__ns - 1):
            for t_id in range(s_id + 1, self.__ns):
                cond_set = set()
                for i_id in range(self.__ni):
                    s1_id, o1_id = self.__get_transition(s_id, i_id)
                    t1_id, o2_id = self.__get_transition(t_id, i_id)
                    if o1_id != o2_id:
                        cond_set = None
                        break
                    if s1_id != t1_id:
                        cond_set.add((s1_id, t1_id))
                if cond_set is not None:
                    table.put(s_id, t_id, step, cond_set)
        changed = True
        while changed:
            step += 1
            changed = False
            for s_id in range(self.__ns - 1):
                for t_id in range(s_id + 1, self.__ns):
                    cond_set = table.get(s_id, t_id, step - 1)
                    if cond_set is not None:
                        for s1_id, t1_id in cond_set:
                            if table.get(s1_id, t1_id, step - 1) is None:
                                cond_set = None
                                changed = True
                                break
                        if cond_set is not None:
                            table.put(s_id, t_id, step, cond_set)
        return table

    def minimize(self, table):
        """最小化を行う．

        :param EqTable table: 等価状態対テーブル
        :return: 最小化した機械を返す．
        """

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
                if table.get(s, t) is not None:
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

        : param dict[str, str] input_dict: 出力用の入力記号の辞書
        : param dict[str, str] output_dict: 出力用の出力記号の辞書
        : param dict[str, str] state_dict: 出力用の状態名の辞書
        : param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

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

        : param dict[str, str] input_dict: 出力用の入力記号の辞書
        : param dict[str, str] output_dict: 出力用の出力記号の辞書
        : param dict[str, str] state_dict: 出力用の状態名の辞書
        : param state_label: 左上隅の左下側のラベル
        : param input_label: 左上隅の右上側のラベル．
        : param bool no_backslash: 左上隅のラベルを表示しない時に True にするフラグ
        : param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

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

    def gen_latex_eqtable_all(self, table, *,
                              state_dict=None,
                              fout=sys.stdout):
        """最小化のための等価状態テーブルを LaTeX 形式で出力する．

        :param EqTable table: 等価状態対テーブル
        :param dict[str, str] state_dict: 出力用の状態名の辞書
        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout が省略されば場合には標準出力を用いる．
        """

        for step in range(table.max_step + 1):
            fout.write('\n')
            fout.write('\\vspace{1cm}')
            fout.write('Step\#{}\n'.format(step + 1))
            self.gen_latex_eqtable(
                table, step, state_dict=state_dict, fout=fout)

    def gen_latex_eqtable(self, table, step, *,
                          state_dict=None,
                          fout=sys.stdout):
        """最小化のための等価状態テーブルを LaTeX 形式で出力する．

        :param EqTable table: 等価状態対テーブル
        :param int step: 対象のステップ
        :param dict[str, str] state_dict: 出力用の状態名の辞書
        :param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

        fout が省略されば場合には標準出力を用いる．
        """

        fout.write('\\begin{tabular}{|c||')
        for _ in range(self.__ns - 1):
            fout.write('c|')
        fout.write('}\n')
        fout.write('\\cline{1-2}\n')
        for i in range(1, self.__ns):
            t = self.__state_list[i]
            fout.write(label_str(t, state_dict))
            for j in range(i):
                fout.write(' & ')
                s = self.__state_list[j]
                cond_set = table.get(j, i, step)
                if cond_set is not None:
                    for s1_id, t1_id, in cond_set:
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
        for i in range(self.__ns - 1):
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

        : param input_map: 入力の符号割当
        : param output_map: 出力の符号割当
        : param state_map: 状態の符号割当
        : return: 次状態関数，出力関数のリストを返す．
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

    def gen_dot_diagram(self, *, fout=sys.stdout):
        """GraphVizを使って状態遷移図を表す dot コードを出力する．

        : param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

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

        : param dict[str, str] input_dict: 出力用の入力記号の辞書
        : param dict[str, str] output_dict: 出力用の出力記号の辞書
        : param dict[str, str] state_dict: 出力用の状態名の辞書
        : param fout: 出力先のファイルオブジェクト(名前付きオプション引数)

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

        : param dict[str, str] input_dict: 出力用の入力記号の辞書
        : param dict[str, str] output_dict: 出力用の出力記号の辞書
        : param dict[str, str] state_dict: 出力用の状態名の辞書
        : return: dot コードを表す文字列を返す．
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

    table = fsm.make_eqtable()
    fsm.gen_latex_eqtable_all(table)
    print('')

    input_map = {'0': '0', '1': '1'}
    output_map = {'a': '001', 'b': '010', 'c': '011',
                  'd': '100', 'e': '101', '0': '000'}
    state_map = {'s0': '00', 's1': '01', 's2': '10', 's3': '11'}
    delta_list, lambda_list = fsm.extract_functions(input_map={'0': (0, ), '1': (1, )},
                                                    output_map={'a': (0, 0, 1),
                                                                'b': (0, 1, 0),
                                                                'c': (0, 1, 1),
                                                                'd': (1, 0, 0),
                                                                'e': (1, 0, 1),
                                                                '0': (0, 0, 0)},
                                                    state_map={'s0': (0, 0),
                                                               's1': (0, 1),
                                                               's2': (1, 0),
                                                               's3': (1, 1)})

    for func in delta_list:
        func.gen_latex_karnaugh()

    for func in lambda_list:
        func.gen_latex_karnaugh()
