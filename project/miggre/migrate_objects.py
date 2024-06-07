# -.- coding: utf-8 -.-

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                                    migrate_objects.py                                     #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                              #
#      this script used to get object ddl sql statement.                                    #
#                                                                                           #
# Author     : chenlong                                                                     #
# Version    : v1.0                                                                         #
# CreDate    : 2024/04/26                                                                   #
# License    : Copyright (c) 2024 by cl                                                     #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import os
import re
import sys
import logging

from multiprocessing import Pool, Queue
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.db import OraDBSimpleFactory, execute_command


# get_triggery_sql = "SELECT DBMS_METADATA.GET_DDL('TRIGGER', trigger_name) AS trigger_ddl FROM user_triggers"
# get_function_sql = "SELECT DBMS_METADATA.GET_DDL('FUNCTION', object_name) AS function_ddl FROM user_procedures WHERE object_type='FUNCTION'"
# get_produce_sql = "SELECT DBMS_METADATA.GET_DDL('PROCEDURE', object_name) AS procedure_ddl FROM user_procedures WHERE object_type='PROCEDURE' and rownum <=2"
# get_pk_sql = "SELECT 'ALTER TABLE ' || table_name || ' ADD CONSTRAINT ' || constraint_name || ' PRIMARY KEY (' || column_list || ');' FROM user_constraints WHERE constraint_type='P'"
# get_wk_sql = "SELECT 'ALTER TABLE ' || table_name || ' ADD CONSTRAINT ' || constraint_name || ' FOREIGN KEY (' || column_list || ') REFERENCES ' || r_table_name || ' (' || r_column_list || ');' FROM user_constraints WHERE constraint_type = 'R'"


def migrate(object_name):
    try:
        sqls = old_db.select("select text from user_source where name='%s' order by line" % object_name)
        rebulid_statement = "create or replace " + "\n".join([i[0] for i in sqls])
        rebulid_statement = rebulid_statement.strip() + "\n/\n"
        new_db.create_procedure(rebulid_statement)
        logging.info(rebulid_statement)
    except ValueError as err:
        logging.error(err)
        # logging.error("execute %s occur a mistake." % rebulid_statement)


def migrate_by_file(file_name):
    if not os.path.isfile(file_name):
        logging.error("no such file %s." % file_name)
    try:
        new_db.execute_sql_file(file_name)
    except Exception as err:
        logging.error("execute %s file error," % file_name + str(err))

os.environ["NLS_LANG"] = "AMERICAN_AMERICA.AL32UTF8"

factory = OraDBSimpleFactory()
old_db = factory.create_db_object('/cimcim/cl/tools/common/db_sit.conf')
new_db = factory.create_db_object('/cimcim/cl/tools/common/db_sit_new.conf')
logging.basicConfig(level=logging.INFO, filename="migrate_object.log", format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')

logging.info("rebuild objects.")

base_path = os.path.join(os.getcwd(), "ddls")
# 同步序列
migrate_by_file(os.path.join(base_path, "sequences.sql"))

# 同步函数
logging.info("rebuild function.")
migrate_by_file(os.path.join(base_path, "functions.sql"))

# 同步类型
logging.info("rebuild type.")
migrate_by_file(os.path.join(base_path, "types.sql"))
new_db.create("CREATE OR REPLACE TYPE T_RET_TABLE is table of varchar2(50)")
new_db.create("CREATE OR REPLACE TYPE TYPE_TABLE_VARCHAR2 IS TABLE OF VARCHAR(30000)")

# 同步视图
logging.info("rebuild view.")
migrate_by_file(os.path.join(base_path, "view.sql"))
# migrate_by_file(os.path.join(base_path, "view.sql"))

# 同步触发器
migrate_by_file(os.path.join(base_path, "trigger.sql"))

# 同步存储包
migrate_by_file(os.path.join(base_path, "procedure_packs.sql"))

# 同步前置存储过程(SP_ETL_CREATE_LOG, )
migrate("SP_ETL_CREATE_LOG")

# 同步存储过程
# procedures = old_db.select("select distinct name from user_source where type='PROCEDURE'")
# procedures = list(map(lambda x:x[0], procedures))

# functions = old_db.select("select distinct name from user_source where type='FUNCTION'")
# functions = list(map(lambda x:x[0], functions))

# with open("functions.sql", "w") as p:
#     for object_name in functions:
#         try:
#             sqls = old_db.select("select text from user_source where name='%s' order by line" % object_name)
#             rebulid_statement = "create or replace " + "\n".join([i[0] for i in sqls])
#             rebulid_statement = rebulid_statement.strip() + "\n/\n"
#             p.write(rebulid_statement)
#         except ValueError as err:
#             logging.error(err)
#             pass

# pool = Pool(processes=4)
# pool.map_async(migrate, procedures)
# pool.close()
# pool.join()
# logging.info("done.")