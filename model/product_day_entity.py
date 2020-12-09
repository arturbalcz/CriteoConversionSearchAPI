drop_product_day_table_script = "DROP TABLE IF EXISTS PRODUCT_DAY;"
create_product_day_table_script = "CREATE TABLE PRODUCT_DAY (" \
                      "ID INT AUTO_INCREMENT PRIMARY KEY," \
                      "PRODUCT_ID VARCHAR(32)," \
                      "PARTNER_ID VARCHAR(32)," \
                      "DAILY_SALES_AMOUNT FLOAT," \
                      "DAILY_CLICKS_NUMBER INT, " \
                      "DAILY_SALES_NUMBER INT," \
                      "DAY_DATE DATE," \
                      "PRODUCT_PRICE FLOAT," \
                      ");"
insert_click_entity_script = "INSERT INTO PRODUCT_DAY (" \
                       "PRODUCT_ID," \
                       "PARTNER_ID," \
                       "DAILY_SALES_AMOUNT," \
                       "DAILY_CLICKS_NUMBER," \
                       "DAILY_SALES_NUMBER," \
                       "DAY_DATE," \
                       "PRODUCT_PRICE" \
                       "VALUES (%s,%s,%s,%s,%s,%s,%s)"
