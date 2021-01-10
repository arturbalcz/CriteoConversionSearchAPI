from model.product_statistics import ProductStatistics


class UcbAlgorithm:
    @staticmethod
    def exclude_products(products, beta):
        excluded_products = []
        for product in products:
            mean = product[ProductStatistics.MEAN]
            std_dev = product[ProductStatistics.STD_DEV]
            ucb_value = mean + std_dev * beta
            if ucb_value < 0:
                excluded_products.append(product)
        return excluded_products
