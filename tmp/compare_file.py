# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                                      compare_file.py                                        #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script compares two files.                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.1                                                                           #
# CreTime    : 2024/03/29                                                                     #
# License    : Copyright (c) 2024 by cl                                                       #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import os
import re
import sys
import hashlib
import subprocess
import itertools
from datetime import datetime
from abc import ABCMeta, abstractmethod


def read_file_by_line(file_name):
    """生成器函数, 惰性按行读取文件"""
    with open(file_name, 'r') as file:
        for line in file:
            yield line


def clean_file(rows):
    """装饰器函数, 在比较前清洗文件，替换文件的金额类型,可以选择全部清洗或者前1000行"""
    def decorator(func):
        def wrapper(self, file_a, file_b, log_file):
            # 选择要清洗的行数
            if rows.lower() == "all":                 # 全部清洗
                input_file = read_file_by_line(file_a)
            elif rows.lower() == "top1000":           # 清洗文件前1000行
                input_file = [ line for no, line in enumerate(read_file_by_line(file_a), start=0) if no<1000 ]
            else:
                raise ValueError("illegal parameter: %s" % str(rows))

            # 将清洗后的数据写入到clean_file_a文件
            out_file = file_a + ".clean"
            with open(out_file, 'w') as f_out:
                for line in input_file:
                    # 1.替换 000.000格式数据为0                 " 00000000000000000000.000000"  ->   0
                    new_line = re.sub(r'(@) 0+(0)\.0+(?=\D|$)', r'\1\2', line)
                    # 2.替换正decimal整型前后的0以及删除小数点     " 00000000000000000100.000000"  ->   100
                    new_line = re.sub(r'(@) 0+([0-9]*)\.0+(?=\D|$)', r'\1\2', new_line)
                    # 3.替换负decimal整型前后的0以及删除小数点     "-00000000000000000100.000000"  ->   -100
                    new_line = re.sub(r'(@-)0+([0-9]*)\.0+(?=\D|$)', r'\1\2', new_line)
                    # 4.替换负decimal类型前后的0                 "-00000000000000000000.0002800" ->   -.00028
                    new_line = re.sub(r'(@-)0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', new_line)
                    # 5.替换正decimal类型前后的0，删除空格         " 00000000000000000000.0002800" ->   .00028
                    new_line = re.sub(r'(@) 0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', new_line)
                    # 6.替换正NULL类型中间的空格，删除空格         "@!@ @!@" ->   "@!@@!@"
                    new_line = re.sub(r'(@[!|\|]@) (?=\D|$)', r'\1', new_line)
                    f_out.write(new_line)
            return func(self, out_file, file_b, log_file)
        return wrapper
    return decorator


def count_lines(filename):
    """计算文件的行数"""
    result = subprocess.run(['wc', '-l', filename], capture_output=True, text=True)
    output = result.stdout.strip()
    line_count = int(output.split()[0])
    return line_count


def remove_tmp_file():
    """清理多余的文件"""
    pass


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
    @clean_file("all")
    def compare(self, file_a, file_b, log_file="run_out.log"):
        with open(file_a, 'r') as f_a, open(file_b, 'r') as f_b, open(log_file, 'w') as log:
            line_number = 0
            # log.write(f"{str(datetime.now())}: lines in {file_a} but not in {file_b}.\n")
            while True:
                line_a = f_a.readline()
                line_b = f_b.readline()
                if not line_a and not line_b:
                    break
                line_number += 1
                if line_a != line_b:
                    log.write(f"Line {line_number}:\n{line_a.strip()} \n{line_b.strip()}")


class UnSortSmallFileCompare(FileCompare):
    """对比小文件，使用集合加减的方法对比"""
    @clean_file("all")
    def compare(self, file_a, file_b, log_file="run_out.log"):
        with open(file_a, 'r') as f_a, open(file_b, 'r') as f_b, open(log_file, 'w') as log:
            lines_a = set(f_a.readlines())
            lines_b = set(f_b.readlines())

            common_lines = lines_a.intersection(lines_b)
            unique_lines_a = lines_a - common_lines

            if unique_lines_a:
                # log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), file_a, file_b))
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

    def _compare(self, file_a, file_b, log_file):
        # 计算文件的每一行hash值
        hash_dict_a = self.hash_file_lines_dict(file_a)
        hash_set_b = self.hash_file_lines_set(file_b)

        # 写入差异行号到log文件中
        with open(log_file, 'w') as log:
            # log.write(f"{str(datetime.now())}: lines in {file_a} but not in {file_b}.\n")
            for line_no, hash_val in hash_dict_a.items():
                if hash_val in hash_set_b:         # set判断元素在其中是O(1)复杂度，在这里使用if提前continue无法提升性能
                    log.write(f"line {str(line_no)} in\n")
                    continue
                else:
                    log.write(f"line {str(line_no)} out\n")

    @clean_file("all")
    def compare(self, file_a, file_b, log_file):
        self._compare(file_a, file_b, log_file)


class UnSortLargeFileRandomCompare(UnSortLargeFileAllCompare):
    """抽样对比无序大文本"""
    @clean_file("top1000")
    def compare(self, file_a, file_b, log_file):
        # with open(file_a, 'r') as f_in:
        #     rows = ''.join(itertools.islice(f_in, 100))
        # with open(file_a, 'w') as f_out:
        #     f_out.write(rows)
        # os.system("head - 100 {} > {} && mv {} {}".format(file_a, random_file_a, random_file_a, file_b))
        super(UnSortLargeFileRandomCompare, self)._compare(file_a, file_b, log_file)


class CompareContext:
    def __init__(self):
        self.compare_strategy = None

    def set_compare_strategy(self, compare_strategy):
        self.compare_strategy = compare_strategy

    def compare(self, file_a, file_b, log_file="run_out"):
        self.compare_strategy.compare(file_a, file_b, log_file)


def check_result(clean_file, file_b, log_file) -> dict:
    """check logs file result, return the result."""
    clean_file_lines = count_lines(clean_file)
    log_file_lines = count_lines(log_file)

    if log_file_lines == 0:                       # definitely success
        compare_result = "success"
    elif log_file_lines == clean_file_lines:      # the eaual number of rows means that the tow files are likely to be the same.
        compare_result = "possible success"
    else:
        compare_result = "failed"

    # captute the same lines of clean_file and file_b, And then we can find the diffences by comparing those two line.
    process = subprocess.Popen(["head -1 %s" % clean_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    first_line_in_clean_file, err = process.communicate()
    first_line_li = [col.strip() for col in re.split('@[!|\|]@', first_line_in_clean_file) if col]

    pattern = '.*'.join(first_line_li[:2]) if len(first_line_li) <= 4 else '.*'.join(first_line_li[:5])
    process = subprocess.Popen(["grep %s %s | head -1" % (pattern, file_b)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    captute_line_in_file_b, err = process.communicate()

    return {
                "clean_file_rows"  : clean_file_lines,
                "log_file_rows"    : log_file_lines,
                "ds_sampling_line" : first_line_in_clean_file,
                "sh_sampling_line" : captute_line_in_file_b,
                "compare_result"   : compare_result
            }


def main():
    print("%s: begin to compare..." % str(datetime.now()))

    # 接收用户参数
    if len(sys.argv) < 2:
        raise ValueError("Parameter error,Usage: python compare_file.py <file_a_path> <file_b_path>")
    file_a = sys.argv[1]
    file_b = sys.argv[2]
    log_file = file_a + ".mismatch.txt"
    random_compare = True

    # 判断两个文件的行数是否一致
    count_a = count_lines(file_a)
    count_b = count_lines(file_b)
    if count_a != count_b:
        with open(log_file, 'w') as f:
            f.write("The number of lines in two files is not equal\n%s=%s\n%s=%s" % (file_a, count_a, file_b, count_b))
        exit(-1)

    # 选择对比策略
    compare_file = CompareContext()
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
