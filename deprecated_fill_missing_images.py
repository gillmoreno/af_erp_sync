import pandas as pd
from apis.sql import query_sync_db

products_df = pd.read_csv("missing_images_products.csv")
variations_df = pd.read_csv("missing_images_variations.csv")

for i, row in products_df.iterrows():
    if isinstance(row["ImgPrincipale"], str):
        query = f"""
            UPDATE 
                SAM_GENITORI
            SET 
                ImgPrincipale='{row["ImgPrincipale"]}'
            WHERE 
                szCodice='{row["szCodice"]}';
        """
        print(query)
        query_sync_db(query, write=True)
        print(row["ImgPrincipale"])
    if isinstance(row["ImgGalleria"], str):
        query = f"""
            UPDATE 
                SAM_GENITORI
            SET 
                ImgGalleria='{row["ImgGalleria"]}'
            WHERE 
                szCodice='{row["szCodice"]}';
        """
        query_sync_db(query, write=True)
        print(row["ImgGalleria"])

for i, row in variations_df.iterrows():
    if isinstance(row["szImmagine"], str):
        query = f"""
            UPDATE 
                SAM_VARIATIONS
            SET 
                szImmagine='{row["szImmagine"]}'
            WHERE 
                szDescrizione='{row["szDescrizione"]}';
        """
        print(query)
        query_sync_db(query, write=True)
        print(row["szImmagine"])