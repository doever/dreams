# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 start_file_scan.py                                          #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script compares two files.                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/4/15                                                                      #
# License    : Copyright (c) 2024 by cl, All rights reserved                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import time
import asyncio

#
# ETL_JOB_LI = [
#     "etl_job_001",
#     "etl_job_002",
#     "etl_job_003",
#     "etl_job_004",
#     "etl_job_005",
#     "etl_job_006",
#     "etl_job_007",
#     "etl_job_008"
# ]


# 定义异步操作函数
async def async_operation(callback):
    print("Async operation started.")
    # 模拟异步操作
    await asyncio.sleep(2)
    result = "Async operation completed."
    # 调用回调函数，并传递结果
    callback(result)


# 定义回调函数
def handle_result(etl_job):
    print(f"更新作业{etl_job}的日期")


async def main():
    print('start...')
    file1_path = 'file_a.txt'
    file2_path = 'file_b.txt'
    await async_operation(handle_result)
    print('end...')

# 发起异步操作，并传递回调函数
asyncio.run(main())



# async def compare_large_files(file1_path, file2_path):
    # 异步读取文件内容
    # async with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
    #     content1 = await file1.read()
    #     content2 = await file2.read()
    # 执行文件比较操作
    # if content1 == content2:
    #     print("Files are identical")
    # else:
    #     print("Files are different")

# async def main():
#     print('start...')
#     file1_path = 'file_a.txt'
#     file2_path = 'file_b.txt'
#     await compare_large_files(file1_path, file2_path)
#     print('end...')
#
# # 在异步事件循环中运行主函数
# asyncio.run(main())

