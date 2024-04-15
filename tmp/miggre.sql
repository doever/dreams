-- etl批处理程序的调度系统升级，需要使用新老调度并行去跑数据，但是oracle实例只有一个，怎么去比对新老调度执行一个日批后的结果呢


-- 1. 创建表空间
create tablespace {tablespace_name} datafile 'TABLESPACE_QCJ.dbf' size 1024M autoextend on next 5M maxsize unlimited;;

-- 2. 创建用户
create user {username} IDENTIFIED BY {password} default tablespace {tablespace_name}
temporary tablespace {tempspace_name} profile DEFAULT;


-- 3. 授予两个用户能互相访问
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
