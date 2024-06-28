# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 migrate_index.py.py                                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script compares two files.                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/6/19                                                                      #
# License    : Copyright (c) 2024 by cl, All rights reserved                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


def create_index_statements(index_list):
    statements = []
    current_index = []
    for item in index_list:
        # 清除空白列表项
        if not item:
            continue

        # 如果开始新的索引创建，则清空当前索引的列表
        if item[0].startswith('CREATE INDEX'):
            if current_index:
                statements.append(' '.join(current_index))
                current_index = []

        # 将当前项添加到当前索引的列表中
        current_index.extend(item)

    # 不要忘记添加最后一个索引
    if current_index:
        statements.append(' '.join(current_index))

    return statements


# 提供的列表
index_list = [
                ['CREATE INDEX "CRM"."TMP_B_M_PCUS_CUST_MNG_IDX1" ON "CRM"."TMP_B_M_PCUS_CUST_MNG_RELA_C_1" ("CUST_ID")'],
                ['PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS'],
                ['STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645'],
                ['PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1'],
                ['BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)'],
                ['TABLESPACE "MDM_INDEXSPACE"'], [''], [''],
                ['CREATE INDEX "CRM"."TMP_B_M_PCUS_CUST_MNG_IDX2" ON "CRM"."TMP_B_M_PCUS_CUST_MNG_RELA_C_1" ("CUST_MNGR_ATTR_ORG_ID")'],
                ['PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS'],
                ['STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645'],
                ['PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1'],
                ['BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)'],
                ['TABLESPACE "MDM_INDEXSPACE"'], [''], [''],
                ['CREATE INDEX "CRM"."TMP_B_M_PCUS_CUST_MNG_IDX3" ON "CRM"."TMP_B_M_PCUS_CUST_MNG_RELA_C_1" ("CUST_MNGR_ATTR_ORG_ID1")'],
                [''],
                ['PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS'],
                ['STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645'],
                ['PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1'],
                ['BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)'],
                ['TABLESPACE "MDM_INDEXSPACE"'], [''], [''],
                ['CREATE INDEX "CRM"."TMP_B_M_PCUS_CUST_MNG_IDX4" ON "CRM"."TMP_B_M_PCUS_CUST_MNG_RELA_C_1" ("CUST_MNGR_ATTR_ORG_ID2")'],
                [''],
                ['PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS'],
                ['STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645'],
                ['PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1'],
                ['BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)'],
                ['TABLESPACE "MDM_INDEXSPACE"'], [''], [''],
                ['CREATE INDEX "CRM"."TMP_B_M_PCUS_CUST_MNG_IDX5" ON "CRM"."TMP_B_M_PCUS_CUST_MNG_RELA_C_1" ("CUST_MNGR_ATTR_ORG_ID3")'],
                [''],
                ['PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS'],
                ['STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645'],
                ['PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1'],
                ['BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)'],
                ['TABLESPACE "MDM_INDEXSPACE"']
              ]

# 调用函数并打印结果
sql_statements = create_index_statements(index_list)
for stmt in sql_statements:
    print(stmt + ';')