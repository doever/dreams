# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 file_scan.py                                                #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script compares two files.                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/4/17                                                                      #
# License    : Copyright (c) 2024 by cl, All rights reserved                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #

# -.- coding: utf-8 -.-

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                                 satrt_file_scan.py                                        #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                              #
#      batch call compare_file script.                                                      #
#                                                                                           #
# Author     : chenlong                                                                     #
# Version    : v1.0                                                                         #
# CreDate    : 2024/04/15                                                                   #
# License    : Copyright (c) 2024 by cl                                                     #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #

## 是否有最大触发限制
## 生产环境ora解析是否有问题

import os
import re
import sys
import json
import time
import base64
import logging
import subprocess
import requests


class OraDB:
    _instance = None

    def __new__(cls, user, password, sid):
        if not cls._instance:
            cls._instance = super(DB, cls).__new__(cls, user, password, sid)
            return cls._instance

    def __init__(self, user, password, sid):
        self.user = user
        self.password = password
        self.sid = sid
        self.conn_str = self.user + "/" + self.password + "@" + self.sid

    def select(self, sql):
        cmd = "sqlplus -S %s <<EOF\nset heading off pagesize 0 feedback off echo off linesize 10000;\n%s;\nquit\nEOF" % (
        self.conn_str, sql)
        print(cmd)
        output = run_cmd(cmd)
        result_li = [i.split(",") for i in output.split("\n")]
        return result_li

    def update(self, sql):
        cmd = "sqlplus -S %s <<EOF\n%s;\ncommit;\nquit\nEOF" % (self.conn_str, sql)
        print(cmd)
        output = run_cmd(cmd)
        return output

    insert = update
    delete = update


class EtlJobAgent(object):
    def __init__(self):
        self._observers = []

    def add_observers(self, observer):
        self._observers.append(observer)
        print("订阅成功")

    def remove_observers(self, observer):
        self._observers.remove(observer)
        print("取消订阅")

    def notify_observers(self, sys_id, etl_job, work_dt):
        for observer in self._observers:
            observer.file_trigger(sys_id, etl_job, work_dt)

    # def add_etl_job(self, sys_id, etl_job, work_dt):
    #     self.notify_observers(sys_id, etl_job, work_dt)


class Observer(object):
    def __init__(self, protocol, host_ip, port):
        self.protocol = protocol
        self.host_ip = host_ip
        self.port = port
        self.headers = {
            "User-Agent": "python-requests/2.23.0",
            "Accept-Encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "charset": "utf-8",
            "Connection": "Keep-Alive",
            "Accept": "*/*"
        }
        self.query_job_url = "%s://%s:%s/xenon/meta/jobProcess/queryJobProcess"
        self.execute_job_url = "%s://%s:%s/xenon/meta/job/executeInterfaceJob"
        self.get_job_url = "%s://%s:%s/xenon/meta/job/getJob"

    def execute_job(self, js_data):
        response = requests.post(self.execute_job_url, data=js_data, headers=self.headers)
        if response.status_code != '200':
            LOGGER.error("fail to execute etl job %s" % str(js_data))
        # return query_job

    def file_trigger(self, sys_id, etl_job, work_dt):
        js_data = json.dumps({
            "projectName": sys_id,
            "jobName": etl_job,
            "flipTime": work_dt
        })
        try:
            response = requests.post(self.query_job_url, data=js_data, headers=self.headers)
        except Exception as err:
            LOGGER.error("query job process request error:%s" % err)
        else:
            if response.status_code != '200':
                LOGGER.warning("query job process request failed, response code is %s, mes:%s" % (
                response.status_code, response.text))
                job_status = "ERROR"
            else:
                res_di = response.json()
                code = res_di.get("code").upper()
                status = res_di.get("data").get("status").upper()

                if code == "FAILURE":  # 记录不存在，未运行job
                    self.execute_job(js_data)
                elif code == "OK" and status == "SUCCESS":  # 查询到记录，且任务状态是完成
                    DB.update("update load_table_info set c_date=c_date+1 where etljob='%s'" % etl_job)
                    LOGGER.info("%s load success, switch next day." % etl_job)

                elif code == "OK" and (status == "RUNNING" or status == "FAILED"):
                    LOGGER.warning("%s load failed.")
                else:
                    pass


def get_db_conn(conf):
    with open(conf, "r") as cf:
        conf_str = cf.read()
        try:
            db_user = base64.b64decode(re.findall('dbuser=(.+?)\n', conf_str)[0]).strip()
            db_pass = base64.b64decode(re.findall('dbpass=(.+?)\n', conf_str)[0]).strip()
            db_sid = base64.b64decode(re.findall('dbhost=(.+?)\n', conf_str)[0]).strip()
        except IndexError as err:
            raise ValueError("no such column name dbuser or dbpass or dbhost!")
        else:
            db = OraDB(user=db_user, password=db_pass, sid=db_sid)
            return db


def run_cmd(cmd_list):
    try:
        process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = process.communicate()
    except Exception as err:
        LOGGER.error(err)
        exit(-3)
    else:
        if err:
            LOGGER.error("execute failed, %s\ncommand:\n %s" % (err, str(cmd_list)))
            # exit(-6)
        return output


def client():
    flow_map = {
        "主流名称1": "FLOW_TIME1",
        "主流名称2": "FLOW_TIME2",
        "主流名称3": "FLOW_TIME3",
        "其他流1": "FLOW_TIME4",
        "其他流2": "FLOW_TIME5",
        "其他流3": "FLOW_TIME6",
    }
    # 创建日志目录
    # log_dir = "/etl/dwexp/log"
    # os.system("mkdir -p %s" % os.path.join(log_dir))

    # 接收用户参数
    if len(sys.argv) <= 2:
        print("Parameter error, Usage: python compare_file.py <file_a_path> <file_b_path>")
        exit(-1)
    flow_name = sys.argv[1]
    work_dt = sys.argv[2]

    # 验证参数，防止注入问题
    if not flow_map.get(flow_name) and not re.match("20\d{6}", work_dt):
        print("Parameter value error, undefined flow_namr %s or false date format" % (flow_name, work_dt))
        exit(-2)

    # 定义日志对象和数据库对象
    global DB, LOGGER
    DB = get_db_conn("/cimcim/conf/db.conf")
    log_file = os.path.join("/etl/dwexp/log", work_dt, flow_name + work_dt + ".run.log")
    logging.basicConfig(level=logging.INFO, filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')
    LOGGER = logging.getLogger("FileScan")
    LOGGER.info("begin...")

    etl_agent = EtlJobAgent()  # 任务发布者
    observer = Observer("", "", "")  # 订阅者
    etl_agent.add_observers(observer)  # 绑定订阅者

    while True:  # 循环读流日期差值，直到当前流的日期与最小流日期差值小于3天
        cols = ",".join(flow_map.values())
        res = DB.select("select %s-least(%s) from f_cm_bat_times" % (flow_map.get(flow_name), flow_map.get(flow_name)))
        date_diff = res[0][0]
        if date_diff >= 3:
            time.sleep(300)
        else:
            # 流翻牌, 修改流日期+1
            DB.update(
                "update f_cm_bat_times set %s=%s+1 where 1=1" % (flow_map.get(flow_name), flow_map.get(flow_name)))
        break

    etl_jobs = ["see u someday"]
    while etl_jobs:  # 循环执行触发文件作业，直到所有作业翻牌
        # 实时读取最新配置
        etl_jobs = DB.select(
            "select sys_id||','|| etljob||','|| datapath||','|| c_label||','|| suffixformat||','|| to_char(C_DATE,'YYYYMMDD')||','|| to_char(C_DATE,'YYYY-MM-DD') from LOAD_TABLE_INFO WHERE c_valid ='1' and flow_name='%s' and c_date=to_date('%s','YYYYMMDD')" % (
            flow_name, work_dt))
        print(etl_jobs)
        for sys_id, etl_job, data_path, c_label, suffixformat, c_date1, c_date2 in etl_jobs:
            # 判断flg文件跟数据文件是否都存在
            if os.path.isfile(os.path.join(data_path, work_dt, c_label + work_dt + suffixformat)) and os.path.isfile(
                    os.path.join(data_path, work_dt, c_label + work_dt + ".flg")):
                etl_agent.notify_observers(sys_id, etl_job, work_dt)
            else:
                continue
        time.sleep(300)


if __name__ == "__main__":
    client()

