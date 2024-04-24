-- etl批处理程序的调度系统升级，需要使用新老调度并行去跑数据，但是oracle实例只有一个，怎么去比对新老调度执行一个日批后的结果呢


-- 1. 创建表空间
create tablespace {tablespace_name} datafile 'TABLESPACE_QCJ.dbf' size 1024M autoextend on next 5M maxsize unlimited;;

-- 2. 创建用户
create user {username} IDENTIFIED BY {password} default tablespace {tablespace_name}
temporary tablespace {tempspace_name} profile DEFAULT;


-- 3. 授予两个用户能互相访问（只读权限）
GRANT CREATE SESSION TO source_user;
GRANT CREATE SESSION TO new_user;

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

