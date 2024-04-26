
# 相对导入保证了对内导包不会出错，被外使用的时候不会出错，应该是用来做一个被使用工具包使用的
from ..abf import test_abf
from .aae import pppp


def test2():
    print("我是最里面的")


# test_abf()