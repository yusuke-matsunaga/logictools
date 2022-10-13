#! /usr/bin/env python3

"""ハイパーキューブを描く dpic ソースを出力するスクリプト

:file: dpic_hc.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2020 Yusuke Matsunaga, All rights reserved.
"""

import sys
from logictools.bool3 import Bool3


head = R""".PS

dnl 単位長
define(`HC_UNIT', `30 * L_unit')dnl

dnl HC_UNIT によるスケーリング(1次元)
define(`HC_scalar', `$1 * HC_UNIT')dnl

dnl HC_UNIT によるスケーリング(2次元)
define(`HC_vect', `($1 * HC_UNIT, $2 * HC_UNIT)')dnl

define(`HC_D0001', `HC_vect(2.5, 0.3)')dnl
define(`HC_D0010', `HC_vect(0, 1)')dnl
define(`HC_D0100', `HC_vect(0.6, 0.3)')dnl
define(`HC_D1000', `HC_vect(1, 0)')dnl

G0000: HC_vect(0, 0)
G0001: G0000 + HC_D0001
G0010: G0000 + HC_D0010
G0011: G0000 + HC_D0001 + HC_D0010
G0100: G0000 + HC_D0100
G0101: G0000 + HC_D0100 + HC_D0001
G0110: G0000 + HC_D0100 + HC_D0010
G0111: G0000 + HC_D0100 + HC_D0010 + HC_D0001
G1000: G0000 + HC_D1000
G1001: G0000 + HC_D1000 + HC_D0001
G1010: G0000 + HC_D0010 + HC_D1000
G1011: G0000 + HC_D0010 + HC_D1000 + HC_D0001
G1100: G0000 + HC_D0100 + HC_D1000
G1101: G0000 + HC_D0100 + HC_D1000 + HC_D0001
G1110: G0000 + HC_D0100 + HC_D0010 + HC_D1000
G1111: G0000 + HC_D0100 + HC_D0010 + HC_D1000 + HC_D0001

ZERO: G0000 + HC_vect(-1.2, 0.2)
move to ZERO
arrow right thickness 1.5
"\Large{{{v0}}}" ljust
move to ZERO
arrow up right thickness 1.5
"\Large{{{v1}}}" above
move to ZERO
arrow up thickness 1.5
"\Large{{{v2}}}" above
move to ZERO
arrow up right 1.5 dashed thickness 1.5
"\Large{{{v3}}}" ljust

define(`HC_VERTEX',`dnl
define(`m4p', $1)dnl
define(`m4col', `ifelse(`$2',,"black",`$2')')dnl
circle shaded m4col outlined "black" radius HC_scalar(0.05) at G`'m4p
"\Large{{$1}}" at G`'m4p + HC_vect(0.2, -0.1)
')

define(`HC_LINE', `dnl
define(`m4dotted', `ifelse(`$3',,,`$3')')dnl
line from G`'$1 to G`'$2 thickness 1.5 m4dotted chop HC_scalar(0.05)
')

HC_LINE(0000, 0001, dashed)
HC_LINE(0000, 0010)
HC_LINE(0000, 0100)
HC_LINE(0000, 1000)

HC_LINE(0001, 0011)
HC_LINE(0001, 0101)
HC_LINE(0001, 1001)

HC_LINE(0010, 0011, dashed)
HC_LINE(0010, 0110)
HC_LINE(0010, 1010)

HC_LINE(0011, 0111)
HC_LINE(0011, 1011)

HC_LINE(0100, 0101, dashed)
HC_LINE(0100, 0110)
HC_LINE(0100, 1100)

HC_LINE(0101, 0111)
HC_LINE(0101, 1101)

HC_LINE(0110, 0111, dashed)
HC_LINE(0110, 1110)

HC_LINE(0111, 1111)

HC_LINE(1000, 1001, dashed)
HC_LINE(1000, 1010)
HC_LINE(1000, 1100)

HC_LINE(1001, 1011)
HC_LINE(1001, 1101)

HC_LINE(1010, 1011, dashed)
HC_LINE(1010, 1110)

HC_LINE(1011, 1111)

HC_LINE(1100, 1101, dashed)
HC_LINE(1100, 1110)

HC_LINE(1101, 1111)

HC_LINE(1110, 1111, dashed)
"""


def dpic_hc(func, *, var_map=None, fout=sys.stdout):
    """関数の幾何学的表現の図を描くための dpic ファイルを生成する．

    :param func: 対象の関数
    :param var_map: 変数名の辞書(名前付きのオプション引数)
    :param fout: 出力先のファイルオブジェクト(名前付きのオプション引数)

    fout が省略された場合には標準出力が用いられる．
    """

    if var_map is None:
        # デフォルトの変数名マップを作る．
        var_map = {i: 'x_{}'.format(i + 1)
                   for i in range(0, input_num)}

    fout.write(head.format(v0=var_map[0], v1=var_map[1],
                           v2=var_map[2], v3=var_map[3]))
    input_num = func.input_num
    nexp = 1 << input_num
    for p in range(0, nexp):
        cube_pat = ''
        val_list = []
        for i in range(0, input_num):
            if p & (1 << (input_num - i - 1)):
                pat = '1'
                val = Bool3._1
            else:
                pat = '0'
                val = Bool3._0
            cube_pat += pat
            val_list.append(val)
        if func.val(val_list) == Bool3._1:
            color = "black"
        else:
            color = "white"
        fout.write('HC_VERTEX({}, "{}")\n'.format(cube_pat, color))
    fout.write('.PE\n')
