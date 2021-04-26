#! /usr/bin/env python3

"""Cover の実装ファイル

:file: cover.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2019 Yusuke Matsunaga, All rights reserved.
"""

import sys


class Cover:
    """カバー(キューブの集合)を表すクラス

    :param cube_list: キューブ(Cube)のリスト
    """

    def __init__(self, cube_list=None):
        if cube_list:
            self.__cube_list = cube_list
        else:
            self.__cube_list = []

    def add_cube(self, cube):
        """キューブ(Cube)を追加する．

        :param cube: 追加するキューブ
        """
        self.__cube_list.append(cube)

    @property
    def cube_num(self):
        """キューブ数を返す．"""
        return len(self.__cube_list)

    @property
    def literal_num(self):
        """リテラル数を返す．"""
        ans = 0
        for cube in self.__cube_list:
            ans += cube.literal_num
        return ans

    @property
    def cube_list(self):
        """キューブのリストを返す．"""
        return self.__cube_list

    def __getitem__(self, pos):
        """要素のキューブを取り出す．"""
        assert 0 <= pos < self.cube_num
        return self.__cube_list[pos]

    def latex_str(self, *, var_map=None):
        """積和形論理式を表す LaTeX 文字列を返す．

        :param var_map: 変数名の辞書(名前付きのオプション引数)
        """
        ans = ''
        plus = ''
        for cube in self.__cube_list:
            ans += plus
            plus = ' + '
            ans += cube.latex_str(var_map=var_map)
        return ans

    def DeMorgan_latex_str(self, *, var_map=None):
        """De Morgan の法則で否定した和積形論理式を表す LaTeX 文字列を返す．

        :param[in] var_map: 変数名の辞書(名前付きのオプション引数)
        """
        ans = ''
        for cube in self.__cube_list:
            ans += cube.DeMorgan_latex_str(var_map=var_map)
        return ans

    def print(self, *, fout=None):
        """内容を出力する．

        :param fout: 出力先のファイルオブジェクト(名前付きのオプション引数)

        fout が省略された場合は標準出力が用いられる．
        """
        if fout is None:
            fout = sys.stdout
        for cube in self.__cube_list:
            print(cube, file=fout)
