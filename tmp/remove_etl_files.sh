#上月底日期=当前日期的上一个月末日期
#1.清理/etl/dwexp/crm下面的日期目录
#  清理（当前系统日期-17）到（当前系统日期-10）日期目录里面的数据文件，但要保留最近3个月末日期的文件
#2.查看/etl1/dwexp/crm这个目录下是否有 上月底日期 目录，且目录里面有数据文件
#  如果没有目录，或者目录里面是空的，则将/etl/dwexp/crm的上月底日期目录下的数据文件同步到/etl1/dwexp/crm上月底日期
#  否则什么也不做
#3.清理/etl1/dwexp/crm下面的日期目录，保留12个月的月末的数据即可



#!/bin/bash

# 获取当前日期
current_date=$(date +%Y%m%d)
# 计算上月底日期
last_month_end_date=$(date -d "$(date +%Y-%m-01) -1 day" +%Y%m%d)
# 定义保留日期目录的数组
declare -a keep_data_directory
log_file="/etl/dwexp/log/$current_date/remove_etl_files.log"


# 计算最近的三个月底的日期
for ((i = 0; i < 3; i++)); do
    last_day_of_month=$(date -d "$(date +%Y-%m-01) -$i month +1 month -1 day" +%Y%m%d)
    keep_data_directory+=("$last_day_of_month")
done

# 计算最近十天的日期
for ((i = 0; i < 10; i++)); do
    ten_days_ago=$(date -d "$current_date -$i days" +%Y%m%d)
    keep_data_directory+=("$ten_days_ago")
done

# 清理/etl/dwexp/crm下日期目录,保留最近的十天加最近三个月底的日期数据
for dir in $(ls -d /etl1/dwexp/crm/*/); do
    dir_name=$(basename "$dir")
    if [[ "$dir_name" =~ [0-9]{8} ]]; then
        if ! [[ "${keep_data_directory[@]}" =~ "$dir_name" ]]; then
            rm -f "$dir"/*
            echo "remove $dir/*" >> $log_file
        fi
    fi
done


# 同步数据/etl/dwexp/crm/上月底 到 /etl1/dwexp/crm/上月底
if [ ! -d "/etl1/dwexp/crm/$last_month_end_date" ] || [ -z "$(ls -A /etl1/dwexp/crm/$last_month_end_date)" ]; then
    rsync -av /etl/dwexp/crm/$last_month_end_date/ /etl1/dwexp/crm/$last_month_end_date/
    echo "rsync etl/dwexp/crm/$last_month_end_date /etl1/dwexp/crm/$last_month_end_date" >> $log_file
fi


# 清理/etl1/dwexp/crm下日期目录，保留12个月的月末数据
for dir in $(ls -d /etl1/dwexp/crm/*/); do
    dir_name=$(basename $dir)
    if [[ $dir_name =~ ^[0-9]{6} ]]; then
        year_month=${dir_name:0:6}
        if [ $year_month -lt $(date -d "12 months ago" +%Y%m) ]; then
            rm -f $dir
            echo "remove $dir" >> $log_file
        fi
    fi
done
