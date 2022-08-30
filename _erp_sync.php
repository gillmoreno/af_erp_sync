<?php

if ( ! defined( 'ABSPATH' ) ) {
    /** Set up WordPress environment */
    require_once __DIR__ . '/wp-load.php';
}

include_once __DIR__ . '/wp-content/plugins/woocommerce/includes/class-wc-product-simple.php';

function createProduct($name, $description, $price){
    $product = new WC_Product_Simple();
    $product->set_name($name);
    $product->set_slug(slugify($name));
    $product->set_description($description);
    $product->set_regular_price($price);
    $product->save();
    $product_id = $product->get_id();
    print $product_id;
}

function slugify($text, string $divider = '-') {
    // replace non letter or digits by divider
    $text = preg_replace('~[^\pL\d]+~u', $divider, $text);
    // transliterate
    $text = iconv('utf-8', 'us-ascii//TRANSLIT', $text);
    // remove unwanted characters
    $text = preg_replace('~[^-\w]+~', '', $text);
    // trim
    $text = trim($text, $divider);
    // remove duplicate divider
    $text = preg_replace('~-+~', $divider, $text);
    // lowercase
    $text = strtolower($text);
    if (empty($text)) {
        return 'n-a';
    }

    return $text;
}

// php -r $'require "_erp_sync.php"; createProduct("Altro\' Fake", "una descrizione fake", 1500);'

// https://rudrastyh.com/woocommerce/create-product-programmatically.html

?>