# -.- coding:utf-8 -.-

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 compare_timesheet.py                                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script compares two files.                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2025/8/8                                                                      #
# License    : Copyright (c) 2024 by cl, All rights reserved                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #

import pandas as pd
from datetime import datetime


def read_xls_to_dict(filename):
    df = pd.read_excel(filename, sheet_name=0, skiprows=2)
    # 删除第一列（按位置）
    df = df.iloc[:, 1:]
    di = {}
    for i in range(0, len(df), 2):
        key = df.iloc[i, 0]
        value = df.iloc[i].to_dict()
        value.pop('姓名')
        di[key] = value
    return di


def read_xlsx_to_dict(filename):
    df = pd.read_excel(filename, sheet_name=0, skiprows=3)
    di = {}
    for row in df.itertuples():
        # print(f"{row.姓名}, {row.实际工作日}")
        if pd.notna(row.姓名):
            di[row.姓名] = row.实际工作日
    return di


def merge_dicts(dicts):
    merged = {}
    for d in dicts:
        for key, subdict in d.items():
            if key not in merged:
                merged[key] = subdict.copy()
            else:
                # 合并子字典，保留先出现的键
                for subkey, value in subdict.items():
                    if subkey not in merged[key]:
                        merged[key][subkey] = value
    return merged


if __name__ == '__main__':
    # 统计的年份周期
    year = 2025
    months = [9, 10, 11]

    di_1 = read_xls_to_dict(r"C:/Users/syrg_/Desktop/翕振智慧金融事业部考勤表9月.xls")
    di_2 = read_xls_to_dict(r"C:/Users/syrg_/Desktop/翕振智慧金融事业部考勤表10月.xls")
    di_3 = read_xls_to_dict(r"C:/Users/syrg_/Desktop/翕振智慧金融事业部考勤表11月.xls")
    di_4 = read_xls_to_dict(r"C:/Users/syrg_/Desktop/翕振智慧金融事业部考勤表12月.xls")
    xy_di_1 = read_xlsx_to_dict(r"C:/Users/syrg_/Desktop/工作量付款确认表-202509.xlsx")
    xy_di_2 = read_xlsx_to_dict(r"C:/Users/syrg_/Desktop/工作量付款确认表-202510.xlsx")
    xy_di_3 = read_xlsx_to_dict(r"C:/Users/syrg_/Desktop/工作量付款确认表-202511.xlsx")

    # ______________________________统计高伟达工时____________________________________________
    dicts = [di_1, di_2, di_3, di_4]
    result = merge_dicts(dicts)
    gwd_timesheet = {}
    for k, v in result.items():
        name = k.split('-')[0]
        month_di = {
            str(months[0]): 0,
            str(months[1]): 0,
            str(months[2]): 0
        }
        for k2, v2 in v.items():
            date_obj = datetime.strptime(f"{year}-{k2}", "%Y-%m-%d")
            mon = date_obj.month
            if str(mon) in month_di.keys() and pd.notna(v2):
                month_di[str(mon)] += v2/8

        gwd_timesheet[name] = month_di

    # print(gwd_timesheet)

    # ______________________________比对兴业工时____________________________________________
    for k, v in xy_di_1.items():
        if k not in gwd_timesheet.keys():
            continue

        if v == gwd_timesheet[k][str(months[0])]:
            print(f"{k} {str(months[0])}的工时相等")
        else:
            print(f"{k} {str(months[0])}的工时不相等！！，高伟达工时：{str(gwd_timesheet[k][str(months[0])])} 兴业工时：{str(v)}")
    print("-"*80)
    for k, v in xy_di_2.items():
        if k not in gwd_timesheet.keys():
            continue

        if v == gwd_timesheet[k][str(months[1])]:
            print(f"{k} {str(months[1])}的工时相等")
        else:
            print(f"{k} {str(months[1])}的工时不相等！！，高伟达工时：{str(gwd_timesheet[k][str(months[1])])} 兴业工时：{str(v)}")
    print("-" * 80)
    for k, v in xy_di_3.items():
        if k not in gwd_timesheet.keys():
            continue

        if v == gwd_timesheet[k][str(months[2])]:
            print(f"{k} {str(months[2])}的工时相等")
        else:
            print(f"{k} {str(months[2])}的工时不相等！！，高伟达工时：{str(gwd_timesheet[k][str(months[2])])} 兴业工时：{str(v)}")
