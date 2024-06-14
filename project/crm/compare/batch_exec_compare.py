# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 batch_exec_compare1.py                                      #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script compares two files.                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/4/11 16:08                                                                #
# License    : Copyright (c) 2024 by cl                                                       #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import re
import os
import sys
import time
import random
import logging
from multiprocessing import Pool


def replace_file_name(files_tuple):
    ds_file = re.sub(r"yyyymmdd", WORK_DT, files_tuple[0])
    sh_file = re.sub(r"yyyymmdd", WORK_DT, files_tuple[1])

    if ds_file.endswith("gz"):
        os.system("gunzip %s" % ds_file)
        os.system("gunzip %s" % sh_file)
        ds_file = ds_file[:-3]
        sh_file = sh_file[:-3]
    return ds_file, sh_file


def run_compare(files_tuple):
    """执行比对任务的函数"""
    ds_file, sh_file = replace_file_name(files_tuple)
    print("begin compare <%s> --> <%s>" % (ds_file, sh_file))
    # time.sleep(100)
    if not os.path.isfile(ds_file) or not os.path.isfile(sh_file):
        LOGGER.warning("the file is not exist, compare script not really work: %s %s" % (ds_file, sh_file))
    else:
        LOGGER.info("begin compare execute :" + "python /home/cl/compare_file_py2.py %s %s" % (ds_file, sh_file))
        os.system("python /home/cl/compare_file_py2.py %s %s" % (ds_file, sh_file))


def main(compare_files_li):
    # 定义日志对象
    global LOGGER, WORK_DT
    log_file = "/etl/dwexp/crm/log/batch_exec_compare.log"
    logging.basicConfig(level=logging.INFO, filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')
    LOGGER = logging.getLogger("BatCompare")

    # 获取工作日期
    try:
        WORK_DT = sys.argv[1]
    except IndexError:
        print("Parameter error, Usage: python batch_exec_compare.py <WORK_DT>")
        sys.exit(1)

    # 创建进程池，指定最大并发进程数量为10
    pool = Pool(processes=3)
    # 使用进程池并行执行比对任务，文件未生成需要再次重调任务
    pool.map(run_compare, compare_files_li)

    # 自动检测文件，文件生成后开启子进程，无需重调
    # while compare_files_li:
    #     for files_tuple in compare_files_li:
    #         ds_file, sh_file = replace_file_name(files_tuple)
    #         if os.path.isfile(ds_file) and os.path.isfile(sh_file):
    #             pool.apply_async(run_compare, (files_tuple,))  # 添加任务到进程池
    #             compare_files_li.remove(files_tuple)

    pool.close()
    pool.join()
    LOGGER.info("All tasks are completed. Exiting...")


if __name__ == "__main__":
    compare_files_li = [
        ("/ds/CRM_30084_yyyymmdd_00001.txt", "/sh/CRM_30084_yyyymmdd_00001.txt"),
        ("/ds/CRM_30083_yyyymmdd_00001.txt", "/sh/CRM_30083_yyyymmdd_00001.txt"),
        ("/ds/CRM_30082_yyyymmdd_00001.txt", "/sh/CRM_30082_yyyymmdd_00001.txt"),
        ("/ds/CRM_30183_yyyymmdd_00001.txt", "/sh/CRM_30083_yyyymmdd_00001.txt"),
        ("/ds/CRM_30182_yyyymmdd_00001.txt", "/sh/CRM_30182_yyyymmdd_00001.txt"),
        ("/ds/CRM_30283_yyyymmdd_00001.txt", "/sh/CRM_30283_yyyymmdd_00001.txt"),
        ("/ds/CRM_30382_yyyymmdd_00001.txt", "/sh/CRM_30382_yyyymmdd_00001.txt"),
        ("/ds/CRM_30483_yyyymmdd_00001.txt", "/sh/CRM_30483_yyyymmdd_00001.txt"),
        ("/ds/CRM_30582_yyyymmdd_00001.txt", "/sh/CRM_30582_yyyymmdd_00001.txt"),
        ("/ds/CRM_30683_yyyymmdd_00001.txt", "/sh/CRM_30683_yyyymmdd_00001.txt"),
        ("/ds/CRM_30782_yyyymmdd_00001.txt", "/sh/CRM_30782_yyyymmdd_00001.txt"),
        ("/ds/CRM_30883_yyyymmdd_00001.txt", "/sh/CRM_30883_yyyymmdd_00001.txt"),
        ("/ds/CRM_30982_yyyymmdd_00001.txt", "/sh/CRM_30982_yyyymmdd_00001.txt"),
        ("/ds/CRM_31083_yyyymmdd_00001.txt", "/sh/CRM_31083_yyyymmdd_00001.txt"),
        ("/ds/CRM_31182_yyyymmdd_00001.txt", "/sh/CRM_31182_yyyymmdd_00001.txt"),
        ("/ds/CRM_31283_yyyymmdd_00001.txt", "/sh/CRM_31283_yyyymmdd_00001.txt"),
        ("/ds/CRM_31382_yyyymmdd_00001.txt", "/sh/CRM_31382_yyyymmdd_00001.txt")
    ]
    main(compare_files_li)



