import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.auth import wcapi
from slugify import slugify
from loguru import logger

"""
Attributes, attributes terms and its translations must be created before the products and variations
"""


def search_attribute_by_slug(attribute_id: int, slug: str) -> dict:
    """
    Searches for an attribute term by its slug within a specific attribute.

    Args:
        attribute_id (int): The ID of the attribute to search within.
        slug (str): The slug of the attribute term to search for.

    Returns:
        dict: The first attribute term matching the slug, if found, within the specified attribute.
    """
    return wcapi.get(f"products/attributes/{str(attribute_id)}/terms?slug={slug}").json()


def create_attribute_term(attribute_id: int, option_it: str, option_en: str):
    """
    Creates a new attribute term under a given attribute and sets up its translation.

    Args:
        attribute_id (int): The ID of the attribute under which the term is to be created.
        option_it (str): The name of the attribute term in Italian.
        option_en (str): The name of the attribute term in English for translation purposes.

    Returns:
        int: The ID of the newly created attribute term.
    """
    data = {"name": option_it, "slug": slugify(option_it)}
    term = wcapi.post(f"products/attributes/{str(attribute_id)}/terms", data).json()
    translate_attribute_term(attribute_id, term["id"], option_en, slugify(option_en + "-en"))
    return term["id"]


def translate_attribute_term(
    attribute_id: int,
    original_attribute_term_id: int,
    translation: str,
    slug: str,
    lang: str = "en",
):
    """
    Adds a translation for an existing attribute term.

    Args:
        attribute_id (int): The ID of the attribute to which the term belongs.
        original_attribute_term_id (int): The ID of the attribute term to translate.
        translation (str): The translated name of the attribute term.
        slug (str): A slug for the translated term.
        lang (str, optional): The language code for the translation. Defaults to "en".

    Note:
        This function is part of the process of creating multilingual attribute terms, supporting
        e-commerce sites that operate in multiple languages.
    """
    data = {
        "name": translation,
        "translation_of": original_attribute_term_id,
        "slug": slug,
        "lang": lang,
    }
    attribute = wcapi.post(f"products/attributes/{str(attribute_id)}/terms", data).json()
    logger.info(f"attribute slug -> {attribute['slug']}")
