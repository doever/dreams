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
END
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

