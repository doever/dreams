# encoding=utf-8
"""
两个使用不同程序分别从oracle的emp表导出的分隔符分割的txt格式文本文件，
需要对比文件是否完全一致，将不一致的行记录到log日志里面
emp表结构：emp_id int, emp_name varchar2(100), entry_date date, bonus number(15, 2), address text
文本文件A示例
00001@!@kimi@!@2021-01-01@!@2000.00@!@uuu
00002@!@diaz@!@1988-01-01@!@00000000000000.00@!@uuu
00003@!@phoebe@!@1958-01-01@!@3000.00@!@uuu
00004@!@nano@!@2018-04-01@!@1000.00@!@uuu

文本文件B示例
00001@!@kimi@!@2021-01-01@!@2000.00@!@uuu
00002@!@diaz@!@1988-01-01@!@0@!@uuu
00004@!@nano@!@2018-04-01@!@1000.00@!@uuu
"""
import os
import re
import sys
import hashlib
import subprocess
import itertools
from datetime import datetime
from abc import ABCMeta, abstractmethod


def clean_file(func):
    """装饰器函数，用于清洗文件"""
    print("clean...")

    def wrapper(self, file_a, file_b, log_file):
        print("clean123...")
        # 对 file_a 进行清洗
        clean_file_a = file_a if file_a.endswith('clean') else file_a + ".clean"
        with open(file_a, 'r') as f_in, open(clean_file_a, 'w') as f_out:
            for line in f_in:
                # 清洗文件内容
                line = re.sub(r'(@) 0+(0)\.0+(?=\D|$)', r'\1\2', line)
                line = re.sub(r'(@) 0+([0-9]*)\.0+(?=\D|$)', r'\1\2', line)
                line = re.sub(r'(@-)0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', line)
                line = re.sub(r'(@) 0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', line)
                f_out.write(line)
        # 调用被装饰的函数
        return func(self, clean_file_a, file_b, log_file)
    return wrapper


class FileCompare:
    __metaclass__ = ABCMeta

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
            print(common_lines)
            unique_lines_a = lines_a - common_lines
            print(unique_lines_a)

            if unique_lines_a:
                log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), file_a, file_b))
                for line in unique_lines_a:
                    log.write(line)


class UnSortLargeFileAllCompare(FileCompare):
    """全量对比无序大文本，内存可能会占用较大"""
    @staticmethod
    def file_hash_and_lines(file):
        hash_dict = {}
        with open(file, 'r') as file:
            for i, line in enumerate(file, start=1):
                # Calculate the hash of each line
                line_hash = hashlib.md5(line.encode()).hexdigest()
                # Store the hash value and line number in the dictionary
                hash_dict[line_hash] = i
        return hash_dict

    @clean_file
    def compare(self, file_a, file_b, log_file):
        # Calculate hashes and lines for each file
        print(file_a)
        hash_dict_a = self.file_hash_and_lines(file_a)
        hash_dict_b = self.file_hash_and_lines(file_b)

        # Find the differences between the two dictionaries
        diff_dict = {hash_val: line_info for hash_val, line_info in hash_dict_a.items() if hash_val not in hash_dict_b}

        # Write the differences to the log file
        with open(log_file, 'w') as log:
            log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), file_a, file_b))
            for hash_val, line_num in diff_dict.items():
                # log.write(f'Line {line_num} in {file_a}: {line_data} is missing from {file_b}\n')
                log.write("line {}\n".format(line_num))


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


def count_lines(filename):
    """计算文件的行数"""
    result = subprocess.run(['wc', '-l', filename], capture_output=True, text=True)
    output = result.stdout.strip()
    line_count = int(output.split()[0])
    return line_count


def remove_tmp_file():
    """清理多余的文件"""
    pass


def main():
    if len(sys.argv) < 2:
        raise ValueError("Parameter error,Usage: python compare_file.py <file_a_path> <file_b_path>")

    file_a = sys.argv[1]
    file_b = sys.argv[2]
    log_file = file_a + "_mismatch.log"
    strict = False

    # count_a = count_lines(file_a)
    # count_b = count_lines(file_b)
    count_a = 15
    count_b = 15

    if count_a != count_b:
        with open(file_a + "_mismatch.txt", 'w') as f:
            f.write("The number of lines in two files is not equal\n{}={}\n{}={}".format(file_a, count_a, file_b, count_b))
        exit(-1)

    # clean_file_a = clean_file(file_a)
    compare_context = CompareContext()
    if count_a <= 50 * 10000:
        print(1)
        # file_a = file_a + ".clean"
        # with open(file_a[:-6], 'r') as f_in:
        #     rows = ''.join(itertools.islice(f_in, 100))
        # with open(file_a, 'w') as f_out:
        #     f_out.write(rows)
        compare_context.set_compare_strategy(UnSortLargeFileRandomCompare())

    elif strict:
        print(2)
        compare_context.set_compare_strategy(UnSortLargeFileAllCompare())
    else:
        print(3)
        compare_context.set_compare_strategy(UnSortLargeFileRandomCompare())

    compare_context.compare(file_a, file_b, log_file)


if __name__ == "__main__":
    main()
