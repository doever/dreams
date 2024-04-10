# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                              clean_file.py.py                               #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                #
#     This script compares two files.                                         #
#                                                                             #
# Author     : cl                                                             #
# Version    : v1.0                                                           #
# CreateTime : 2024/4/10 9:05                                                 #
# License    : Copyright (c) 2024 by cl                                       #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import re

# 打开文件并读取内容
# with open('file_a.txt', 'r') as file:
#     content = file.read()
content = """00001000@!@aimi@!@2021-01-01@!@ 00000000000000000000.000000@!@uu1@!@ 00000000000000000000.000000
00002000@!@bimi@!@2022-01-01@!@-00000000000000000000.000028@!@uuua22@!@ 00000000000000000000.000000
00002000@!@bimi@!@2022-01-01@!@-00000000000000000000.00002800@!@uuua22@!@ 00000000000000000000.000000
00003001@!@cimi@!@2023-01-01@!@ 00000000000000000000.000028@!@uuua3@!@ 0003.00
00004001@!@cimi@!@2023-01-01@!@ 00000000000000000000.00002800@!@uuua3@!@ 0003.00
00005001@!@dimi@!@2024-01-01@!@ 00000000000000000100.000000@!@uuua4@!@ 0004.00
00006001@!@eimi@!@2025-01-01@!@ 00000000000000002515.825440@!@uuua5@!@ 00000000000000000000.000000
000070001@!@fimi@!@2026-01-01@!@-00000000000000002515.825440@!@uuua5@!@ 00000000000000000000.000000
00008001@!@himi@!@2027-01-01@!@ 00000000000000002515.825441@!@uuua5@!@ 00000000000000000000.000000
00009001@!@himi@!@2027-01-01@!@ 00000000000000002515.825441@!@uuua5@!@-00000000000000000000.002800
00010001@!@himi@!@2027-01-01@!@ 00000000000000002515.825441@!@uuua5@!@ 00000000000000000000.000028
00011001@!@himi@!@2027-01-01@!@ 00000000000000002515.825441@!@uuua5@!@ 00000000000000000000.000028000
00012001@!@himi@!@2027-01-01@!@ 00000000000000002515.825441@!@uuua5@!@-0000000000000012300.002800
00013001@!@himi@!@2027-01-01@!@ 00000000000000002515.825441@!@uuua5@!@ 0000000000000560000.000028
00014001@!@himi@!@2027-01-01@!@ 00000000000000002515.825441@!@uuua5@!@-00000000000008900.000028000"""

with open('file_a.txt', 'r') as file:
    content = file.read()
# 定义正则表达式模式，用于匹配数字后面的零
# pattern = r'(-?)0+(\.0*|\.[1-9][0-9]*)?'
# 使用 re.sub 函数进行替换
# new_content = re.sub(pattern, lambda x: x.group(1) + (x.group(2) or ''), content)

# a.
# 替换 000.000格式数据为0
# content = re.sub(r'(@) 0+(0)\.0+([@\n])', r'\1\2\3', content)
# 去除正decimal类型数字(小数点后第一位是0)两边多余的0,去除第一个空格
# content = re.sub(r'(@) 0+([0-9]*\.)|\.0+(?=\D|$)', r'\1\2', content)
# 去除负decimal类型数字(小数点后第一位是0)两边多余的0，保留负号
# content = re.sub(r'(@-)0+([0-9]*\.)|\.0+(?=\D|$)', r'\1\2', content)
# 去除decimal类型末尾的0
# content = re.sub(r'(\.\d*?)0+(?=\D|$)', r'\1', content)


# b.精确匹配
# 1.替换 000.000格式数据为0      " 00000000000000000000.000000"  ->   0
content = re.sub(r'(@) 0+(0)\.0+(?=\D|$)', r'\1\2', content)

# 2.替换decimal整十型前后的0以及删除小数点 " 00000000000000000100.000000"  ->   100
content = re.sub(r'(@) 0+([0-9]*)\.0+(?=\D|$)', r'\1\2', content)

# 3.替换负decimal类型前后的0   "-00000000000000000000.0002800" ->   -.00028
content = re.sub(r'(@-)0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', content)

# 4.替换正decimal类型前后的0，删除空格  " 00000000000000000000.0002800" ->   .00028
content = re.sub(r'(@) 0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', content)

print(content)







