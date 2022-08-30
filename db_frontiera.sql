CREATE DATABASE erp_integration;

USE erp_integration;

CREATE TABLE products(
    id_wp INT NOT NULL,
    id_sam_erp VARCHAR(32) NOT NULL,
    name VARCHAR(64) NOT NULL,
    categories VARCHAR(64) NOT NULL, #MANY TO MANY?
    tags VARCHAR(64) NOT NULL, #MANY TO MANY?
    stock FLOAT NOT NULL,
    price FLOAT NOT NULL,
    photo_url VARCHAR(2056),
    description_it TEXT,
    description_en TEXT,
    small_description_it VARCHAR(1024),
    small_description_en VARCHAR(1024),
    length SMALLINT,
    width SMALLINT,
    height SMALLINT,
    in_sync BOOLEAN,
    PRIMARY KEY (id_wp)
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
    order_status VARCHAR(16),
    shipping_address VARCHAR(512) NOT NULL,  
);

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