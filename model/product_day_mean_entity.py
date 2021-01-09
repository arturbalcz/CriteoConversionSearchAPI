class ProductDayMean:
    ID = 0
    PRODUCT_DAY_ID = 1
    DAILY_PROFIT = 2
    DAILY_COST = 3
    MEAN = 4
    STD_DEV = 5

    drop_product_day_table_script = "DROP TABLE IF EXISTS PRODUCT_DAY_MEAN;"
    create_product_day_table_script = "CREATE TABLE PRODUCT_DAY_MEAN (" \
                      "ID INT AUTO_INCREMENT PRIMARY KEY," \
                      "PRODUCT_DAY_ID INT," \
                      "DAILY_PROFIT FLOAT," \
                      "DAILY_COST FLOAT," \
                      "MEAN FLOAT," \
                      "STD_DEV FLOAT" \
                      ");"
    insert_product_day_entity_script = "INSERT INTO PRODUCT_DAY_MEAN (" \
                      "PRODUCT_DAY_ID," \
                      "DAILY_PROFIT," \
                      "DAILY_COST," \
                      "MEAN," \
                      "STD_DEV" \
                      ")" \
                      "VALUES (%s,%s,%s,%s,%s);"
