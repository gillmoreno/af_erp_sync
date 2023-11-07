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