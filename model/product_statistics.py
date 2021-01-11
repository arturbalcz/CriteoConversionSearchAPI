class ProductStatistics:
    PRODUCT_ID = 0
    DAILY_PROFIT = 1
    DAILY_COST = 2
    MEAN = 3
    STD_DEV = 4

    select_products_statistics_where_partner_id_and_day_script = 'SELECT PRODUCT_ID, DAILY_PROFIT, DAILY_COST, MEAN, STD_DEV FROM PRODUCT_DAY JOIN PRODUCT_DAY_MEAN PDM ON PRODUCT_DAY.ID = PDM.PRODUCT_DAY_ID WHERE PARTNER_ID = %(partner_id)s AND DAY_DATE = %(date)s ORDER BY PRODUCT_ID;'