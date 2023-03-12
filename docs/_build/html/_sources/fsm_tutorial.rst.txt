有限状態機械に関する処理
==========================

有限状態機械の生成
-------------------

有限状態機械は `lctools.Fsm` を用いて表す．
有限状態機械を生成するするためには入力記号と出力記号
および状態名のリストを名前付き引数として与える．

::

   from lctools import Fsm

   i_list = ['a', 'b', 'c']
   o_list = ['x', 'y']
   s_list = ['S0', 'S1', 'S2']

   fsm = Fsm(input_list=i_list,
             output_list=o_list,
	     state_list=s_list)


この時点では `fsm` は状態遷移を一つも持たない．
入力記号と出力記号，状態名は通常は文字列を用いるが，
実際には辞書のキーに用いることができるものであれば
どのようなデータ型でも用いることができる．
LaTeX 用の出力時には別の文字列を指定することができるので，
ここではただ単に他と区別可能な文字列を用いるのがよい．


状態遷移の追加
---------------

状態遷移の追加は `Fsm.add_transition(from_name, input_val, next_name, output_val)`
を用いる．

::

   fsm.add_transition(from_name, input_val, next_name, output_val)

`from_name` は遷移元の状態名，`input_val` は遷移を引き起こす入力記号，
`next_name` は遷移先の状態名，`output_val` はそのときの出力記号を指定
する．
`from_name` や `next_name` が存在しない場合にはエラーとなる．
`from_name` の `input_val` による遷移がすでに存在する場合にもエラーと
なる．


状態遷移情報の取得
-------------------

状態遷移情報の取得は `Fsm.get_transition(from_name, input_val)`
を用いる．

::

   next_name, output_val = fsm.get_transition(from_name, input_val)

`from_name` と `input_val` にそれぞれ遷移元の状態名，入力値を指定する．
結果として遷移先の状態名と出力値のタプルが返される．


状態数の最小化
----------------

等価状態を求めることで状態数の最小化を行う．

::

   new_fsm = fsm.minimize()

`new_fsm` には `fsm` と等価で状態数が最小の有限状態機械が返される．


符号化
----------

有限状態機械の入力記号，出力記号，状態名を2値符号化するには
`Fsm.encode()` を用いる．

::

   new_fsm = fsm.encode(input_map=imap,
                        output_map=omap,
			state_map=smap)

`input_map`, `output_map`, `state_map` にはそれぞれ入力記号，出力記号，
状態名をキーにして `0`, `1` のリストで表された2値ベクタを指定する．
この引数は省略不可の名前付き引数なので常に明示的に指定する必要がある．
結果として符号化した有限状態機械が返される．
この場合の入力記号，出力記号，状態名はすべて2値ベクタとなる．


状態遷移関数，出力関数の抽出
-------------------------------

2値符号化した有限状態機械の状態遷移関数，出力関数を取り出すには以下の
メソッドを用いる．

::

   delta_list, lambda_list = fsm.extract_functions(input_map=imap,
                                                   output_map=omap,
						   state_map=smap)

`input_map`, `output_map`, `state_map` にはそれぞれ入力記号，出力記号，
状態名をキーにして `0`, `1` のリストで表された2値ベクタを指定する．
この引数は省略不可の名前付き引数なので常に明示的に指定する必要がある．
結果として状態遷移関数と出力関数のリストがそれぞれ `delta_list` と
`lambda_list` に返される．
これらの関数は `BoolFunc` の形で表されている．


内容の出力
------------

有限状態機械の内容を出力するメソッドは以下の通り．

.. table::
   :align: left
   :widths: auto

   ================================ ================================================
   関数名                           説明
   ================================ ================================================
   print_table()                    内容を状態遷移表の形式で出力する．
   gen_latex_table()                状態遷移表を LaTeX 形式で出力する．
   gen_latex_encoded_table()        2値符号化した状態遷移表を LaTeX 形式で出力する．
   gen_latex_compatible_table()     等価状態の表を表す LaTeX 形式で出力する．
   gen_dot_diagram()                状態遷移図を `dot` 形式で出力する．
   gen_latex_diagram()              状態遷移図を LaTeX 形式で出力する．
   ================================ ================================================
