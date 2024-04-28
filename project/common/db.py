# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 common.py                                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script compares two files.                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/4/25                                                                      #
# License    : Copyright (c) 2024 by cl, All rights reserved                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import os
import re
import base64
import subprocess


class OraDB:
    def __init__(self, user, password, sid):
        self.user = user
        self.password = password
        self.sid = sid
        self.conn_str = self.user + "/" + self.password + "@" + self.sid

    def execute_sql_file(self, sql_file):
        cmd = "sqlplus -S %s <<EOF\n@%s;\nquit\nEOF" % (self.conn_str, sql_file)
        # cmd = "sqlplus -S %s @%s" % (self.conn_str, sql_file)
        output = execute_command(cmd)
        if re.search("ORA-", output, re.IGNORECASE) or re.search("SP2-", output, re.IGNORECASE):
            raise ValueError("Select statement error \n%splease check sql syntax.\n%s" % (output, sql_file))

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
        if re.findall("ORA-", output) or re.findall("SP2-", output):
            raise ValueError("Select statement error \n%splease check sql syntax.\n%s" % (output, sql))
        results = [i.strip().split(",") for i in output.strip().split("\n") if output.strip()]
        return results

    def update(self, sql):
        cmd = "sqlplus -S %s <<EOF\n%s;\ncommit;\nquit\nEOF" % (self.conn_str, sql)
        output = execute_command(cmd)
        if re.findall("ORA-", output) or re.findall("SP2-", output):
            raise ValueError("Sql statement error \n%splease check sql syntax.\n%s" % (output, sql))
        return output

    insert = update
    delete = update


def get_db_conn(db_type):
    if db_type.lower() == "develop":
        conf_file = "/etc/conf/db.conf"
    elif db_type.lower() == "test":
        conf_file = "/etc/cl/tools/common/db_test.conf"
    elif db_type.lower() == "pp":
        conf_file = "/etc/cl/tools/common/db_pp.conf"
    else:
        raise ValueError("Unknown params : %s, use sit or uat or pp" % db_type)

    if not os.path.isfile(conf_file):
        raise FileNotFoundError("no such files : %s" % conf_file)

    # base64解析conf_file文件
    with open(conf_file, "r") as cf:
        conf_str = cf.read()
        try:
            db_user = base64.b64decode(re.findall('user=(.+?)\n', conf_str)[0]).strip()
            db_pass = base64.b64decode(re.findall('pass=(.+?)\n', conf_str)[0]).strip()
            db_sid = base64.b64decode(re.findall('host=(.+?)\n', conf_str)[0]).strip()
        except IndexError as err:
            raise ValueError("No such column name dbuser or dbpass or dbhost!")
        else:
            db = OraDB(user=db_user, password=db_pass, sid=db_sid)
            return db


def execute_command(commands):
    try:
        process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = process.communicate()
    except Exception as err:
        raise ValueError(err)
        exit(-3)
    else:
        if err:
            raise ValueError("Execute failed, %s\ncommand:\n %s" % (err, str(commands)))
        return output
