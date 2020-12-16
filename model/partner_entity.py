class Partner:
    ID = 0
    PARTNER_ID = 1
    TOTAL_SALES_AMOUNT = 2
    TOTAL_CLICKS_NUMBER = 3
    SINGLE_CLICK_COST = 4

    drop_partner_table_script = "DROP TABLE IF EXISTS PARTNER;"
    create_partner_table_script = "CREATE TABLE PARTNER (" \
                          "ID INT AUTO_INCREMENT PRIMARY KEY," \
                          "PARTNER_ID VARCHAR(32)," \
                          "TOTAL_SALES_AMOUNT FLOAT," \
                          "TOTAL_CLICKS_NUMBER INT," \
                          "SINGLE_CLICK_COST FLOAT" \
                          ");"
    insert_partner_entity_script = "INSERT INTO PARTNER (" \
                          "PARTNER_ID," \
                          "TOTAL_SALES_AMOUNT," \
                          "TOTAL_CLICKS_NUMBER," \
                          "SINGLE_CLICK_COST" \
                          ")" \
                          "VALUES (%s,%s,%s,%s);"
    select_distinct_partner_id_script = "SELECT DISTINCT PARTNER_ID FROM PARTNER;"
    select_all_where_partner_id_script = "SELECT * FROM PARTNER WHERE PARTNER_ID = %(partner_id)s;"