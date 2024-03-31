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
00002@!@diaz@!@1988-01-01@!@0.00@!@uuu
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


class FileCompare:
    __metaclass__ = ABCMeta

    def __init__(self, file_a, file_b):
        self.file_a = file_a
        self.file_b = file_b
        self.log_file = file_a + "_mismatch.log"

    @abstractmethod
    def compare(self):
        pass


class SortSmallFileCompare(FileCompare):
    """有序小文件对比，逐行对比"""
    def compare(self):
        with open(self.file_a, 'r') as f_a, open(self.file_b, 'r') as f_b, open(self.log_file, 'w') as log:
            line_number = 0
            log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), self.file_a, self.file_b))
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
    def compare(self):
        with open(self.file_a, 'r') as f_a, open(self.file_b, 'r') as f_b, open(self.log_file, 'w') as log:
            lines_a = set(f_a.readlines())
            lines_b = set(f_b.readlines())

            common_lines = lines_a.intersection(lines_b)
            print(common_lines)
            unique_lines_a = lines_a - common_lines
            print(unique_lines_a)

            if unique_lines_a:
                log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), self.file_a, self.file_b))
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

    def compare(self):
        # Calculate hashes and lines for each file
        print(self.file_a)
        hash_dict_a = self.file_hash_and_lines(self.file_a)
        hash_dict_b = self.file_hash_and_lines(self.file_b)

        # Find the differences between the two dictionaries
        diff_dict = {hash_val: line_info for hash_val, line_info in hash_dict_a.items() if hash_val not in hash_dict_b}

        # Write the differences to the log file
        with open(self.log_file, 'w') as log:
            log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), self.file_a, self.file_b))
            for hash_val, line_num in diff_dict.items():
                # log.write(f'Line {line_num} in {file_a}: {line_data} is missing from {file_b}\n')
                log.write("line {}\n".format(line_num))


class UnSortLargeFileRandomCompare(UnSortLargeFileAllCompare):
    """抽样对比无序大文本"""
    def compare(self):
        with open(self.file_a, 'r') as f_in:
            rows = ''.join(itertools.islice(f_in, 100))
        with open(self.file_a, 'w') as f_out:
            f_out.write(rows)
        # os.system("head - 100 {} > {} && mv {} {}".format(self.file_a, random_file_a, random_file_a, self.file_b))
        super(UnSortLargeFileRandomCompare, self).compare()


class CompareFileStrategy:
    def __init__(self):
        self.compare_strategy = None

    def set_compare_strategy(self, compare_strategy):
        self.compare_strategy = compare_strategy

    def compare(self):
        self.compare_strategy.compare()


def count_lines(filename):
    """计算文件的行数"""
    result = subprocess.run(['wc', '-l', filename], capture_output=True, text=True)
    output = result.stdout.strip()
    line_count = int(output.split()[0])
    return line_count


def clean_file(input_file):
    """清理文件，替换文件的 00000.0000"""
    output_file = input_file + ".clean"
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            new_line = re.sub(r'(?<=@)\s*0*\.0*', '0', line)
            f_out.write(new_line)
    return output_file


def remove_tmp_file():
    """清理多余的文件"""
    pass


def main():
    if len(sys.argv) < 2:
        raise ValueError("Parameter error,Usage: python compare_file.py <file_a_path> <file_b_path>")

    file_a = sys.argv[1]
    file_b = sys.argv[2]
    strict = False

    # count_a = count_lines(file_a)
    # count_b = count_lines(file_b)
    count_a = 5
    count_b = 5

    if count_a != count_b:
        with open(file_a + "_mismatch.txt", 'w') as f:
            f.write("The number of lines in two files is not equal\n{}={}\n{}={}".format(file_a, count_a, file_b, count_b))
        exit(-1)

    clean_file_a = clean_file(file_a)
    compare_strategy = CompareFileStrategy()
    if count_a <= 50 * 10000:
        compare_strategy.set_compare_strategy(UnSortLargeFileRandomCompare(clean_file_a, file_b))
        # compare_strategy.set_compare_strategy(UnSortSmallFileCompare(clean_file_a, file_b))
    elif strict:
        compare_strategy.set_compare_strategy(UnSortLargeFileAllCompare(clean_file_a, file_b))
    else:
        compare_strategy.set_compare_strategy(UnSortLargeFileRandomCompare(clean_file_a, file_b))

    compare_strategy.compare()


if __name__ == "__main__":
    main()
