# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                              compare_file.py                                #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                #
#     This script compares two files.                                         #
#                                                                             #
# Author     : cl                                                             #
# Version    : v1.1                                                           #
# CreateTime : 2024/03/29                                                     #
# License    : Copyright (c) 2024 by cl                                       #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import os
import re
import sys
import hashlib
import subprocess
import itertools
from datetime import datetime
from abc import ABCMeta, abstractmethod


def clean_file(func):
    """装饰器函数, 在比较前清洗文件，替换文件的金额类型"""
    def wrapper(self, file_a, file_b, log_file):
        # 对file_a开始清洗
        # clean_file_a = file_a if file_a.endswith('clean') else file_a + ".clean"
        clean_file_a = file_a + ".clean"

        f_out = open(clean_file_a, 'w')
        with open(file_a, 'r') as f_in:
           for line in f_in:
               # 1.替换 000.000格式数据为0                   " 00000000000000000000.000000"  ->   0
               new_line = re.sub(r'(@) 0+(0)\.0+(?=\D|$)', r'\1\2', line)
               # 2.替换正decimal整型前后的0以及删除小数点     " 00000000000000000100.000000"  ->   100
               new_line = re.sub(r'(@) 0+([0-9]*)\.0+(?=\D|$)', r'\1\2', new_line)
               # 3.替换负decimal整型前后的0以及删除小数点     "-00000000000000000100.000000"  ->   -100
               new_line = re.sub(r'(@-)0+([0-9]*)\.0+(?=\D|$)', r'\1\2', new_line)
               # 4.替换负decimal类型前后的0                  "-00000000000000000000.0002800" ->   -.00028
               new_line = re.sub(r'(@-)0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', new_line)
               # 5.替换正decimal类型前后的0，删除空格         " 00000000000000000000.0002800" ->   .00028
               new_line = re.sub(r'(@) 0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', new_line)
               # 6.替换正NULL类型中间的空格，删除空格         "@!@ @!@" ->   "@!@@!@"
               new_line = re.sub(r'(@[!|\|]@) (?=\D|$)', r'\1', new_line)
               f_out.write(new_line)
        f_out.close()
        return func(self, clean_file_a, file_b, log_file)
    return wrapper


def count_lines(filename):
    """计算文件的行数"""
    result = subprocess.run(['wc', '-l', filename], capture_output=True, text=True)
    output = result.stdout.strip()
    line_count = int(output.split()[0])
    return line_count


def remove_tmp_file():
    """清理多余的文件"""
    pass


def check_result(file_a, file_b, log_file):
    return {
        'file_a': None,
        'file_b': None,
        'sample_line_in_file_a' : None,
        'sample_line_in_file_b' : None,
        'result' : 'success'
    }


class FileCompare:
    """文件比较策略类抽象接口"""
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def compare(self, file_a, file_b, log_file):
        pass


class SortSmallFileCompare(FileCompare):
    """有序小文件对比，逐行对比"""
    @clean_file
    def compare(self, file_a, file_b, log_file="run_out.log"):
        with open(file_a, 'r') as f_a, open(file_b, 'r') as f_b, open(log_file, 'w') as log:
            line_number = 0
            log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), file_a, file_b))
            while True:
                line_a = f_a.readline()
                line_b = f_b.readline()
                if not line_a and not line_b:
                    break
                line_number += 1
                if line_a != line_b:
                    log.write("Line {}:\n{} \n{}".format(line_number, line_a.strip(), line_b.strip()))


class UnSortSmallFileCompare(FileCompare):
    """对比小文件，使用集合加减的方法对比"""
    @clean_file
    def compare(self, file_a, file_b, log_file="run_out.log"):
        with open(file_a, 'r') as f_a, open(file_b, 'r') as f_b, open(log_file, 'w') as log:
            lines_a = set(f_a.readlines())
            lines_b = set(f_b.readlines())

            common_lines = lines_a.intersection(lines_b)
            unique_lines_a = lines_a - common_lines

            if unique_lines_a:
                log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), file_a, file_b))
                for line in unique_lines_a:
                    log.write(line)


class UnSortLargeFileAllCompare(FileCompare):
    """全量对比无序大文本，内存可能会占用较大"""
    @staticmethod
    def hash_file_lines_dict(file: str) -> dict:
        """计算文件的每一行hash，存储行号跟哈希值到字典中"""
        hash_dict = {}
        with open(file, 'r') as file:
            for i, line in enumerate(file, start=1):
                line_hash = hashlib.md5(line.encode()).hexdigest()
                # Store the hash value and line number in the dictionary
                hash_dict[i] = line_hash
        return hash_dict

    @staticmethod
    def hash_file_lines_set(file: str) -> set:
        """计算文件的每一行hash，存储哈希值到集合中"""
        hash_set = set({})
        with open(file, 'r') as file:
            for i, line in enumerate(file, start=1):
                line_hash = hashlib.md5(line.encode()).hexdigest()
                # Store the hash value and line number in the set
                hash_set.add(line_hash)
        return hash_set

    @clean_file
    def compare(self, file_a, file_b, log_file):
        # 计算文件的每一行hash值
        hash_dict_a = self.hash_file_lines_dict(file_a)
        hash_set_b = self.hash_file_lines_set(file_b)

        # 写入差异行号到log文件中
        with open(log_file, 'w') as log:
            log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), file_a, file_b))
            for line_num, hash_val in hash_dict_a.items():
                if hash_val in hash_set_b:         # set判断元素在其中是O(1)复杂度，在这里使用if提前continue无法提升性能
                    log.write("line {} in\n".format(line_num))
                    continue
                else:
                    log.write("line {} out\n".format(line_num))


class UnSortLargeFileRandomCompare(UnSortLargeFileAllCompare):
    """抽样对比无序大文本"""
    def compare(self, file_a, file_b, log_file):
        # with open(file_a, 'r') as f_in:
        #     rows = ''.join(itertools.islice(f_in, 100))
        # with open(file_a, 'w') as f_out:
        #     f_out.write(rows)
        # os.system("head - 100 {} > {} && mv {} {}".format(file_a, random_file_a, random_file_a, file_b))
        super(UnSortLargeFileRandomCompare, self).compare(file_a, file_b, log_file)


class CompareContext:
    def __init__(self):
        self.compare_strategy = None

    def set_compare_strategy(self, compare_strategy):
        self.compare_strategy = compare_strategy

    def compare(self, file_a, file_b, log_file="run_out"):
        self.compare_strategy.compare(file_a, file_b, log_file)


def main():
    print("%s: begin to compare..." % str(datetime.now()))

    # 接收用户参数
    if len(sys.argv) < 2:
        raise ValueError("Parameter error,Usage: python compare_file.py <file_a_path> <file_b_path>")
    file_a = sys.argv[1]
    file_b = sys.argv[2]
    log_file = file_a + ".mismatch.log"
    random_compare = True

    # 判断两个文件的行数是否一致
    count_a = count_lines(file_a)
    count_b = count_lines(file_b)
    if count_a != count_b:
        with open(log_file, 'w') as f:
            f.write("The number of lines in two files is not equal\n%s=%s\n%s=%s" % (file_a, count_a, file_b, count_b))
        exit(-1)

    # 选择对比策略
    compare_file = CompareFile()
    if count_a <= 50 * 10000:  # 全文本对比，集合加减
        compare_file.set_compare_strategy(UnSortSmallFileCompare())
    elif random_compare:  # 抽样对比，取文件的前1000行
        file_a = file_a + '.random'
        os.system("head -1000 %s > %s" % (file_a[:-7], file_a))
        compare_file.set_compare_strategy(UnSortLargeFileRandomCompare())
    else:
        compare_file.set_compare_strategy(UnSortLargeFileAllCompare())

    # 开始比较
    compare_file.compare(file_a, file_b, log_file)

    # 将比较结果记录到日志
    result_di = check_result(file_a + '.clean', file_b, log_file)
    with open(log_file, 'a') as log:
        for k, v in result_di.items():
            log.write("%s: %s\n" % (k, v))

    remove_tmp_file()
    print("%s: end..." % str(datetime.now()))


if __name__ == "__main__":
    main()
