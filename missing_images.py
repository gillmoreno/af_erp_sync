import json
import pandas as pd
import questionary

PRODUCT_COLS = ["szCodice", "szDescrizione", "ImgPrincipale", "ImgGalleria"]
VARIATION_COLS = ["szArticoloID", "szImmagine", "szDescrizione"]

def create_missing_images_csv(is_product: bool):
    prefix = "products" if is_product else "variations"
    columns = PRODUCT_COLS if is_product else VARIATION_COLS
    
    with open(f"{prefix}.json", 'r') as f:
        data = json.load(f)

    d = data["data"]
    df = pd.DataFrame(d)
    df = df.loc[:, columns]
    df.to_csv(f"missing_images_{prefix}.csv", index=False)

def main():
    choices = [
        {"name": "Product", "value": True},
        {"name": "Variation", "value": False}
    ]
    is_product = questionary.select(
        "Select whether to create missing images CSV for a Product or Variation:",
        choices=choices
    ).ask()

    create_missing_images_csv(is_product)

if __name__ == "__main__":
    main()