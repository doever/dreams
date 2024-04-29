# -.- coding: utf-8 -.-
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 role_allocate.py                                            #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script allocate role by csv config file.                                           #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/4/25                                                                      #
# License    : Copyright (c) 2024 by cl, All rights reserved                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import os
import sys
import csv
import codecs
import logging
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from common.db import get_db_conn, execute_command, test


def generator_role_allocate_sql(role_csv_file, role_map):
    """
    Generate sql by role config csv file.

    Args:
        role_csv_file -> str : role csv file absolute path
        role_map -> dict : a dict of role name and role code, just like {"管理员": "R0001", ...}

    Return:
        -> list : a list of all role config sql segments
    """

    role_sql_list = []  # 存储角色配置的insert语句

    with open(role_csv_file, "r") as f_csv:
        reader = csv.reader(f_csv)
        first_row = next(reader)
        # 有效的角色名称跟角色代码的二维数组
        valid_role_list = [(role_name, role_map[role_name]) for role_name in first_row if role_name in role_map.keys()]
        value_of_role_list = (row for row in reader)

    for role_name, role_code in valid_role_list:
        index = first_row.index(role_name)              # 角色名称在原文件中的位置（列号）
        for row in value_of_role_list:
            if row[index]:                              # 角色是否配置了权限
                role_sql_list.append("insert into operatorrole values (sys_guid(), '%s', '%s', '%s', '%s', '%s', '1');" % (role_code, row[0], row[1], row[2], row[3]))

    return role_sql_list


def generator_menu_allocate_sql(menu_csv_file):
    """
    Generate sql by role config csv file.

    Args:
        menu_csv_file -> str : menu csv file absolute path

    Return:
        -> list : a list of all role config sql segments
    """
    menu_sql_list = []
    with codecs.open(menu_csv_file, "r", encoding="gbk", errors='ignore') as f_csv:
        reader = csv.reader(f_csv)
        next(reader)
        for row in reader:
            print(row)
            menu_sql_list.append("insert into menu values('%s', '%s', '%s', '%s');" % (row[1], row[2], row[3], row[4]))

    return menu_sql_list


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Begin config role.")
    try:
        sit_db = get_db_conn("develop")
        uat_db = get_db_conn("test")

        parser = argparse.ArgumentParser(description="need one or two csv files")
        parser.add_argument("role_csv_file", type=str,
                            help="Param error, Usage: python config_roles.py role_csv_file -m <menu_csv_file>")
        parser.add_argument("--menu_csv_file", "-m", type=str, default=None, help="菜单表csv文件")
        args = parser.parse_args()

        role_map_sit = dict(sit_db.select("select rolename || ',' || roleid from ac_role"))
        role_map_uat = dict(uat_db.select("select rolename || ',' || roleid from ac_role"))
        # 对比sit跟uat环境的ac_role表
        if role_map_sit != role_map_uat:
            raise ValueError("The value of role_name and role_id in ac_role table are different between SIT environment and UAT environment.")

        logging.info("Load role config file: %s." % args.role_csv_file)
        sql_list = ["truncate table ac_operatorrole_c_app;"]
        sql_list += generator_role_allocate_sql(args.role_csv_file, role_map_sit)
        sql_list.append(
            "update ac_operatorrole_c_app d set func_rank=(select rn from (select t.*,t.rowid rid,row_number() over(partition by role,first_modu_id order by sec_modu_id) rn from ac_operatorrole_c_app t) s where  s.rid=d.rowid);")

        if args.menu_csv_file:
            logging.info("Load menu config file: %s." % args.menu_csv_file)
            sql_list.append("truncate table AC_MENU_TREE_APP;")
            sql_list += generator_menu_allocate_sql(args.menu_csv_file)
        logging.info("All csv file load success.")

        sql_list.append("commit;")
        sql_str = "\n".join(sql_list)

        # GBK 文件
        logging.info("Creating allocate_role.sql file.")
        with open("allocate_role.sql", "w") as sql_file:
            sql_file.write(sql_str)

        sit_db.execute_sql_file("allocate_role.sql")
        logging.info("Execute allocate_role.sql success in the SIT environment.")
        uat_db.execute_sql_file("role.sql")
        logging.info("Execute allocate_role.sql success in the UAT environment.")
        logging.info("Done.")

    except Exception as err:
        logging.error(err)


if __name__ == '__main__':
    main()
