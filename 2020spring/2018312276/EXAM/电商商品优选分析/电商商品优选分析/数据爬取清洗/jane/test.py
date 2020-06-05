# !/usr/bin/env python
# -*- coding: utf-8 -*-,
# @File  : test.py
# @Desc  : 
# @Author: 
# @Time  : 2020/5/12 13:19
# @Version: 1.0
# @License : Copyright(C)，Drcnet
a = [{"a": 100, "b": 20}, {"a": 99, "b": 50}]
a.sort(key=lambda x: x["a"])
print(a)
