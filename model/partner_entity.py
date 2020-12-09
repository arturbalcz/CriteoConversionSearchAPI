drop_product_day_table_script = "DROP TABLE IF EXISTS PARTNER;"
create_product_day_table_script = "CREATE TABLE PARTNER (" \
                      "ID INT AUTO_INCREMENT PRIMARY KEY," \
                      "PARTNER_ID VARCHAR(32)," \
                      "TOTAL_SALES_AMOUNT FLOAT," \
                      "TOTAL_CLICKS_NUMBER INT," \
                      "SINGLE_CLICK_COST FLOAT," \
                      ");"
