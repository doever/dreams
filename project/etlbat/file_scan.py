# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 file_scan.py                                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script compares two files.                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/4/26                                                                      #
# License    : Copyright (c) 2024 by cl, All rights reserved                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


import os
import re
import sys
import json
import time
import base64
import logging
import subprocess
import requests
import traceback
from datetime import datetime, timedelta

# schedule server api config info
PROXY = "http"  # 协议
SCHEDULE_HOST_IP = "192.168.1.80"                           # 调度服务器IP
SCHEDULE_HOST_PORT = "8088"                                 # 调度服务器端口
QUERY_JOB_URL = "/test/me/job/queryJob"                     # 查询job执行状态的URL
EXECUTE_JOB_URL = "/test/me/job//executeJob"                # 执行job的URL
GET_JOB_URL = "/test/me//job/getJob"                        # 执行job信息的URL
REQUEST_HEAD = {                                            # 请求头
    "User-Agent": "python-requests/2.23.0",
    "Accept-Encoding": "gzip, deflate, br",
    "content-type": "application/json",
    "charset": "utf-8",
    "Connection": "Keep-Alive",
    "Accept": "*/*"
}

# program config info
LOG_BASE_PATH = "/home/etl/log"                             # 日志目录
ORADB_CONFIG_FILE = "/etc/conf/db.conf"                     # Oracle配置文件
SLEEP_TIME = 300                                            # 轮询的休眠时间
MAX_DATE_DIFF_DAYS = 3                                      # 控制不同流之间日期的最大差值
FLOW_DATE_DI = {                                            # 任务流对应各自批量日期字段
    "TEST_AM_FLOW": "AM_FLOW_TIME",
    "TEST_DS_FLOW": "DS_FLOW_TIME",
    "TEST_GG_FLOW": "GG_FLOW_TIME"
    # "其他流3"     : "",
    # add more flow at here
}


class OraDB:
    def __init__(self, user, password, sid):
        self.user = user
        self.password = password
        self.sid = sid
        self.conn_str = self.user + "/" + self.password + "@" + self.sid

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
        output = execute_commands(cmd)

        if re.search("ORA-", output, re.IGNORECASE) or re.search("SP2-", output, re.IGNORECASE):
            raise ValueError("Select statement error \n%splease check sql syntax.\n%s" % (output, sql))
        results = [i.strip().split(",") for i in output.strip().split("\n") if output.strip()]
        return results

    def update(self, sql):
        cmd = "sqlplus -S %s <<EOF\n%s;\ncommit;\nquit\nEOF" % (self.conn_str, sql)
        output = execute_commands(cmd)
        if re.search("ORA-", output, re.IGNORECASE) or re.search("SP2-", output, re.IGNORECASE):
            raise ValueError("Sql statement error \n%splease check sql syntax.\n%s" % (output, sql))
        return output

    insert = update
    delete = update


def get_db_conn(conf):
    with open(conf, "r") as cf:
        conf_str = cf.read()
        try:
            db_user = base64.b64decode(re.findall('dbuser=(.+?)\n', conf_str)[0]).strip()
            db_pass = base64.b64decode(re.findall('dbpass=(.+?)\n', conf_str)[0]).strip()
            db_sid = base64.b64decode(re.findall('dbhost=(.+?)\n', conf_str)[0]).strip()
        except IndexError as err:
            raise ValueError("No such column name dbuser or dbpass or dbhost!")
        else:
            db = OraDB(user=db_user, password=db_pass, sid=db_sid)
            return db


def execute_commands(commands):
    try:
        process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = process.communicate()
    except Exception as err:
        LOGGER.error(err)
        exit(-3)
    else:
        if err:
            LOGGER.error("Execute failed, %s\ncommand:\n %s" % (err, str(commands)))
            # exit(-6)
        return output


def client():
    # 接收用户参数
    if len(sys.argv) <= 2:
        print("Parameter error, Usage: python satrt_file_scan.py flow_name work_dt")
        exit(-1)
    flow_name = sys.argv[1]
    work_dt = sys.argv[2]

    # 参数验证，防止注入问题
    if not FLOW_DATE_DI.get(flow_name) and not re.match("^20\d{6}$", work_dt):
        print("Parameter value error, undefined flow_name :%s or false date format: %s" % (flow_name, work_dt))
        exit(-2)

    # 定义日志
    global LOGGER, DB
    log_file = os.path.join(LOG_BASE_PATH, work_dt, "START_" + flow_name + "_" + work_dt +".log")
    logging.basicConfig(level=logging.INFO, filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    LOGGER = logging.getLogger("FileScan")

    try:
        LOGGER.info("Begin scanning files(work_dt:%s)..." % work_dt)
        DB = get_db_conn(ORADB_CONFIG_FILE)

        # 循环读流日期差值，直到当前流的日期与最小流日期差值小于3天
        while True:
            cols = ",".join(FLOW_DATE_DI.values())
            date_diff = int(DB.select("select %s-least(%s) from f_cm_bat_times" % (FLOW_DATE_DI.get(flow_name), cols))[0][0])
            if date_diff >= MAX_DATE_DIFF_DAYS - 1 :
                LOGGER.info("The date of current flow is greater than the minimun date of all flows for more than 3 days, date_diff is: %s. " % str(date_diff + 1))
                time.sleep(SLEEP_TIME)
            else:
                flow_current_date = DB.select("select to_char(%s, 'YYYYMMDD') from f_cm_bat_times" % FLOW_DATE_DI.get(flow_name))[0][0]
                if work_dt == (datetime.strptime(flow_current_date, "%Y%m%d") + timedelta(days=2)).strftime("%Y%m%d"):  # 由于在start作业翻牌，导致work_dt与当前流日期的差值是2，如果在end作业里面翻牌，差值就是1
                    # todo:更新日期加一还是更新为work_dt-1？
                    next_day = (datetime.strptime(work_dt, "%Y%m%d") + timedelta(days=-1)).strftime("%Y%m%d")
                    DB.update("update f_cm_bat_times set %s=to_date('%s', 'YYYYMMDD') where 1=1" % (FLOW_DATE_DI.get(flow_name), next_day))
                    LOGGER.info("Workflow %s change flow date %s -> %s." % (flow_name, flow_current_date, next_day))
                break

        # 循环执行触发文件加载，直到所有作业翻牌
        etl_jobs = ["see u someday"]
        while etl_jobs:
            # 实时读取ETL JOB配置
            etl_jobs = DB.select("select sys_id||','|| etljob||','|| datapath||','|| c_label||','|| suffixformat||','|| to_char(C_DATE,'YYYYMMDD')||','|| to_char(C_DATE,'YYYY-MM-DD') from LOAD_TABLE_INFO WHERE c_valid ='1' and flow_name='%s' and c_date=to_date('%s','YYYYMMDD')-1" % (flow_name, work_dt))
            LOGGER.info("Ready to load etl jobs: (work_dt:%s):\n" % work_dt + "\n".join([i[1] for i in etl_jobs]))
            for sys_id, etl_job, data_path, c_label, suffixformat, c_date1, c_date2 in etl_jobs:
                # 判断flg文件跟数据文件是否都存在
                if os.path.isfile(
                        os.path.join(data_path, work_dt, c_label + "_" + work_dt + suffixformat)) and os.path.isfile(
                        os.path.join(data_path, work_dt, c_label + "_" + work_dt + ".flg")):
                    js_data = json.dumps({
                        "projectName": sys_id,
                        "jobName": etl_job,
                        "flipTime": re.sub(r"(\d{4})(\d{2})(\d{2})", r"\1-\2-\3", work_dt)
                    })
                    response = requests.post(
                        "%s://%s:%s%s" % (PROXY, SCHEDULE_HOST_IP, SCHEDULE_HOST_PORT, QUERY_JOB_URL), data=js_data,
                        headers=REQUEST_HEAD)
                    code = response.json().get("code").upper()
                    response_data = response.json().get("data") if response.json().get("data") else {}
                    job_status = response_data.get("status").upper() if response_data.get("status") else ""

                    if code == "FAILURE":  # 任务未运行
                        res = requests.post(
                            "%s://%s:%s%s" % (PROXY, SCHEDULE_HOST_IP, SCHEDULE_HOST_PORT, EXECUTE_JOB_URL),
                            data=js_data, headers=REQUEST_HEAD)
                        LOGGER.info("Start etl load job %s." % etl_job)
                    elif code == "OK" and job_status == "SUCCESS":  # 任务运行成功
                        DB.update("update load_table_info set c_date=to_date('%s', 'YYYYMMDD') where etljob='%s'" % (
                        work_dt, etl_job))
                        LOGGER.info("%s load success, switch next day." % etl_job)
                    else:
                        pass
                else:
                    LOGGER.info(
                        "%s file not exist" % os.path.join(data_path, work_dt, c_label + "_" + work_dt + suffixformat))
                    continue

            if etl_jobs:
                LOGGER.info("Start next scanning.")
                time.sleep(SLEEP_TIME)
            else:
                LOGGER.info("Done.")

    except Exception as err:
        LOGGER.error("The scan file program occur a mistake, %s" % err)
        traceback.print_exc()
        raise ValueError(err)  # 让调度接收异常状态，而不会显示为成功


if __name__ == "__main__":
    client()