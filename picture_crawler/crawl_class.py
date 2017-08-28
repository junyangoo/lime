# -*-coding:utf-8 -*-
# !/usr/bin/python

from abc import *


class C:
    __metaclass__ = ABCMeta
    # @abstractproperty
    def a(self):
        print 'hello'
    def b(self):
        print 'This is StractClass'


class B(C):
    pass
    # def a(self):
    #     print 'alive'


x = B()
x.a()