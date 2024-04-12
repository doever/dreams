# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                                    compare_file_py2.py                                      #
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
        def wrapper(self, file_a, file_b, mismatch_file):
            LOGGER.info("begin clean file...")
            # 选择要清洗的行数
            if rows.lower() == "all_rows":  # 全部清洗
                input_file = read_file_by_line(file_a)
            elif rows.lower() == "top_1000_rows":  # 清洗文件前1000行
                input_file = [line for no, line in enumerate(read_file_by_line(file_a), start=0) if no < 1000]
            else:
                LOGGER.error("illegal parameter: %s" % str(rows))
                raise ValueError("illegal parameter: %s" % str(rows))

            # 将清洗后的结果写入到clean_file_a文件
            out_file = file_a + ".clean.txt"
            with open(out_file, 'w') as f_out:
                for line in input_file:
                    # 1.替换 000.000格式数据为0                   " 00000000000000000000.000000"  ->   0
                    new_line = re.sub(r'(@) 0+(0)\.0+(?=\D|$)', r'\1\2', line)
                    # 2.替换正decimal整型前后的0以及删除小数点     " 00000000000000000100.000000"  ->   100
                    new_line = re.sub(r'(@) 0+([0-9]*)\.0*(?=\D|$)', r'\1\2', new_line)
                    # 3.替换负decimal整型前后的0以及删除小数点     "-00000000000000000100.000000"  ->   -100
                    new_line = re.sub(r'(@-)0+([0-9]*)\.0*(?=\D|$)', r'\1\2', new_line)
                    # 4.替换负decimal类型前后的0                  "-00000000000000000000.0002800" ->   -.00028
                    new_line = re.sub(r'(@-)0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', new_line)
                    # 5.替换正decimal类型前后的0，删除空格         " 00000000000000000000.0002800" ->   .00028
                    new_line = re.sub(r'(@) 0+([0-9]*\.)([0-9]*?)0*(?=\D|$)', r'\1\2\3', new_line)
                    # 6.替换正NULL类型中间的空格，删除空格         "@!@ @!@" ->   "@!@@!@"
                    new_line = re.sub(r'(@[!|\|]@) (?=\D|$)', r'\1', new_line)
                    f_out.write(new_line)
            return func(self, out_file, file_b, mismatch_file)
        return wrapper
    return decorator


def run_cmd(cmd_list):
    try:
        process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = process.communicate()
    except Exception as err:
        LOGGER.error(err)
        exit(-3)
    else:
        if err:
            LOGGER.error("execute %s command failed, %s" % (str(cmd_list), err))
            exit(-6)
        return output


def count_lines(filename):
    """计算文件行数"""
    if not os.path.isfile(filename):
        LOGGER.error("no such file <%s>, count lines failed." % filename)
        exit(-4)
    output = run_cmd(["wc -l %s" % filename])
    line_count = int(output.split()[0])
    return line_count


def remove_tmp_file():
    """清理多余的文件"""
    pass


class FileCompare:
    """抽象文件比较类接口"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def compare(self, file_a, file_b, mismatch_file):
        pass


class SortSmallFileCompare(FileCompare):
    """有序小文件对比，逐行对比"""

    @clean_file("all_rows")
    def compare(self, file_a, file_b, mismatch_file):
        # with open(file_a, 'r') as f_a, open(file_b, 'r') as f_b, open(mismatch_file, 'w') as f_log:
        LOGGER.info("Sort small file all compare...")
        f_log = open(mismatch_file, 'w')
        f_b = open(file_b, 'r')
        with open(file_a, 'r') as f_a:
            line_number = 0
            f_log.write("{}: lines in {} but not in {}.\n".format(str(datetime.now()), file_a, file_b))
            while True:
                line_a = f_a.readline()
                line_b = f_b.readline()
                if not line_a and not line_b:
                    break
                line_number += 1
                if line_a != line_b:
                    f_log.write("Line {}:\n{} \n{}".format(line_number, line_a.strip(), line_b.strip()))
        f_log.close()
        f_b.close()


class UnSortSmallFileCompare(FileCompare):
    """无序小文件对比，使用集合加减的方法对比"""
    @clean_file("all_rows")
    def compare(self, file_a, file_b, mismatch_file):
        LOGGER.info("UnSort small file set compare...")
        with open(file_a, 'r') as f_a:
            lines_a = set(f_a.readlines())
        with open(file_b, 'r') as f_b:
            lines_b = set(f_b.readlines())

        common_lines = lines_a.intersection(lines_b)
        unique_lines_a = lines_a - common_lines
        with open(mismatch_file, 'w') as log:
            if unique_lines_a:
                # log.write("%s: lines in %s but not in %s.\n" % (str(datetime.now()), file_a, file_b))
                for line in unique_lines_a:
                    log.write(line)


class UnSortLargeFileAllCompare(FileCompare):
    """全量对比无序大文本，内存可能会占用较大"""
    @staticmethod
    def file_hash_lines_dict(file):
        """将文件的每一行转成hash的字典"""
        hash_dict = {}
        with codecs.open(file, 'r', encoding='gb18030', errors='ignore') as file:
            for i, line in enumerate(file, start=1):
                try:
                    # 计算每一行hash value
                    line_hash = hashlib.md5(line.encode('gb18030')).hexdigest()
                    # 保存hash value和行号
                    hash_dict[i] = line_hash
                except Exception as err:
                    pass

        return hash_dict

    @staticmethod
    def file_hash_lines_set(file):
        """将文件的每一行转成hash的集合"""
        hash_set = set({})
        with codecs.open(file, 'r', encoding='gb18030', errors='ignore') as file:
            for i, line in enumerate(file, start=1):
                try:
                    # 计算每一行hash value
                    line_hash = hashlib.md5(line.encode('gb18030')).hexdigest()
                    # 保存hash value
                    hash_set.add(line_hash)
                except Exception as err:
                    pass

        return hash_set


def _compare(self, file_a, file_b, mismatch_file):
    # 将文件a,b的的每一行转换成哈希字典{line_hash_value: line_number, ...}
    LOGGER.info("hash files...")
    try:
        hash_dict_a = self.file_hash_lines_dict(file_a)
        hash_set_b = self.file_hash_lines_set(file_b)
    except MemoryError as err:  # 内存溢出
        LOGGER.error("run out of memory, %s" % err)
        del hash_dict_a, hash_set_b
        exit(-999)

    LOGGER.info("compare the hash value...")
    # 将不在文件B的hash value以及行号写入日志
    with open(mismatch_file, 'w') as mismatch_file:
        for line_no, hash_val in hash_dict_a.items():
            if hash_val in hash_set_b:
                # log.write("line %s\n in" % line_no)
                continue
            else:
                mismatch_file.write("line %s escaped.\n" % str(line_no))


@clean_file("all_rows")
def compare(self, file_a, file_b, mismatch_file):
    LOGGER.info("UnSort large file all compare...")
    self._compare(file_a, file_b, mismatch_file)


class UnSortLargeFileRandomCompare(UnSortLargeFileAllCompare):
    """抽样对比无序大文本"""

    @clean_file('top_1000_rows')
    def compare(self, file_a, file_b, mismatch_file):
        LOGGER.info("UnSort large file random compare...")
        # with open(file_a, 'r') as f_in:
        #    rows = ''.join(itertools.islice(f_in, 100))
        # with open(file_a, 'w') as f_out:
        #    f_out.write(rows)
        # os.system("head - 100 {} > {} && mv {} {}".format(file_a, random_file_a, random_file_a, file_b))
        super(UnSortLargeFileRandomCompare, self)._compare(file_a, file_b, mismatch_file)


class CompareFile:
    """比较策略上下文"""

    def __init__(self):
        self.compare_strategy = None

    def set_compare_strategy(self, compare_strategy):
        self.compare_strategy = compare_strategy

    def compare(self, file_a, file_b, mismatch_file):
        self.compare_strategy.compare(file_a, file_b, mismatch_file)


def check_result(clean_file, file_b, mismatch_file):
    """
        check logs file result, And return the result.
        args:
            clean_file: clean file absolute path
            file_b: file_b absolute path
            mismatch_file: mismatch file absolute path
        return:
            a dict such like: {"clean_file_rows": "1000", "mismatch_file_rows": "0", "sampling_line_a": "", "sampling_line_b": "", "compare_result": "success"}
    """

    clean_file_lines = count_lines(clean_file)
    mismatch_file_lines = count_lines(mismatch_file)

    if mismatch_file_lines == 0:  # definitely success
        compare_result = "success"
        return {
            "clean_file_rows": clean_file_lines,
            "mismatch_rows": mismatch_file_lines,
            "ds_sampling_line": "",
            "sh_sampling_line": "",
            "compare_result": compare_result
        }
    elif mismatch_file_lines == clean_file_lines:  # the eaual number of rows means that the tow files are likely to be the same.
        compare_result = "possible success"
    else:
        compare_result = "failed"

    # captute the same lines of clean_file and file_b, And then we can find the diffences by comparing those two line.
    first_mismatch_line = run_cmd(["head -1 %s" % mismatch_file])
    # if the contents of mismatch_line are only line numbers, find the corresponding line in the clean file accroding to the line numbers
    if first_mismatch_line.startswith("line"):
        mismatch_line_no = int(first_mismatch_line.split(' ')[1])
        first_mismatch_line = run_cmd(["head -%s %s | tail -1" % (str(mismatch_line_no + 1), mismatch_file)])

    first_line_li = [col.strip() for col in re.split('@[!|\|]@', first_mismatch_line) if col]

    pattern = '.*'.join(first_line_li[:2]) if len(first_line_li) <= 4 else '.*'.join(first_line_li[:5])
    captute_line_in_file_b = run_cmd(["grep %s %s | head -1" % (pattern, file_b)])

    return {
        "clean_file_rows": clean_file_lines,
        "mismatch_rows": mismatch_file_lines,
        "ds_sampling_line": first_mismatch_line,
        "sh_sampling_line": captute_line_in_file_b,
        "compare_result": compare_result
    }


def main():
    # 创建目录, 存放脚本生成的文件
    global BASE_PATH, LOGGER
    BASE_PATH = "/etl/dwexp/crm/log"
    run_cmd(["mkdir -p %s" % (os.path.join(BASE_PATH, 'compare'))])

    # 接收用户参数
    if len(sys.argv) <= 2:
        print("Parameter error, Usage: python compare_file.py <file_a_path> <file_b_path>")
        raise ValueError("Parameter error, Usage: python compare_file.py <file_a_path> <file_b_path>")
    file_a = sys.argv[1]
    file_b = sys.argv[2]
    mismatch_file = file_a + ".mismatch.txt"
    random_compare = True

    # 判断文件是否存在
    if not os.path.isfile(file_a) or not os.path.isfile(file_b):
        print("no such files <%s> or <%s>" % (file_a, file_b))
        exit(-1)

    # 定义日志对象
    log_file = file_a + ".run.log"
    logging.basicConfig(level=logging.INFO, filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')
    LOGGER = logging.getLogger("Compare")
    LOGGER.info("begin compare...")

    # 判断两个文件的行数是否一致
    count_a = count_lines(file_a)
    count_b = count_lines(file_b)
    if count_a != count_b:
        LOGGER.error("The number of lines in two files is not equal\n%s=%s\n%s=%s" % (file_a, count_a, file_b, count_b))
        exit(-2)

    # 选择对比策略
    compare_file = CompareFile()
    if count_a <= 10 * 10000:  # 全文本对比，集合加减
        compare_file.set_compare_strategy(UnSortSmallFileCompare())
    elif random_compare:  # 抽样对比，取文件的前1000行
        compare_file.set_compare_strategy(UnSortLargeFileRandomCompare())
    else:
        compare_file.set_compare_strategy(UnSortLargeFileAllCompare())

    # 开始比较
    compare_file.compare(file_a, file_b, mismatch_file)

    # 将比较结果记录到mismatch文件中
    result_di = check_result(file_a + '.clean.txt', file_b, mismatch_file)
    with open(mismatch_file, 'a') as f_mismatch_file:
        for k, v in result_di.items():
            f_mismatch_file.write("\n%s: %s" % (k, v))
            # LOGGER.info("%s: %s\n" % (k, v))

    # 移动生成的清洗文件，mismatch文件，程序日志文件到/etl/dwexp/crm/log/compare, 如果文件已存在就不覆盖
    for source_file in [mismatch_file, log_file, file_a + '.clean.txt']:
        file_name = os.path.split(source_file)[-1]
        target_dir = os.path.join(BASE_PATH, "compare")
        if not os.path.isfile(os.path.join(target_dir, file_name)):
            run_cmd(["mv %s %s" % (source_file, target_dir)])

    remove_tmp_file()
    LOGGER.info("end...")


if __name__ == "__main__":
    main()

# 小文件集合比较   18W  数据     8核心20G内存     内存消耗：0.4G     总耗时：  4min 30s
# 抽样比较        3000W数据     8核心20G内存     内存消耗：3.48G     总耗时： 9min 32s  {行数判断：1min  hash文件：6min  查找元素：2min}
