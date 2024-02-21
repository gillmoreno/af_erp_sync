"""
A utility script for generating CSV files listing products or variations with missing image data.

This script reads from JSON files containing product or variation data, allows the user to select
whether to process products or variations, and generates a CSV file listing the items with their
relevant details and missing image information.

Functions:
    create_missing_images_csv(is_product: bool):
        Generates a CSV file listing either products or variations with missing image data.

    main():
        Entry point for the script, handling user input to select between products or variations
        and invoking the CSV generation process.

Usage:
    Run this script directly to start the process of generating a CSV file for products or variations
    with missing images. The script requires the presence of 'products.json' or 'variations.json' in
    the same directory, depending on the user's selection.

Note:
    This script uses `questionary` for interactive user prompts and `pandas` for data manipulation
    and CSV file generation.
"""

import json
import pandas as pd
import questionary

PRODUCT_COLS = ["id_sam_erp", "szDescrizione", "cover_image", "gallery"]
VARIATION_COLS = ["sku", "image_", "szDescrizione"]


def create_missing_images_csv(is_product: bool):
    """
    Generates a CSV file listing products or variations with missing image data from a JSON source.

    Args:
        is_product (bool): Determines whether to process products (True) or variations (False).

    The function reads from a JSON file ('products.json' or 'variations.json'), extracts relevant data
    into a pandas DataFrame, and saves it to a CSV file ('missing_images_products.csv' or
    'missing_images_variations.csv'), listing items with their details and missing image information.
    """
    prefix = "products" if is_product else "variations"
    columns = PRODUCT_COLS if is_product else VARIATION_COLS

    with open(f"{prefix}.json", "r") as f:
        data = json.load(f)

    d = data["data"]
    df = pd.DataFrame(d)
    df = df.loc[:, columns]
    df.to_csv(f"missing_images_{prefix}.csv", index=False)


def main():
    choices = [{"name": "Product", "value": True}, {"name": "Variation", "value": False}]
    is_product = questionary.select(
        "Select whether to create missing images CSV for a Product or Variation:", choices=choices
    ).ask()

    create_missing_images_csv(is_product)


if __name__ == "__main__":
    main()
