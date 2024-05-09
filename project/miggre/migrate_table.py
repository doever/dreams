# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 migrate_table.py.py                                         #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script                   .                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/5/7                                                                       #
# License    : Copyright (c) 2024 by cl, All rights reserved                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #

import os
import re
import csv
import base64
import subprocess

from multiprocessing import Pool

class OraDB:
    def __init__(self, user, password, sid):
        self.user = user
        self.password = password
        self.sid = sid
        self.conn_str = self.user + "/" + self.password + "@" + self.sid

    @staticmethod
    def execute_success(output):
        """Verify that the output is correct"""
        ora_pattern = re.compile(r"ORA-", re.IGNORECASE)
        sp2_pattern = re.compile(r"SP2-", re.IGNORECASE)
        if not ora_pattern.search(output) and not sp2_pattern.search(output):
            return True
        return False

    def execute_sql_file(self, sql_file):
        cmd = "sqlplus -S %s <<EOF\n@%s;\nquit\nEOF" % (self.conn_str, sql_file)
        output = execute_command(cmd)
        if self.execute_success(output):
            return output
        raise ValueError("Execute sql file error \n%s please check sql file.\n%s" % (output, sql_file))

    def select(self, sql):
        sqlplus_format_di = {
            "serveroutput": "on",
            "feedback": "off",
            "heading": "off",
            "echo": "off",
            "verify": "off",
            "trimspool": "on",
            "linesize": "10000",
            "pagesize": "0",
            "termout": "on"
        }
        sqlplus_format_str = " ".join(["%s %s" % (k, v) for k, v in sqlplus_format_di.items()])
        cmd = "sqlplus -S %s <<EOF\nset %s;\n%s;\nquit\nEOF" % (self.conn_str, sqlplus_format_str, sql)
        output = execute_command(cmd)
        if self.execute_success(output):
            results = [i.strip().split(",") for i in output.strip().split("\n") if output.strip()]
            return results
        raise ValueError("Select statement error \n%s please check sql syntax.\n%s" % (output, sql))

    def update(self, sql):
        cmd = "sqlplus -S %s <<EOF\n%s;\ncommit;\nquit\nEOF" % (self.conn_str, sql)
        output = execute_command(cmd)
        if self.execute_success(output):
            return output
        raise ValueError("Sql statement error \n%splease check sql syntax.\n%s" % (output, sql))

    insert = update
    delete = update


class OraDBSimpleFactory:
    __slots__ = ('config_file',)
    _ORA_DB_ENVIRONMENT = ('sit', 'uat', 'pp')

    def __init__(self):
        self.config_file = None

    @staticmethod
    def parse_config(config_file):
        config = {}
        with open(config_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    match = re.match(r'^([^=]+)=(.*)$', line)
                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip()
                        config[key] = base64.b64decode(value)
        return config

    def create_db_object(self, ora_db_environment):
        if ora_db_environment not in self._ORA_DB_ENVIRONMENT:
            raise TypeError("Init error, Oracle DB environment is not supported, Excepted one of: (%s)" % ", ".join(self._ORA_DB_ENVIRONMENT))
        self.config_file = "/etc/cl/tools/common/db_%s.conf" % ora_db_environment

        if not os.path.exists(self.config_file):
            raise FileNotFoundError("No such files : %s" % self.config_file)

        config = self.parse_config(self.config_file)
        if not config.get("db_user") or not config.get("db_pass") or not config.get("db_host"):
            raise ValueError("No such column name db_user or db_pass or db_host in %s!" % self.config_file)

        db = OraDB(user=config.get("db_user"), password=config.get("db_pass"), sid=config.get("db_host"))
        return db


def execute_command(commands):
    try:
        process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = process.communicate()
    except Exception as err:
        raise ValueError(err)
    else:
        if err:
            raise ValueError("Execute failed, %s\ncommand:\n %s" % (err, str(commands)))
        return output


def migrate(table_info):
    table_name, is_partition = table_info
    db.insert("create table %s as select * from %s" % (table_name+'_bak', table_name))


def main():
    global db
    factory = OraDBSimpleFactory()
    db = factory.create_db_object('uat')
    with open("all_tables.csv", "r") as f_csv:
        reader = csv.reader(f_csv)
        next(reader)
        tables = [(row[1], row[2]) for row in reader]

    pool = Pool(processes=10)
    pool.map_async(migrate, tables)
    pool.close()
    pool.join()



