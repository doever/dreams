import sys
import os

# # 将项目根目录添加到搜索路径中
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

print(sys.path)
from .aa.aaf import test2


def af_print():
    test2()
    print("af_print")


if __name__ == '__main__':
    test2()
