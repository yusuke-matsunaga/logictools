#! /usr/bin/env python3

### @file karnaugh.py
### @brief BoolFunc カルノー図を作るスクリプト
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2017, 2019, 2020 Yusuke Matsunaga
### All rights reserved.

from lctools.bool3 import Bool3


### @brief 0変数のカルノー図を出力する．
def karnaugh0(func, var_map, fout) :
    fout.write('+-+\n')
    fout.write('|{:1}|\n'.format(func.val([])))
    fout.write('+-+\n')


### @brief 1変数のカルノー図を出力する．
def karnaugh1(func, var_map, fout) :
    fout.write('---+-+\n')
    fout.write(' 0 |{:1}|\n'.format(func.val([Bool3._0])))
    fout.write('---+-+\n')
    fout.write(' 1 |{:1}|\n'.format(func.val([Bool3._1])))
    fout.write('---+-+\n')

### @brief 2変数のカルノー図を出力する．
def karnaugh2(func, var_map, fout) :
    fout.write(' {:3}|0|1|\n'.format(var_map[1]))
    fout.write(' \  | | |\n')
    fout.write(' {:3}| | |\n'.format(var_map[0]))
    fout.write('----+-+-+\n')
    fout.write('  0 |{:1}|{:1}\n'.format(func.val([Bool3._0, Bool3._0]),
                                         func.val([Bool3._0, Bool3._1])))
    fout.write('----+-+-+\n')
    fout.write('  1 |{:1}|{:1}\n'.format(func.val([Bool3._1, Bool3._0]),
                                         func.val([Bool3._1, Bool3._1])))

### @brief 3変数のカルノー図を出力する．
def karnaugh3(func, var_map, fout) :
    fout.write(' {:3}{:3}|00|01|11|10|\n'.format(var_map[1], var_map[2]))
    fout.write('   \   |  |  |  |  |\n')
    fout.write('   {:3} |  |  |  |  |\n'.format(var_map[0]))
    fout.write('-------+--+--+--+--+\n')
    fout.write('   0   | {:1}| {:1}| {:1}| {:1}|\n'.format(func.val([Bool3._0, Bool3._0, Bool3._0]),
                                                           func.val([Bool3._0, Bool3._0, Bool3._1]),
                                                           func.val([Bool3._0, Bool3._1, Bool3._1]),
                                                           func.val([Bool3._0, Bool3._1, Bool3._0])))
    fout.write('-------+--+--+--+--+\n')
    fout.write('   1   | {:1}| {:1}| {:1}| {:1}|\n'.format(func.val([Bool3._1, Bool3._0, Bool3._0]),
                                                           func.val([Bool3._1, Bool3._0, Bool3._1]),
                                                           func.val([Bool3._1, Bool3._1, Bool3._1]),
                                                           func.val([Bool3._1, Bool3._1, Bool3._0])))

### @brief 4変数のカルノー図を出力する．
def karnaugh4(func, var_map, fout) :
    fout.write(' {:3}{:3}|00|01|11|10|\n'.format(var_map[2], var_map[3]))
    fout.write('   \   |  |  |  |  |\n')
    fout.write(' {:3}{:3}|  |  |  |  |\n'.format(var_map[0], var_map[1]))
    fout.write('-------+--+--+--+--+\n')
    fout.write('  00   | {:1}| {:1}| {:1}| {:1}|\n'.format(func.val([Bool3._0, Bool3._0, Bool3._0, Bool3._0]),
                                                           func.val([Bool3._0, Bool3._0, Bool3._0, Bool3._1]),
                                                           func.val([Bool3._0, Bool3._0, Bool3._1, Bool3._1]),
                                                           func.val([Bool3._0, Bool3._0, Bool3._1, Bool3._0])))
    fout.write('-------+--+--+--+--+\n')
    fout.write('  01   | {:1}| {:1}| {:1}| {:1}|\n'.format(func.val([Bool3._0, Bool3._1, Bool3._0, Bool3._0]),
                                                           func.val([Bool3._0, Bool3._1, Bool3._0, Bool3._1]),
                                                           func.val([Bool3._0, Bool3._1, Bool3._1, Bool3._1]),
                                                           func.val([Bool3._0, Bool3._1, Bool3._1, Bool3._0])))
    fout.write('-------+--+--+--+--+\n')
    fout.write('  11   | {:1}| {:1}| {:1}| {:1}|\n'.format(func.val([Bool3._1, Bool3._1, Bool3._0, Bool3._0]),
                                                           func.val([Bool3._1, Bool3._1, Bool3._0, Bool3._1]),
                                                           func.val([Bool3._1, Bool3._1, Bool3._1, Bool3._1]),
                                                           func.val([Bool3._1, Bool3._1, Bool3._1, Bool3._0])))
    fout.write('-------+--+--+--+--+\n')
    fout.write('  10   | {:1}| {:1}| {:1}| {:1}|\n'.format(func.val([Bool3._1, Bool3._0, Bool3._0, Bool3._0]),
                                                           func.val([Bool3._1, Bool3._0, Bool3._0, Bool3._1]),
                                                           func.val([Bool3._1, Bool3._0, Bool3._1, Bool3._1]),
                                                           func.val([Bool3._1, Bool3._0, Bool3._1, Bool3._0])))
