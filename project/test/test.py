import sys
import os

# 将项目根目录添加到搜索路径中
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# print(1111111)
# print(os.path.dirname(os.path.dirname(__file__)))
# print(sys.path)
# print(1111111)
from a.af import af_print


af_print()
print(__file__)

# from b.bf import bf_print
#
# bf_print()