"""
This script updates the database with missing cover images and gallery images for products and variations.

It reads from 'missing_images_products.csv' and 'missing_images_variations.csv' to find the image URLs that need to be updated. For each product and variation listed in the CSV files, it constructs and executes SQL UPDATE statements to fill in missing cover and gallery images in the database.

The script utilizes pandas for reading and iterating over CSV data, and a custom database interaction function `query_sync_db` for executing the SQL queries.

Attributes:
    products_df (DataFrame): A DataFrame containing product data extracted from 'missing_images_products.csv', including columns for ERP IDs and image URLs.
    variations_df (DataFrame): A DataFrame containing variation data extracted from 'missing_images_variations.csv', including columns for ERP IDs and image URLs.

Note:
    This script is intended to be run as a standalone utility and assumes the existence of 'missing_images_products.csv' and 'missing_images_variations.csv' in the same directory. It also requires database access credentials to be properly configured in the environment.
"""

import pandas as pd
from apis.sql import query_sync_db

products_df = pd.read_csv("missing_images_products.csv")
variations_df = pd.read_csv("missing_images_variations.csv")

# for i, row in products_df.iterrows():
#     if isinstance(row["cover_image"], str):
#         query = f"""
#             UPDATE
#                 products
#             SET
#                 cover_image='{row["cover_image"]}'
#             WHERE
#                 id_sam_erp='{row["id_sam_erp"]}';
#         """
#         print(query)
#         query_sync_db(query, write=True)
#         print(row["cover_image"])
#     if isinstance(row["gallery"], str):
#         query = f"""
#             UPDATE
#                 products
#             SET
#                 gallery='{row["gallery"]}'
#             WHERE
#                 id_sam_erp='{row["id_sam_erp"]}';
#         """
#         query_sync_db(query, write=True)
#         print(row["gallery"])

for i, row in variations_df.iterrows():
    if isinstance(row["image_"], str):
        query = f"""
            UPDATE 
                variations
            SET 
                image_='{row["image_"]}'
            WHERE 
                sku='{row["sku"]}';
        """
        print(query)
        query_sync_db(query, write=True)
        print(row["image_"])
