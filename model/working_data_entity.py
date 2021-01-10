class WorkingData:
    ID = 0
    SALE = 1
    SALES_AMOUNT = 2
    PRODUCT_ID = 3
    PARTNER_ID = 4
    CLICK_DATE = 5

    drop_table_script = "DROP TABLE IF EXISTS WORKING_DATA;"
    create_table_script = "CREATE TABLE IF NOT EXISTS WORKING_DATA (" \
                            "ID INT AUTO_INCREMENT PRIMARY KEY," \
                            "SALE INT," \
                            "SALES_AMOUNT FLOAT," \
                            "PRODUCT_ID VARCHAR(32)," \
                            "PARTNER_ID VARCHAR(32)," \
                            "CLICK_DATE DATE" \
                            ");"
    insert_entity_script = "INSERT INTO WORKING_DATA (" \
                             "SALE," \
                             "SALES_AMOUNT," \
                             "PRODUCT_ID," \
                             "PARTNER_ID," \
                             "CLICK_DATE" \
                             ")" \
                             "VALUES (%s,%s,%s,%s,%s);"
    select_distinct_product_id = "SELECT DISTINCT PRODUCT_ID FROM WORKING_DATA"
    select_distinct_click_day_where_product_id_script = "SELECT DISTINCT CLICK_DATE FROM WORKING_DATA WHERE PRODUCT_ID = %(product_id)s;"
    select_all_where_click_date_and_product_id_script = "SELECT * FROM WORKING_DATA WHERE CLICK_DATE = %(click_date)s AND PRODUCT_ID = %(product_id)s;"
    delete_all_script = "DELETE FROM WORKING_DATA"