from model.product_day_mean_entity import ProductDayMean


class UcbAlgorithm:
    @staticmethod
    def exclude_products(products, beta):
        excluded_products = []
        for product in products:
            mean = product[ProductDayMean.MEAN]
            std_dev = product[ProductDayMean.STD_DEV]
            ucb_value = mean + std_dev * beta
            if ucb_value < 0:
                excluded_products.append(product)
        return excluded_products
