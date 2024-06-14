--配置表
create table migrate_table_conf(
table_name varchar2(30),
is_partition varchar2(10),
partition_column varchar2(30),
is_migrate varchar2(10),
object_type varchar2(20),
size varchar2(30)
);


--同步脚本的日志表
create table migrate_result(
object_name varchar2(30),
is_partition varchar2(10),
partition_column varchar2(30),
is_migrate varchar2(10),
object_type varchar2(20),
size varchar2(30)
);

--比对日志表


