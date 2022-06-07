#! /usr/bin/env python3

"""論理式をパーズするクラス

:file: parser.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2020 Yusuke Matsunaga, All rights reserved.
"""

from lctools.boolfunc import BoolFunc


class Token:
    """トークンを表すクラス

    :paramt token_id: トークンID
    :param str_rep: 文字列表現
    :param var_id: 変数番号
    """
    def __init__(self, token_id, str_rep=None, var_id=0):
        self.__id = token_id
        if str_rep:
            self.__str = str_rep
        else:
            self.__str = token_id
        self.__var_id = var_id

    @property
    def id(self):
        """トークンIDを返す．"""
        return self.__id

    @property
    def var_id(self):
        """変数番号を返す．"""
        return self.__var_id

    def to_string(self):
        """内容を表す文字列を返す．"""
        return self.__str

    def print(self):
        """内容を出力する"""
        if self.id == 'Var':
            print('Var#{}'.format(self.var_id))
        else:
            print(self.id)


class Parser:
    """論理式をパーズするためのクラス

    :param input_numm: 入力数
    :param var_map: 変数の辞書
    """
    def __init__(self, input_num, var_map):
        self.__input_num = input_num
        # コピーを作る．
        self.__varmap = dict(var_map)
        # 逆向きの辞書を作る．
        self.__idmap = dict()
        max_id = 0
        for varid, name in self.__varmap.items():
            self.__idmap[name] = varid
            assert varid < input_num
        self.__buf_str = ""
        self.__token_list = list()
        self.__rpos = 0
        self.__first = True
        self.__emsg_list = list()

    def __call__(self, expr_str):
        """パーズする．

        :param expr_str: 論理式を表す文字列
        """
        self.__emsg_list = list()
        self.__token_list = list()
        self.__rpos = 0
        if not self.__lex_analyze(expr_str):
            self.print_emsg()
            return None

        return self.__parse_expr(None)

    def print_emsg(self):
        """エラーメッセージを出力する．"""
        for emsg in self.__emsg_list:
            print(emsg)

    def __lex_analyze(self, expr_str):
        """字句解析を行う．"""
        epos = len(expr_str)
        rpos = 0
        token_list = list()
        self.__buf_str = ""
        self.__first = True
        while rpos < epos:
            # 一文字読み出す．
            c = expr_str[rpos]
            rpos += 1

            if self.__first and c == '0':
                self.__lex_flush_buf()
                self.__token_list.append(Token('0'))
            elif self.__first and c == '1':
                self.__lex_flush_buf()
                self.__token_list.append(Token('1'))
            elif c == '(':
                self.__lex_flush_buf()
                self.__token_list.append(Token('('))
            elif c == ')':
                self.__lex_flush_buf()
                self.__token_list.append(Token(')'))
            elif c == '*':
                self.__lex_flush_buf()
                self.__token_list.append(Token('*'))
            elif c == '&':
                self.__lex_flush_buf()
                self.__token_list.append(Token('*', '&'))
            elif c == '+':
                self.__lex_flush_buf()
                self.__token_list.append(Token('+'))
            elif c == '|':
                self.__lex_flush_buf()
                self.__token_list.append(Token('+', '|'))
            elif c == '^':
                self.__lex_flush_buf()
                self.__token_list.append(Token('^'))
            elif c == "'":
                self.__lex_flush_buf()
                self.__token_list.append(Token("'"))
            elif c == '~':
                self.__lex_flush_buf()
                self.__token_list.append(Token('~'))
            elif c == '!':
                self.__lex_flush_buf()
                self.__token_list.append(Token('~', '!'))
            elif c == ' ' or c == '\t':
                self.__lex_flush_buf()
            else:
                self.__first = False
                self.__buf_str += c
        self.__lex_flush_buf()
        return len(self.__emsg_list) == 0

    def __lex_flush_buf(self):
        self.__first = True
        if self.__buf_str != "":
            # まず論理演算子のエイリアスのチェック
            tmp_str = self.__buf_str.lower()
            if tmp_str == 'zero':
                self.__token_list.append(Token('0', 'zero'))
            elif tmp_str == 'one':
                self.__token_list.append(Token('1', 'one'))
            elif tmp_str == 'and':
                self.__token_list.append(Token('*', 'and'))
            elif tmp_str == 'or':
                self.__token_list.append(Token('+', 'or'))
            elif tmp_str == 'xor':
                self.__token_list.append(Token('^', 'xor'))
            elif tmp_str == 'not':
                self.__token_list.append(Token('~', 'not'))
            else:
                # それ以外は変数名のみOK
                if self.__buf_str not in self.__idmap:
                    emsg = 'Error: {} is not found.'.format(self.__buf_str)
                    self.__emsg_list.append(emsg)
                    # ここでは無視
                else:
                    var_id = self.__idmap[self.__buf_str]
                    tok = Token('Var', self.__buf_str, var_id)
                    self.__token_list.append(tok)
            self.__buf_str = ''

    def __parse_expr(self, end_token):
        func = self.__parse_product()
        while True:
            token = self.__read_token()
            if token is None or token.id == end_token:
                return func
            if token.id != '+' and token.id != '^':
                emsg = 'Error[parse_expr]: {}, unexpected'.format(token.to_string())
                self.__emsg_list.append(emsg)
                return None
            func1 = self.__parse_product()
            if func1 is None:
                return None

            if token.id == '+':
                func |= func1
            else:
                func ^= func1

    def __parse_product(self):
        func = self.__parse_primary()
        while True:
            token = self.__peek_token()
            if token is None or token.id != '*':
                return func
            self.__read_token()
            func1 = self.__parse_primary()
            func &= func1

    def __parse_primary(self):
        token = self.__read_token()
        if token.id == '0':
            return BoolFunc.make_const0(self.__input_num)
        if token.id == '1':
            return BoolFunc.make_const1(self.__input_num)
        if token.id == 'Var':
            return BoolFunc.make_literal(self.__input_num, token.var_id)
        if token.id == '~':
            token = self.__read_token()
            if token.id == 'Var':
                func1 = BoolFunc.make_literal(self.__input_num, token.var_id)
            if token.id == '(':
                func1 = self.__parse_expr(')')
            return ~func1
        if token.id == '(':
            return self.__parse_expr(')')

        emsg = 'Error[parse_primary]: {}, unexpected.'.format(token.to_string())
        self.__emsg_list.append(emsg)
        return None

    def __read_token(self):
        if self.__rpos < len(self.__token_list):
            token = self.__token_list[self.__rpos]
            self.__rpos += 1
            return token
        else:
            return None

    def __peek_token(self):
        if self.__rpos < len(self.__token_list):
            return self.__token_list[self.__rpos]
        else:
            return None


if __name__ == '__main__':

    var_map = {0: 'a',
               1: 'b',
               2: 'c',
               3: 'd'}
    parser = Parser(4, var_map)

    f1 = parser('a * b + c * d')

    if f1:
        f1.print_table()
    else:
        parser.print_emsg()

    f2 = BoolFunc.make_from_string('(!a ^ b) xor (~c + d)', 4, var_map)

    if f2:
        f2.print_table()

    var_map2 = {0:'x_0',
                1:'x_1',
                2:'x_2',
                3:'x_3'}
    parser2 = Parser(4, var_map2)
    f3 = parser2('x_0 * x_1 + x_2 * x_3')
    if f3:
        f3.print_table()
    else:
        parser.print_emsg()
