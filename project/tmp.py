# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                                 test.py                                     #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                #
#     This script compares two files.                                         #
#                                                                             #
# Author     : cl                                                             #
# Version    : v1.0                                                           #
# CreTime    : 2024/4/10 14:07                                                #
# License    : Copyright (c) 2024 by cl                                       #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


def decor(func):
    def wrapper(name):
        print("装饰器执行了...")
        return func(name)
    return wrapper


class A:
    def __init__(self):
        pass

    @decor
    def print_log(self):
        self._inside()

    def _inside(self):
        print('hello A world')


class B(A):
    """
    this class test the decor function

    args:
        word -> str : any word or text
    return:
        int : count of word
    """
    @decor
    def print_log(self):
        print('hello B')
        super()._inside()


def count_word(word):
    """
    this function counts the occurences of a word in a word

    args:
        word -> str : any word or text
    return:
        int : count of word
    """
    print(word)
    return 0


if __name__ == '__main__':
    # A().print_log()
    B().print_log()