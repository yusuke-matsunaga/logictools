#! /usr/bin/env python3

### @file parser.py
### @brief 論理式をパーズするクラス
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

from lctools.boolfunc import BoolFunc


### @brief トークンを表すクラス
class Token :

    ### @brief 初期化
    ### @param[in] token_id トークンID
    ### @param[in] var_id 変数番号
    def __init__(self, token_id, str_rep = None, var_id = 0) :
        self.__id = token_id
        if str_rep :
            self.__str = str_rep
        else :
            self.__str = token_id
        self.__var_id = var_id

    ### @brief トークンIDを返す．
    @property
    def id(self) :
        return self.__id

    ### @brief 変数番号を返す．
    @property
    def var_id(self) :
        return self.__var_id

    ### @brief 内容を表す文字列を返す．
    def to_string(self) :
        return self.__str

    ### @brief 内容を出力する
    def print(self) :
        if self.id == 'Var' :
            print('Var#{}'.format(self.var_id))
        else :
            print(self.id)


class Parser :

    ### @brief 初期化
    ### @param[in] input_numm 入力数
    ### @param[in] var_map 変数の辞書
    def __init__(self, input_num, var_map) :
        self.__input_num = input_num
        # コピーを作る．
        self.__varmap = dict(var_map)
        # 逆向きの辞書を作る．
        self.__idmap = dict()
        max_id = 0
        for varid, name in self.__varmap.items() :
            self.__idmap[name] = varid
            assert varid < input_num

        self.__buf_str = ""
        self.__token_list = list()
        self.__rpos = 0
        self.__emsg_list = list()


    ### @brief 文字列を読み込む．
    ### @param[in] expr_str 論理式を表す文字列
    def __call__(self, expr_str) :
        self.__emsg_list = list()
        self.__token_list = list()
        self.__rpos = 0
        ret = self.__lex_analyze(expr_str)
        if ret == False :
            return None

        return self.__parse_expr(None)


    def print_emsg(self) :
        for emsg in self.__emsg_list :
            print(emsg)


    ### @brief 字句解析を行う．
    def __lex_analyze(self, expr_str) :
        epos = len(expr_str)
        rpos = 0
        token_list = list()
        self.__buf_str = ""
        while rpos < epos :
            # 一文字読み出す．
            c = expr_str[rpos]
            rpos += 1

            if c == '0' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('0'))
            elif c == '1' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('1'))
            elif c == '(' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('('))
            elif c == ')' :
                self.__lex_flush_buf()
                self.__token_list.append(Token(')'))
            elif c == '*' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('*'))
            elif c == '&' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('*', '&'))
            elif c == '+' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('+'))
            elif c == '|' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('+', '|'))
            elif c == '^' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('^'))
            elif c == "'" :
                self.__lex_flush_buf()
                self.__token_list.append(Token("'"))
            elif c == '~' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('~'))
            elif c == '!' :
                self.__lex_flush_buf()
                self.__token_list.append(Token('~', '!'))
            elif c == ' ' or c == '\t' :
                self.__lex_flush_buf()
            else :
                self.__buf_str += c
        self.__lex_flush_buf()
        return len(self.__emsg_list) == 0


    def __lex_flush_buf(self) :
        if self.__buf_str != "" :
            # まず論理演算子のエイリアスのチェック
            tmp_str = self.__buf_str.lower()
            if tmp_str == 'zero' :
                self.__token_list.append(Token('0', 'zero'))
            elif tmp_str == 'one' :
                self.__token_list.append(Token('1', 'one'))
            elif tmp_str == 'and' :
                self.__token_list.append(Token('*', 'and'))
            elif tmp_str == 'or' :
                self.__token_list.append(Token('+', 'or'))
            elif tmp_str == 'xor' :
                self.__token_list.append(Token('^', 'xor'))
            elif tmp_str == 'not' :
                self.__token_list.append(Token('~', 'not'))
            else :
                # それ以外は変数名のみOK
                if self.__buf_str not in self.__idmap :
                    self.__emsg_list.append('Error: {} is not found.'.format(self.__buf_str))
                    # ここでは無視
                else :
                    var_id = self.__idmap[self.__buf_str]
                    self.__token_list.append(Token('Var', self.__buf_str, var_id))
            self.__buf_str = ''


    def __parse_expr(self, end_token) :

        func = self.__parse_product()

        while True :
            token = self.__read_token()
            if token is None or token.id == end_token :
                return func
            if token.id != '+' and token.id != '^' :
                self.__emsg_list.append('Error[parse_expr]: {}, unexpected'.format(token.to_string()))
                return None
            func1 = self.__parse_product()
            if func1 is None :
                return None

            if token.id == '+' :
                func |= func1
            else :
                func ^= func1


    def __parse_product(self) :
        func = self.__parse_primary()

        while True :
            token = self.__peek_token()
            if token is None or token.id != '*' :
                return func
            self.__read_token()
            func1 = self.__parse_primary()
            func &= func1


    def __parse_primary(self) :
        token = self.__read_token()
        if token.id == '0' :
            return BoolFunc.make_const0(self.__input_num, var_map = self.__varmap)
        if token.id == '1' :
            return BoolFunc.make_const1(self.__input_num, var_map = self.__varmap)
        if token.id == 'Var' :
            return BoolFunc.make_literal(self.__input_num, token.var_id, var_map = self.__varmap)
        if token.id == '~' :
            token = self.__read_token()
            if token.id == 'Var' :
                func1 = BoolFunc.make_literal(self.__input_num, token.var_id, var_map = self.__varmap)
            if token.id =='(' :
                func1 = self.__parse_expr(')')
            return ~func1
        if token.id == '(' :
            return self.__parse_expr(')')

        self.__emsg_list.append('Error[parse_primary]: {}, unexpected.'.format(token.to_string()))
        return None

    def __read_token(self) :
        if self.__rpos < len(self.__token_list) :
            token = self.__token_list[self.__rpos]
            self.__rpos += 1
            return token
        else :
            return None

    def __peek_token(self) :
        if self.__rpos < len(self.__token_list) :
            return self.__token_list[self.__rpos]
        else :
            return None

if __name__ == '__main__' :

    var_map = { 0: 'a',
                1: 'b',
                2: 'c',
                3: 'd' }
    parser = Parser(4, var_map)

    f1 = parser('a * b + c * d')

    if f1 :
        f1.print_table()
    else :
        parser.print_emsg()

    f2 = BoolFunc.make_from_string('(!a ^ b) xor (~c + d)', 4, var_map)

    if f2 :
        f2.print_table()
