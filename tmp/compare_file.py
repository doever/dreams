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
使用python实现，不要使用第三方库
"""
import sys
import hashlib
import subprocess
from datetime import datetime
from abc import ABC, abstractmethod


class FileCompare(ABC):
    def __init__(self, file_a, file_b):
        self.file_a = file_a
        self.file_b = file_b
        self.log_file = file_a + "_mismatch.log"

    @abstractmethod
    def compare(self):
        pass


class SmallSortFileCompare(FileCompare):
    """对比小文件，使用集合加减的方法对比，内存可能溢出"""
    def compare(self):
        with open(self.file_a, 'r') as f_a, open(self.file_b, 'r') as f_b, open(self.log_file, 'w') as log:
            lines_a = set(f_a.readlines())
            lines_b = set(f_b.readlines())

            common_lines = lines_a.intersection(lines_b)
            print(common_lines)
            unique_lines_a = lines_a - common_lines
            print(unique_lines_a)
            unique_lines_b = lines_b - common_lines

            if unique_lines_a:
                log.write("Lines present in {} but not in {}: \n".format(self.file_a, self.file_b))
                for line in unique_lines_a:
                    log.write(line)

            if unique_lines_b:
                log.write("Lines present in {} but not in {}: \n".format(self.file_b, self.file_a))
                for line in unique_lines_b:
                    log.write(line)


class LargeUnSortFileCompare(FileCompare):
    """对比无序大文本，内存可能会占用较大"""
    def compare(self):
        # Calculate hashes and lines for each file
        hash_dict_a = self.file_hash_and_lines(self.file_a)
        hash_dict_b = self.file_hash_and_lines(self.file_b)

        # Find the differences between the two dictionaries
        diff_dict = {hash_val: line_info for hash_val, line_info in hash_dict_a.items() if hash_val not in hash_dict_b}

        # Write the differences to the log file
        with open(self.log_file, 'w') as log:
            log.write(f"{str(datetime.now())}: the result of {self.file_a} minus {self.file_b}.")
            for hash_val, (line_num, line_data) in diff_dict.items():
                # log.write(f'Line {line_num} in {file_a}: {line_data} is missing from {file_b}\n')
                log.write(f'line {line_num}\n')

    @staticmethod
    def file_hash_and_lines(file):
        hash_dict = {}
        with open(file, 'r') as file:
            for i, line in enumerate(file, start=1):
                # Calculate the hash of each line
                line_hash = hashlib.md5(line.encode()).hexdigest()
                # Store the hash value and line number in the dictionary
                hash_dict[line_hash] = (i, line.strip())
        return hash_dict


def count_lines(filename):
    result = subprocess.run(['wc', '-l', filename], capture_output=True, text=True)
    output = result.stdout.strip()
    line_count = int(output.split()[0])
    return line_count


def compare_files2(file_a, file_b, log_file):
    """逐行对比，需要文件排序，如果有错序会导致记录大量数据"""
    with open(file_a, 'r') as f_a, open(file_b, 'r') as f_b, open(log_file, 'w') as log:
        line_number = 0
        while True:
            line_a = f_a.readline()
            line_b = f_b.readline()
            if not line_a and not line_b:
                break
            line_number += 1
            if line_a != line_b:
                log.write(f'Line {line_number}: {line_a.strip()} != {line_b.strip()}\n')



def main():
    if len(sys.argv) != 2:
        raise ValueError("Parameter error,Usage: python compare_file.py <file_a_path> <file_b_path>")

    file_a = sys.argv[1]
    file_b = sys.argv[2]
    log_file_path = file_a + "_mismatch.log"

    if count_lines(file_a) != count_lines(file_b):
        pass
    else:
        pass

    # compare_unsort_large_files(file_a, file_b, log_file_path)


if __name__ == "__main__":
    main()

