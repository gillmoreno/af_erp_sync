from auth import wcapi

"""
Attributes, attributes terms and its translations must be created befor the products and variations
"""

def list_all_attributes_terms(attribute_id: int):
    print(wcapi.get(f"products/attributes/{str(attribute_id)}/terms").json())

def translate_attribute_term(attribute_id: int, original_attribute_term_id: int, translation: str, slug: str, lang: str = "en"):
    data = {
        'name': translation,
        'translation_of': original_attribute_term_id,
        'slug': slug,
        'lang': lang
    }
    print(wcapi.post(f"products/attributes/{str(attribute_id)}/terms", data).json())