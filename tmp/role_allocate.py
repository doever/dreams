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


# -.- coding: utf-8 -.-

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                                    config_roles.py                                        #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                              #
#      this script config roles table, and create role.sql files.                           #
#                                                                                           #
# Author     : chenlong                                                                     #
# Version    : v1.0                                                                         #
# CreDate    : 2024/04/15                                                                   #
# License    : Copyright (c) 2024 by cl                                                     #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import os
import sys
import csv
import codecs
import logging
import argparse

from common import get_db_conn, execute_command


def generator_role_allocate_sql(role_csv_file, role_map):
    """
    genertor sql by role config csv file.

    args:
        role_csv_file -> str : role csv file abosolute path
        role_map -> dict : a dict of role name and role code, juse like {"管理员": "R0001", ...}

    return:
        -> list : a list of all role config sql segments
    """

    role_sql_list = []  # 存储角色配置的insert语句

    with codecs.open(role_csv_file, "r", encoding="gbk", errors='ignore') as f_csv:
        reader = csv.reader(f_csv)
        first_row = next(reader)
        # 有效的角色名称跟角色代码的二维数组
        valid_role_list = [(role_name, role_map[role_name]) for role_name in first_row if role_name in role_map.keys()]
        value_of_role_list = (row for row in reader)

    for role_name, role_code in valid_role_list:
        index = first_row.index(role_name)  # 角色名称在原文件中的位置（列号）
        for row in value_of_role_list:
            if row[index]:  # 角色是否配置了权限
                role_sql_list.append(
                    "insert into AC_OPERATORROLE_C_APP (id,role,first_modu_id,first_modu_nm,sec_modu_id,sec_modu_nm,is_visit) values (sys_guid(), '%s', '%s', '%s', '%s', '%s', '1');" % (
                    role_code, row[0], row[1], row[2], row[3]))

    return role_sql_list


def generator_menu_allocate_sql(menu_csv_file):
    """
    generate sql by role config csv file.

    args:
        menu_csv_file -> str : menu csv file abosolute path

    return:
        -> list : a list of all role config sql segments
    """
    menu_sql_list = []
    with codecs.open(menu_csv_file, "r", encoding="gbk", errors='ignore') as f_csv:
        reader = csv.reader(f_csv)
        next(reader)
        for row in reader:
            print(row)
            menu_sql_list.append(
                "insert into AC_MENU_TREE_APP(MENUID, MENUNAME, PARENTMENUID, IS_DEL) values('%s', '%s', '%s', '%s');" % (
                row[1], row[2], row[3], row[4]))

    return menu_sql_list


def main():
    global LOGGER, DB
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
    LOGGER = logging.getLogger("role")
    LOGGER.info("Begin.")
    # try:
    DB = get_db_conn("/cimcim/conf/db.conf")

    parser = argparse.ArgumentParser(description="need one or two csv files")
    parser.add_argument("role_csv_file", type=str, help="权限角色表csv文件")
    parser.add_argument("--menu_csv_file", "-m", type=str, default=None, help="菜单表csv文件")
    args = parser.parse_args()

    role_map = dict(DB.select("select rolename || ',' || roleid from ac_role"))

    config_sql = "truncate table ac_operatorrole_c_app;\n"
    config_sql += "\n".join(generator_role_allocate_sql(args.role_csv_file, role_map))
    config_sql += "update ac_operatorrole_c_app d set func_rank=(select rn from (select t.*,t.rowid rid,row_number() over(partition by role,first_modu_id order by sec_modu_id) rn from ac_operatorrole_c_app t) s where  s.rid=d.rowid);\n"
    LOGGER.info("Role csv file load success.")
    LOGGER.info(config_sql)

    if args.menu_csv_file:
        config_sql += "truncate table AC_MENU_TREE_APP;\n"
        config_sql += "\n".join(generator_menu_allocate_sql(args.menu_csv_file))
        LOGGER.info("Menu csv file load success.")
    config_sql += "commit;\n"

    with codecs.open("role.sql", 'w', encoding='utf-8', errors='ignore') as sql_file:
        sql_file.write(config_sql)
    LOGGER.info("Created role.sql file success.")

    # DB.execute_file("role.sql")
    LOGGER.info("Execute role.sql file success.")
    LOGGER.info("End")

    # except Exception as err:
    #     LOGGER.error(err)


if __name__ == '__main__':
    main()