import random

seed = 12
excluded_products_ratio = 20


class PseudorandomAlgorithm:
    @staticmethod
    def exclude_products(products):
        excluded_products_number = round(len(products) / excluded_products_ratio)
        random.seed(seed)
        excluded_products = random.sample(products, excluded_products_number)
        return excluded_products
