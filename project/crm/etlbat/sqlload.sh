#!/bin/sh

# Debug
debug_log(){
    local message=$1
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "${timestamp} [debug] ${message}" >> ${DebugLog}
}

handle_interrupt(){
    interruptlogfile="/etl/dwexp/log/debug.interruptlog"
    env >> ${interruptlogfile}
    top -b -n1 | grep "Cpu" >> ${interruptlogfile}
    top -b -n1 | grep "Mem" >> ${interruptlogfile}
    debug_log "program exit unexpect."
    exit 998
}

showhelp()
{
    echo "usage: sh `basename $0` [-a 'sourcefile'] [-b 'format'] [-t 'targettable'] [-d 'workdt'] [-f 'path']"
    echo "mevery param can not empty,please check!"
}

checkvalue()
{
    if [ "" = "$workdt" -o "" = "$targettable" -o "" = "$sourcefile" -o "" = "$format" -o "" = "$path" ];then
        showhelp
        exec_result=1
        run_log
        exit 3
    fi
}

sqlload()
{
    if [ ! -d "/etl/dwexp/log/${workdt}/" ];then
        mkdir /etl/dwexp/log/${workdt}
        chmod -R 777 /etl/dwexp/log/${workdt}
    fi
    debug_log "begin function sqlload."

    if [[ `cat $ctlfilename | grep "char(20000)"` || `cat $ctlfilename | grep "char(200000)"` ]] > /dev/null
    then
    debug_log "load big column files."
    echo "LOAD command :$ORACLE_HOME/bin/sqlldr userid=***** control=$ctlfilename data=$datafile log=$logfilename bad=$badfilename rows=100000 readsize=104857600 bindsize=104857600 errors=0 parallel=true" >> ${DebugLog}
    $ORACLE_HOME/bin/sqlldr userid=$strConn control=$ctlfilename data=$datafile log=$logfilename bad=$badfilename rows=100000 readsize=104857600 bindsize=104857600 errors=0 parallel=true >> ${DebugLog} 2>&1
    else
    debug_log "load small column files."
    echo "LOAD command :$ORACLE_HOME/bin/sqlldr userid=***** control=$ctlfilename data=$datafile log=$logfilename bad=$badfilename  multithreading=true errors=0 direct=y" >> ${DebugLog}
    $ORACLE_HOME/bin/sqlldr userid=$strConn control=$ctlfilename data=$datafile log=$logfilename bad=$badfilename multithreading=true errors=0 direct=y  >> ${DebugLog}  2>&1

    debug_log "end sqlload command."

    if [ -e "${badfilename}" ];then
        echo "load failed,please read ${badfilename} and ${logfilename}"
        exec_result=3
        run_log
        exit 3
    fi


    debug_log "end function sqlload."
}
GetTime()
{
    [ $# -ne 1 ] && echo "Usage: `basename $0` difftime" && exit 1
    DiffTime=$1
    hour=$(( DiffTime/3600 ))
    hour_mod=$(( DiffTime%3600 ))

    min=$(( hour_mod/60 ))
    seconds=$(( hour_mod%60 ))

    printf "%2dh%2dm%2ds\n" ${hour} ${min} ${seconds}
}

run_log(){
Edtime=$(date +%s)
DiffTime=$((Edtime-Bgtime))
sql="insert into F_CM_SQLLOAD_LOG_INFO(file_name, target_table, work_dt, exec_result, beg_date, end_date, run_time, para1, para2, para3)"
sql1="select '"${sourcefile}.${format}"','"${targettable}"',"${workdt},${exec_result}",to_date('"`date -d @${Bgtime} +"%Y-%m-%d %H:%M:%S"`"','YYYY-MM-DD hh24:mi:ss'),to_date('"`date -d @${Edtime} +"%Y-%m-%d %H:%M:%S"`"','YYYY-MM-DD hh24:mi:ss'),'"`GetTime $DiffTime`"','"${linelog}"',null,null from dual;"
sql2="COMMIT;"
 sqlplus -S ${strConn} <<-!!! >/dev/null
 set serveroutput on;
 $sql
 $sql1
 $sql2
 !!!

# Debug
echo ${sql} >> ${DebugLog}
echo ${sql1} >> ${DebugLog}
echo ${sql2} >> ${DebugLog}

}


trap 'handle_interrupt' INT TERM HUP QUIT
info_a="begin.."

Bgtime=$(date +%s)
for line in `cat /cimcim/conf/db.conf`
do
eval "$line"
done

dbuser=$dbuser
dbpass=$dbpass
dbhost=$dbhost

dbuser=`echo $dbuser | openssl base64 -d`
dbpass=`echo $dbpass | openssl base64 -d`
dbhost=`echo $dbhost | openssl base64 -d`

strConn=$dbuser/$dbpass@$dbhost

info_b="parse db option."


while getopts 'a:b:t:d:f:' OPT; do
    case $OPT in
        a|+a)sourcefile="$OPTARG";;
        b|+b)format="$OPTARG";;
        t|+t)targettable="$OPTARG";;
        f|+f)path="$OPTARG";;
        d|+)workdt="$OPTARG";;
        *)showhelp
          exec_result=1
          run_log
          exit 1
    esac
done

info_c="parse user options."

# Debug
DebugLog=/etl/dwexp/log/${workdt}/${sourcefile}_${workdt}.debuglog
env > ${DebugLog}
top -b -n1 | grep "Cpu" >> ${DebugLog}
top -b -n1 | grep "Mem" >> ${DebugLog}

debug_log $info_a
debug_log $info_b
debug_log $info_c
debug_log "load ${sourcefile} to ${targettable}"

linelog="107_$?"
exec_result=107
run_log

debug_log "check value."
checkvalue

ctlfilename=/cimcim/script/ctl/${targettable}.ctl
logfilename=/etl/dwexp/log/${workdt}/${targettable}_${workdt}.log
badfilename=/etl/dwexp/log/${workdt}/${targettable}_${workdt}.bad

case $path in
    0)
        datafile=/etl/dwexp/crm/${workdt}/${sourcefile}_${workdt}.${format}
        ;;
    1)
        datafile=/etl/dwexp/crm/retail/${workdt}/${sourcefile}_${workdt}.${format}
        ;;
    2)
        datafile=/etl/dwexp/crm/T24/tmp/${sourcefile}.${format}
        ;;
    *)  exec_result=4
        run_log
        exit 4
esac

debug_log "join the data file path."

if [ ! -f $datafile ];then
    exec_result=5
    run_log
    exit 5
fi

debug_log "check data file is exists"

if [ -e $logfilename ];then
    rm -f $logfilename
fi

debug_log "remove log file."

if [ -e $badfilename ];then
    rm -f $badfilename
fi

debug_log "remove bad file."

linelog="146_$?"
exec_result=146
run_log

debug_log "begin sqlload script."

sqlload

linelog="152_$?"
exec_result=0
run_log

debug_log "end sqlload script"