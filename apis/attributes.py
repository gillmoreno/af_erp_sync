from auth import wcapi
from slugify import slugify

"""
Attributes, attributes terms and its translations must be created befor the products and variations
"""

def search_attribute_by_slug(attribute_id: int, slug: str) -> dict:
    return wcapi.get(f"products/attributes/{str(attribute_id)}/terms?slug={slug}").json()

def create_attribute_term(attribute_id: int, option_it: str, option_en: str) :
    data = {
        "name": option_it,
        "slug": slugify(option_it)
    }
    term = wcapi.post(f"products/attributes/{str(attribute_id)}/terms", data).json()
    translate_attribute_term(attribute_id, term['id'], option_en, slugify(option_en + '-en'))

def translate_attribute_term(attribute_id: int, original_attribute_term_id: int, translation: str, slug: str, lang: str = "en"):
    data = {
        'name': translation,
        'translation_of': original_attribute_term_id,
        'slug': slug,
        'lang': lang
    }
    print(wcapi.post(f"products/attributes/{str(attribute_id)}/terms", data).json())