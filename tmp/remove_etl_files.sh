#上月底日期=当前日期的上一个月末日期
#1.清理/etl/dwexp/crm下面的日期目录
#  清理（当前系统日期-17）到（当前系统日期-10）日期目录里面的数据文件，但要保留最近3个月末日期的文件
#2.查看/etl1/dwexp/crm这个目录下是否有 上月底日期 目录，且目录里面有数据文件
#  如果没有目录，或者目录里面是空的，则将/etl/dwexp/crm的上月底日期目录下的数据文件同步到/etl1/dwexp/crm上月底日期
#  否则什么也不做
#3.清理/etl1/dwexp/crm下面的日期目录，保留12个月的月末的数据即可
#用shell实现


#!/bin/bash

# 获取当前日期
current_date=$(date +%Y%m%d)

# 计算上月底日期
last_month_end_date=$(date -d "$(date +%Y-%m-01) -1 day" +%Y%m%d)

# 计算清理日期范围
start_date=$(date -d "$current_date -17 days" +%Y%m%d)
end_date=$(date -d "$current_date -10 days" +%Y%m%d)

# 清理/etl/dwexp/crm下日期目录
for ((date = start_date; date <= end_date; date++)); do
    if [ $date != $last_month_end_date ]; then
        rm -rf /etl/dwexp/crm/$date
    fi
done

# 清理/etl/dwexp/crm下日期目录
for ((date = $(date -d $start_date +%s); date <= $(date -d $end_date +%s); date += 86400)); do
    current_date=$(date -d @$date +%Y%m%d)
    if [ "$current_date" != "$last_month_end_date" ]; then
        rm -rf /etl/dwexp/crm/$current_date
    fi
done



# 检查/etl1/dwexp/crm是否有上月底日期目录并且目录不为空
if [ ! -d "/etl1/dwexp/crm/$last_month_end_date" ] || [ -z "$(ls -A /etl1/dwexp/crm/$last_month_end_date)" ]; then
    # 同步数据文件到/etl1/dwexp/crm
    rsync -av /etl/dwexp/crm/$last_month_end_date/ /etl1/dwexp/crm/$last_month_end_date/
fi

# 清理/etl1/dwexp/crm下日期目录，保留12个月的月末数据
for dir in $(ls -d /etl1/dwexp/crm/*/); do
    dir_name=$(basename $dir)
    if [[ $dir_name =~ ^[0-9]{6} ]]; then
        year_month=${dir_name:0:6}
        if [ $year_month -lt $(date -d "12 months ago" +%Y%m) ]; then
            rm -rf $dir
        fi
    fi
done
