class ProductStatistics:
    PRODUCT_ID = 0
    DAILY_PROFIT = 3
    DAILY_COST = 4
    MEAN = 5
    STD_DEV = 6

    select_products_statistics_where_partner_id_and_day_script = 'SELECT PRODUCT_ID, DAILY_PROFIT, DAILY_COST, MEAN, STD_DEV FROM PRODUCT_DAY JOIN PRODUCT_DAY_MEAN PDM ON PRODUCT_DAY.ID = PDM.PRODUCT_DAY_ID WHERE PARTNER_ID = %(partner_id)s AND DAY_DATE = %(date)s ORDER BY PRODUCT_ID;'
    select_products_seen_so_far_where_partner_id_and_day_script = 'WITH products_dates AS (SELECT PRODUCT_ID, DAILY_PROFIT, DAILY_COST, MEAN, STD_DEV, DAY_DATE FROM PRODUCT_DAY JOIN PRODUCT_DAY_MEAN PDM ON PRODUCT_DAY.ID = PDM.PRODUCT_DAY_ID WHERE PARTNER_ID = %(partner_id)s AND DAY_DATE <= %(date)s) SELECT * FROM (SELECT PRODUCT_ID, MAX(DAY_DATE) max FROM products_dates GROUP BY PRODUCT_ID) q JOIN products_dates ON q.PRODUCT_ID = products_dates.PRODUCT_ID AND q.max = products_dates.DAY_DATE ORDER BY q.PRODUCT_ID;'
