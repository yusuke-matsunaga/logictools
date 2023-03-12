.. lctools documentation master file, created by
   sphinx-quickstart on Mon Apr 26 19:07:40 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LCTools: 論理回路の学習用ツール
===================================

LCTools は L(ogic) C(ircuit) Tools の略で，
論理回路に対する数学モデルである論理関数と有限状態機械
を使った簡単なプログラミングが行えるように用意された
いくつからのクラスからなるPythonパッケージである．
具体的には論理関数を表す 'lctools.BoolFunc' と
有限状態機械を表す 'lctools.Fsm' からなる．


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   function_tutorial
   sop_tutorial
   mincov_tutorial
   fsm_tutorial
   modules/modules

.. autosummary::

   lctools


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
