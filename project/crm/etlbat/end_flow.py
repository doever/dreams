# -.- coding: utf-8 -.-

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
#                                      end_flow.py                                          #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #
# Description:                                                                              #
#      this script post request to execute start_file_scan.py script                        #
#                                                                                           #
# Author     : chenlong                                                                     #
# Version    : v1.0                                                                         #
# CreDate    : 2024/04/18                                                                   #
# License    : Copyright (c) 2024 by cl                                                     #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #

import os
import re
import sys
import json
import time
import logging
import requests
from datetime import datetime, timedelta


sys.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.db import *

# 接收用户参数
if len(sys.argv) <= 2:
    print("Parameter error, Usage: python end_flow.py <work_dt>")
    exit(-1)

flow_job_name = sys.argv[1]
work_dt = sys.argv[2]

next_day = (datetime.strptime(work_dt, "%Y%m%d") + timedelta(days=1)).strftime("%Y-%m-%d")

# 定义日志记录器
log_file = os.path.join(LOG_BASE_PATH, work_dt, "END_" + flow_job_name[6:] + "_" + work_dt +".log")
logging.basicConfig(level=logging.INFO, filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger("End")

js_data = json.dumps({
                        "projectName": "CRM",   # todo:是否可以写死
                        "jobName": flow_job_name,
                        "flipTime": next_day
                    })

time.sleep(124)  # 测试

for count in range(3):
    try:
        LOGGER.info("begin execute %s end task(work_dt:%s)" % (flow_job_name, work_dt))
        res = requests.post("%s://%s:%s%s" % (PROXY, SCHEDULE_HOST_IP, SCHEDULE_HOST_PORT, EXECUTE_JOB_URL), data=js_data, headers=REQUEST_HEAD)
        LOGGER.info("repsponse code is : %s" % str(res.status_code))
        LOGGER.info(res.text.encode('utf-8'))
    except Exception as err:
        LOGGER.error("request schedule server occur a mistask, %s" %  err)
    else:
        if res.json().get("code").upper() == "OK":
            LOGGER.info("launch %s job success." % flow_job_name)
        else:
            LOGGER.error("launch %s job failed." % flow_job_name)
        break

    time.sleep(SLEEP_TIME)