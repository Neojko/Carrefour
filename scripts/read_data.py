from xml.sax.handler import DTDHandler
import pandas as pd

ORDERS_FILE = "data/orders.csv"
DELIVERIES_FILE = "data/deliveries.csv"
PRODUCT_IFLS_FILE = "data/product_ifls.csv"
SALES_FILE = "data/sales.csv"
STOCKS_FILE = "data/stocks.csv"

def main():

    # orders_df = pd.read_csv(ORDERS_FILE,  dtype=str)
    # deliveries_df = pd.read_csv(DELIVERIES_FILE,  dtype=str)
    # check_quantity_differences(orders_df, deliveries_df)

    # sales_df = pd.read_csv(SALES_FILE)
    # number_of_products = sales_df.barcode.nunique(dropna = True)
    # number_of_days = sales_df.dateKey.nunique(dropna = True)
    # number_of_rows = len(sales_df.index)


    # product_ifls_df = read_and_clean_product_ifls_df()
    # number_of_products = product_ifls_df.barcode.nunique(dropna = True)
    # number_of_cases = product_ifls_df.prdIflsCode.nunique(dropna = True)

    stocks_df = pd.read_csv(STOCKS_FILE, dtype=str)
    number_of_products = stocks_df.barcode.nunique(dropna = True)
    number_of_days = stocks_df.datekey.nunique(dropna = True)
    number_of_rows = len(stocks_df.index)
    stocks_df['Combo'] = stocks_df['barcode'] + stocks_df['datekey']
    number_of_entries = stocks_df.Combo.nunique(dropna= True)

    a = 4


def read_and_clean_product_ifls_df():
    product_ifls_df = pd.read_csv(PRODUCT_IFLS_FILE)
    # Keep 3 columns (product, package, quantity)
    return product_ifls_df

def check_quantity_differences(orders_df, deliveries_df):
    #comparison_df = pd.merge(orders_df, deliveries_df, on=["orderKey", "barcode"])
    order_keys_in_orders = orders_df.orderKey.unique()
    order_keys_in_deliveries = deliveries_df.orderKey.unique()
    common_order_keys = set(order_keys_in_orders).union(order_keys_in_deliveries)
    number_of_common_order_keys = len(common_order_keys)
    order_keys_only_in_orders = set(order_keys_in_orders).difference(order_keys_in_deliveries)
    number_of_order_keys_only_in_orders = len(order_keys_only_in_orders)
    order_keys_only_in_deliveries = set(order_keys_in_deliveries).difference(order_keys_in_orders)
    number_of_order_keys_only_in_deliveries = len(order_keys_only_in_deliveries)
    number_of_products_in_orders = orders_df.barcode.nunique(dropna = True)
    number_of_products_in_deliveries = deliveries_df.barcode.nunique(dropna = True)

    a = 3


if __name__ == "__main__":
    main()