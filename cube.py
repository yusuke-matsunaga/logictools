#! /usr/bin/env python3

### @file cube.py
### @brief Cube の定義ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2017, 2019 Yusuke Matsunaga
### All rights reserved.

from lctools.bool3 import Bool3

### @class Cube
### @brief キューブを表すクラス
###
### 意味的には Bool3 の列(シーケンス)
### 入力数が高々10程度と仮定して符号なし整数１語で表す．
class Cube :

    ### @brief
    ### @brief 初期化
    ### @param[in] input_num 入力数
    ### @param[in] pat_str パタン文字列
    ###
    ### * input_num と pat_str のどちらか一方は指定されなければならない．
    ### * input_num と pat_str の両方が指定された場合，pat_str の長さは
    ###   input_num と等しくなければならない．
    ### * input_num のみが指定された場合の内容はすべてドントケアとなる．
    ### * pat_str は '0'，'1'，'-' or '*' からなる．
    ###   '0'は否定，'1'は肯定のリテラル，'-' と '*' はその変数が現れな
    ###   いことを示す．
    def __init__(self, *, input_num = None, pat_str = None) :
        assert input_num != None or pat_str != None
        if input_num != None and pat_str != None :
            assert len(pat_str) == input_num
        if input_num == None :
            input_num = len(pat_str)
        self.__input_num = input_num
        self.__body = 0
        if pat_str :
            for i in range(input_num) :
                pat = pat_str[i]
                if pat == '0' :
                    self.set_negliteral(i)
                elif pat == '1' :
                    self.set_posliteral(i)
                elif pat == '-' or pat == '*' :
                    self.clr_literal(i)
                else :
                    assert False

    ### @brief i 番目の変数を正のリテラルに設定する．
    ### @param[in] pos 変数番号 ( 0 <= pos < input_num )
    def set_posliteral(self, pos) :
        self[pos] = Bool3._1

    ### @brief i 番目の変数を負のリテラルに設定する．
    ### @param[in] pos 変数番号 ( 0 <= pos < input_num )
    def set_negliteral(self, pos) :
        self[pos] = Bool3._0

    ### @brief i 番目の変数をドントケアに設定する．
    ### @param[in] pos 変数番号 ( 0 <= pos < input_num )
    def clr_literal(self, pos) :
        self[pos] = Bool3._d

    ### @brief 包含関係を調べる．
    def contain(self, other) :
        assert isinstance(self, Cube)
        assert isinstance(other, Cube)
        assert self.input_num == other.input_num
        for i in range(self.input_num) :
            val_a = self[i]
            val_b = other[i]
            if val_a == Bool3._1 and val_b != Bool3._1 :
                return False
            elif val_a == Bool3._0 and val_b != Bool3._0 :
                return False
        return True

    ### @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ### @brief リテラル数を返す．
    @property
    def literal_num(self) :
        n = 0
        for i in range(self.input_num) :
            if self[i] != Bool3._d :
                n += 1
        return n

    ### @brief input_num の別名
    def __len__(self) :
        return self.__input_num

    ### @brief pos番目の位置のパタンを返す．
    ### @param[in] pos 位置 ( 0 <= pos < input_num )
    ### @retval Bool3._d ドントケア
    ### @retval Bool3._1 positive literal
    ### @retval Bool3._0 negative literal
    def __getitem__(self, pos) :
        assert 0 <= pos < self.input_num
        sft = self.__shift(pos)
        val = (self.__body >> sft) & 3
        if val == 0 :
            return Bool3._d
        elif val == 1 :
            return Bool3._1
        elif val == 2 :
            return Bool3._0

    ### @brief i 番目の変数のリテラルを設定する．
    ### @param[in] pos 変数番号 ( 0 <= pos < input_num )
    ### @param[in] val 値 ( Bool3 )
    def __setitem__(self, pos, val) :
        assert 0 <= pos < self.input_num
        sft = self.__shift(pos)
        msk = 3 << sft
        self.__body &= ~msk
        if val == Bool3._0 :
            self.__body |= (2 << sft)
        elif val == Bool3._1 :
            self.__body |= (1 << sft)
        elif val == Bool3._d :
            pass
        else :
            assert False

    ### 隣接したキューブをマージする．
    ### @param[in] self, other 対象のキューブ
    ### @return 結果のキューブを返す．
    ###
    ### 2つのキューブが隣接していなかった場合，None を返す．
    def __or__(self, other) :
        assert isinstance(self, Cube)
        assert isinstance(other, Cube)
        assert self.input_num == other.input_num
        nd = 0
        ans_pat = ""
        for i in range(self.input_num) :
            val_a = self[i]
            val_b = other[i]
            if val_a ^ val_b == Bool3._1 :
                nd += 1
                ans_pat += '-'
            elif val_a == val_b :
                if val_a == Bool3._0 :
                    ans_pat += '0'
                elif val_a == Bool3._1 :
                    ans_pat += '1'
                else :
                    ans_pat += '-'
            else :
                return None
        if nd == 1 :
            return Cube(pat_str = ans_pat)
        else :
            return None

    ### @biref 等価比較演算子
    def __eq__(self, other) :
        assert isinstance(self, Cube)
        assert isinstance(other, Cube)
        assert self.input_num == other.input_num
        for i in range(self.input_num) :
            val_a = self[i]
            val_b = other[i]
            if val_a != val_b :
                return False
        return True

    ### @brief 小なり比較演算子
    ###
    ### 各入力について Bool3._d < Bool3._1 < Bool3._0
    ### の順で比較を行う．
    def __lt__(self, other) :
        return self.__comp(other) == -1

    ### @brief 大なり比較演算子
    ###
    ### 各入力について Bool3._d < Bool3._1 < Bool3._0
    ### の順で比較を行う．
    def __gt__(self, other) :
        return self.__comp(other) == 1

    ### @brief 小なりイコール比較演算子
    ###
    ### 各入力について Bool3._d < Bool3._1 < Bool3._0
    ### の順で比較を行う．
    def __le__(self, other) :
        return self.__comp(other) <= 0

    ### @brief 大なりイコール比較演算子
    ###
    ### 各入力について Bool3._d < Bool3._1 < Bool3._0
    ### の順で比較を行う．
    def __ge__(self, other) :
        return self.__comp(other) >= 0

    ### @brief 比較関数
    def __comp(self, other) :
        assert isinstance(self, Cube)
        assert isinstance(other, Cube)
        assert self.input_num == other.input_num
        for i in range(self.input_num) :
            val_a = self[i]
            val_b = other[i]
            if val_a < val_b :
                return -1
            elif val_a > val_b :
                return 1
        return 0

    ### @brief ハッシュ関数
    def __hash__(self) :
        return self.__body

    ### @brief 内容を表すLaTex文字列を作る．
    ### @param[in] var_map 変数名の辞書
    def latex_str(self, *, var_map = None) :
        if var_map == None :
            var_map = {}
            for i in range(self.input_num) :
                var_map[i] = 'x_{}'.format(i + 1)
        cube_str = ""
        for i in range(self.input_num) :
            val = self[i]
            if val == Bool3._0 :
                cube_str += '\\bar{{{}}}'.format(var_map[i])
            elif val == Bool3._1 :
                cube_str += '{}'.format(var_map[i])
        if cube_str == '' :
            cube_str = '1'
        return cube_str

    ### @brief DeMorgan の法則で否定した和積形論理式を表すLaTex文字列を作る．
    ### @param[in] var_map 変数名の辞書
    def DeMorgan_latex_str(self, *, var_map = None) :
        if var_map == None :
            var_map = {}
            for i in range(self.input_num) :
                var_map[i] = 'x_{}'.format(i + 1)
        cube_str = '('
        plus = ''
        for i in range(self.input_num) :
            val = self[i]
            if val == Bool3._1 :
                cube_str += plus
                plus = ' + '
                cube_str += '\\bar{{{}}}'.format(var_map[i])
            elif val == Bool3._0 :
                cube_str += plus
                plus = ' + '
                cube_str += '{}'.format(var_map[i])
        cube_str += ')'
        return cube_str

    ### @brief 内容を表す文字列を作る．
    def __str__(self) :
        ans = ""
        for i in range(self.input_num) :
            val = self[i]
            if val == Bool3._0 :
                ans += '0'
            elif val == Bool3._1 :
                ans += '1'
            elif val == Bool3._d :
                ans += '-'
        return ans

    ### @brief __body 中のシフト量を計算する．
    def __shift(self, pos) :
        return (self.input_num - pos - 1) * 2


if __name__ == '__main__' :

    c1 = Cube(input_num = 4)
    print('c1 = {}: {}'.format(c1, c1.latex_str()))

    c2 = Cube(pat_str = '01--')
    print('c2 = {}: {}'.format(c2, c2.latex_str()))

    var_map = {0:'a', 1:'b', 2:'c', 3:'d'}
    print('c2\' = {}'.format(c2.latex_str(var_map = var_map)))

    print('\\bar{{c2}} = {}'.format(c2.DeMorgan_latex_str()))

    c3 = Cube(pat_str = '-1--')
    c23 = c2 | c3
    print('c2 | c3 = {}'.format(c23))

    c4 = Cube(pat_str = '11--')
    c24 = c2 | c4
    print('c2 | c4 = {}'.format(c24))
