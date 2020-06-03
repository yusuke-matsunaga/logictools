#! /usr/bin/env python3

### @file latex_karnaugh.py
### @brief BoolFunc から LaTeX 用のカルノー図記述を作るスクリプト
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2017, 2019, 2020 Yusuke Matsunaga
### All rights reserved.

from lctools.bool3 import Bool3


def __gen_implicant_str(func, cube) :
    input_num = func.input_num
    if input_num == 0 :
        # 無条件で決まる．
        return '\\implicant{0}'

    if input_num == 1 :
        if cube[0] == Bool3._d :
            return '\\implicant{0}{1}'
        elif cube[0] == Bool3._1 :
            return '\\implicant{1}{1}'
        elif cube[0] == Bool3._0 :
            return '\\implicant{0}{0}'
        else :
            assert False

    if input_num == 2 :
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

    if input_num == 3 :
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

    if input_num == 4 :
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


def latex_karnaugh(func, implicant_list, var_map, fout) :
        nexp = 1 << func.input_num

        # ヘッダの出力
        fout.write('\\begin{karnaugh-map}')
        if func.input_num == 0 :
            fout.write('[1][1][1][][]\n')
        elif func.input_num == 1 :
            fout.write('[1][2][1][][${}$]\n'.format(var_map[0]))
        elif func.input_num == 2 :
            fout.write('[2][2][1][${}$][${}$]\n'.format(var_map[0], var_map[1]))
        elif func.input_num == 3 :
            fout.write('[2][4][1][${}$][${}{}$]\n'.format(var_map[0], var_map[1], var_map[2]))
        elif func.input_num == 4 :
            fout.write('[4][4][1][${}{}$][${}{}$]\n'.format(var_map[0], var_map[1], var_map[2], var_map[3]))
        elif func.input_num == 5 :
            fout.write('Too many inputs.\n')
            return
        elif func.input_num == 6 :
            fout.write('Too many inputs.\n')
            return
        else :
            fout.write('Too many inputs.\n')
            return

        def make_val_list(p, input_num) :
            return [ Bool3._1 if p & (1 << i) else Bool3._0 for i in range(input_num) ]
        minterm_list = [ p for p in range(0, nexp) if func.val(make_val_list(p, func.input_num)) == Bool3._1 ]
        fout.write('\\minterms{')
        comma = ''
        for p in minterm_list :
            fout.write('{}{}'.format(comma, p))
            comma = ','
        fout.write('}\n')

        maxterm_list = [ p for p in range(0, nexp) if func.val(make_val_list(p, func.input_num)) == Bool3._0 ]
        fout.write('\\maxterms{')
        comma = ''
        for p in maxterm_list :
            fout.write('{}{}'.format(comma, p))
            comma = ','
        fout.write('}\n')

        fout.write('\\autoterms[$\\ast$]\n')

        if implicant_list :
            for cube in implicant_list :
                impl_str = __gen_implicant_str(func, cube)
                fout.write(impl_str)
                fout.write('\n')

        fout.write('\end{karnaugh-map}\n')
