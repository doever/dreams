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
import random
import subprocess

# 我需要批量调用一个python脚本去比对文件，这样写是否可行，有没有bug

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
    ("/ds/CRM_31382_yyyymmdd_00001.txt", "/sh/CRM_31382_yyyymmdd_00001.txt"),
]


# print("begin batch execute compare")
# while compare_files_li:
#     try:
#         work_dt = sys.argv[1]
#     except IndexError as err:
#         print("Parameter error, Usage: python batch_exec_compare.py <work_dt>")
#     else:
#         for no, files_tuple in enumerate(compare_files_li, start=0):
#             ds_file = re.sub(r"yyyymmdd", work_dt, files_tuple[0])
#             sh_file = re.sub(r"yyyymmdd", work_dt, files_tuple[1])
#
#             if not os.path.isfile(ds_file) or not os.path.isfile(sh_file):
#                 continue
#             if ds_file.endswith("gz"):
#                 process = subprocess.Popen(["gunzip %s" % ds_file, "gunzip %s" % sh_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
#                 output, err = process.communicate()
#                 ds_file = ds_file[:-3]
#                 sh_file = sh_file[:-3]
#
#             process = subprocess.Popen(["python /cimcim/script/compare_file.py %s %s" % (ds_file, sh_file)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
#             compare_files_li.pop(no)


work_dt = "20240101"
while compare_files_li:
    print(compare_files_li)
    count = 0
    # for no, files_tuple in reversed(list(enumerate(compare_files_li, start=0))):
    for no, files_tuple in enumerate(compare_files_li, start=0):
        ds_file = re.sub(r"yyyymmdd", work_dt, files_tuple[0])
        sh_file = re.sub(r"yyyymmdd", work_dt, files_tuple[1])
        random_number = random.choice([1, 2, 3])
        if random_number == 1:
            compare_files_li.pop(no)
            count += 1
    print(f"删除了{str(count)}个元素")