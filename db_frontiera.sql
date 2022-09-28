CREATE DATABASE erp_integration;

USE erp_integration;

CREATE TABLE products(
    id_sam_erp VARCHAR(32) NOT NULL,
    id_wp INT,
    title_it VARCHAR(64) NOT NULL,
    title_en VARCHAR(64) NOT NULL,
    category VARCHAR(64) NOT NULL,
    tags VARCHAR(64),
    meta_description_it VARCHAR(256) NOT NULL,
    meta_description_en VARCHAR(256) NOT NULL,
    cover_image VARCHAR(256) NOT NULL,
    gallery VARCHAR(2056),
    description_it TEXT NOT NULL,
    description_en TEXT NOT NULL,
    small_description_it TEXT NOT NULL,
    small_description_en TEXT NOT NULL,
    dimensions_options VARCHAR(512) NOT NULL,
    colors_options_it VARCHAR(512) NOT NULL,
    colors_options_en VARCHAR(512) NOT NULL,
    in_sync BOOLEAN,
    PRIMARY KEY (id_sam_erp)
);

CREATE TABLE variations(
    sku VARCHAR(32) NOT NULL,
    id_parent_sam_erp INT NOT NULL,
    id_wp INT,
    description_it TEXT NOT NULL,
    description_en TEXT NOT NULL,
    configurator INT,
    quantity_minimum INT,
    quantity_multiplier INT,
    stock FLOAT NOT NULL,
    price FLOAT NOT NULL,
    image_ VARCHAR(256),
    color_it VARCHAR(64),
    color_en VARCHAR(64),
    dimensions VARCHAR(64),
    length_ SMALLINT,
    width SMALLINT,
    height SMALLINT,
    in_sync BOOLEAN,
    PRIMARY KEY (sku)
);



CREATE TABLE orders(
    id_wp INT NOT NULL,
    id_sam_erp VARCHAR(32),
    quantity FLOAT NOT NULL,
    email_to_af_sent BOOLEAN,
    is_custom BOOLEAN,
    custom_image_url VARCHAR(2056),
    customer_id_sam_erp INT,
    customer_id_wp INT NOT NULL,
    shipping_id_sam_erp INT,
    shipping_id_wp INT NOT NULL,
    order_status VARCHAR(16),
    -- shipping_address VARCHAR(512) NOT NULL,
    -- shipping_email VARCHAR(64),
    -- shipping_contact_name VARCHAR(128),
    -- shipping_company_name VARCHAR(256),
);

CREATE TABLE shipments(
    
)

CREATE TABLE customers(
    id_wp INT NOT NULL,
    id_sam_erp VARCHAR(32),
    email VARCHAR(64),
    contact_name VARCHAR(128),
    company_name VARCHAR(256),
    vat_number VARCHAR(16),
    is_active_wp BOOLEAN NOT NULL,
    activation_email_sent BOOLEAN NOT NULL,
    wp_needs_sync BOOLEAN NOT NULL,
    sam_erp_needs_sync BOOLEAN NOT NULL,
    address VARCHAR(256),
    PRIMARY KEY (id_wp)
);