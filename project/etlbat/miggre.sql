-- etl批处理程序的调度系统升级，需要使用新老调度并行去跑数据，但是oracle实例只有一个，怎么去比对新老调度执行一个日批后的结果呢


-- 1. 扩容表空间
create tablespace {tablespace_name} datafile 'TABLESPACE_QCJ.dbf' size 1024M autoextend on next 5M maxsize unlimited;;


-- 2. 创建用户crm2, 指定默认表空间
create user {username} IDENTIFIED BY {password} default tablespace {tablespace_name}
temporary tablespace {tempspace_name} profile DEFAULT;


-- 3. 授予crm, crm2用户能互相访问（只读权限）
GRANT CREATE SESSION TO source_user;
GRANT CREATE SESSION TO new_user;


-- 4. 数据同步
    a. 复制非分区表包含索引;
    SELECT DBMS_METADATA.GET_DDL('TABLE', 'old_table') FROM DUAL;

    b. 复制分区表重建分区;

    c. 重建其他对象（存储过程，函数，触发器，序列）;
        索引：
        SELECT DBMS_METADATA.GET_DDL('INDEX', index_name) AS index_ddl FROM user_indexes;

        触发器：
        SELECT DBMS_METADATA.GET_DDL('TRIGGER', trigger_name) AS trigger_ddl FROM user_triggers;

        函数：
        SELECT DBMS_METADATA.GET_DDL('FUNCTION', object_name) AS function_ddl FROM user_procedures
        WHERE object_type = 'FUNCTION';

        存储过程：
        SELECT DBMS_METADATA.GET_DDL('PROCEDURE', object_name) AS procedure_ddl FROM user_procedures
        WHERE object_type = 'PROCEDURE';

        主键
        SELECT 'ALTER TABLE ' || table_name || ' ADD CONSTRAINT ' || constraint_name || ' PRIMARY KEY (' || column_list || ');'
        FROM user_constraints
        WHERE constraint_type = 'P';

        外键
        SELECT 'ALTER TABLE ' || table_name || ' ADD CONSTRAINT ' || constraint_name || ' FOREIGN KEY (' || column_list || ') REFERENCES ' || r_table_name || ' (' || r_column_list || ');'
        FROM user_constraints
        WHERE constraint_type = 'R';




-- 5. Etl批脚本部署
    a.复制目录/cimcim/script_new/到新路径：(需要确认涉及的脚本，是否/cimcim/下面的都需要部署)
        cp -r /cimcim /cimcim/new/

    b.修改oracle配置文件后，修改涉及sqlplus调用的脚本（sqlload.sh）,改变配置文件的指向，
      检查其他脚本中是否有路径写死的情况

    c.新调度文档配置，改成调用新部署的脚本








-- 4. 同步所有对象（不包含数据）
DECLARE
  v_sql VARCHAR2(1000);
BEGIN
  FOR obj IN (SELECT object_name, object_type FROM all_objects WHERE owner = 'source_user') LOOP
    v_sql := 'CREATE ' || obj.object_type || ' new_user.' || obj.object_name || ' AS SELECT * FROM source_user.' || obj.object_name;
    EXECUTE IMMEDIATE v_sql;
  END LOOP;
END;
/

-- 5. 同步一天切片数据
DECLARE
  v_date DATE := DATE '2024-04-12'; -- 替换为实际日期
BEGIN
  FOR obj IN (SELECT table_name FROM all_tables WHERE owner = 'source_user' AND table_name LIKE 'table_name_%') LOOP
    EXECUTE IMMEDIATE 'INSERT INTO new_user.' || obj.table_name || ' SELECT * FROM source_user.' || obj.table_name || ' WHERE date_column = :1' USING v_date;
  END LOOP;
END;
/

-- 6. 重建索引
DECLARE
  v_sql VARCHAR2(1000);
BEGIN
  FOR idx IN (SELECT index_name FROM all_indexes WHERE owner = 'source_user') LOOP
    v_sql := 'CREATE INDEX new_user.' || idx.index_name || ' ON new_user.' || idx.index_name || ' ...'; -- 根据实际情况添加索引定义
    EXECUTE IMMEDIATE v_sql;
  END LOOP;
END;
/


我有一批需要加载的文件作业，文件名存在数据库配置作业表里面，当我开始一天的批量的时候，我从数据库读出这些文件接口名，
然后一直循环去判断这些文件是否生成，
    a.如果文件生成了，我就发送一条post请求给调度系统，调度系统就调用执行这个文件的ETL作业
    b.我还要在循环中使用post请求判断这个调度的任务状态，如果有这个job我就不执行a
    c.job如果完成了，数据库的这个配置作业表的日期加1



关于之前导包的问题，我有点疑问
dreams
└───project/
    ├──__init__.py
    ├── common/
    │   └──db.py
    │   └── __init__.py
    └── etlbat/
        └── role_allocate.py
        └── __init__.py
结构如上，我需要在role_allocate.py import db.py,我在role_allocate.py 中使用
from project.common.db import *
导入，结果我在pycharm里面可以执行，但是在cmd中直接使用python执行却报错了ModuleNotFoundError: No module named 'project'
在pycharm执行中的sys.path 是['D:\\cl\\dreams\\project\\etlbat', 'D:\\cl\\dreams', 'D:\\AppGallery\\Software\\PyCharm 2023.3.1\\plugins\\python\\helpers\\pycharm_display', 'D:\\AppGallery\\Software\\python\\python39.zip', 'D:\\AppGallery\\Software\\python\\DLLs', 'D:\\AppGallery\\Software\\python\\lib', 'D:\\AppGallery\\Software\\python', 'D:\\AppGallery\\Software\\python\\lib\\site-packages', 'D:\\AppGallery\\Software\\PyCharm 2023.3.1\\plugins\\python\\helpers\\pycharm_matplotlib_backend']
在cmd执行的sys.path 是['D:\\cl\\dreams\\project\\etlbat', 'D:\\AppGallery\\Software\\python\\python39.zip', 'D:\\AppGallery\\Software\\python\\DLLs', 'D:\\AppGallery\\Software\\python\\lib', 'D:\\AppGallery\\Software\\python', 'D:\\AppGallery\\Software\\python\\lib\\site-packages']


结构如下
test
└───a/
│   ├──__init__.py
│   ├── aa/
│   │   └──aaf.py
│   │── af.py
└───b/
│   └── bf.py
│   └── __init__.py
└───test.py

aaf.py代码：
def test2():
    print("aafaffff")

af.py代码：
from aa.aaf import test2
def af_print():
    print("afffff")
if __name__ == '__main__':
    test2()

test.py代码：
from a.af import af_print
af_print()

执行test.py 报错 ModuleNotFoundError: No module named 'aa'