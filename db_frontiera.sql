CREATE DATABASE erp_integration;

USE erp_integration;

CREATE TABLE products(
    id_sam_erp VARCHAR(32) NOT NULL,
    id_wp INT,
    id_wp_en INT,
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
    short_description_it TEXT NOT NULL,
    short_description_en TEXT NOT NULL,
    in_sync BOOLEAN,
    PRIMARY KEY (id_sam_erp)
);

CREATE TABLE variations(
    sku VARCHAR(32) NOT NULL,
    id_parent_sam_erp INT NOT NULL,
    id_wp INT,
    id_wp_en INT,
    description_it TEXT NOT NULL,
    description_en TEXT NOT NULL,
    configurator_it INT,
    configurator_en INT,
    configurator_page_it INT,
    configurator_page_en INT,
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
    is_active BOOLEAN,
    PRIMARY KEY (sku)
);

CREATE TABLE customers(
    id_wp INT NOT NULL,
    id_sam_erp VARCHAR(32),
    wp_needs_sync BOOLEAN DEFAULT 0,
    sam_erp_needs_sync BOOLEAN DEFAULT 0,
    pw_user_status VARCHAR(32),
    email VARCHAR(64),
    username VARCHAR(128),
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    vat_number VARCHAR(16),
    PRIMARY KEY (id_wp)
);

CREATE TABLE billing_addresses(
    id_wp_customer INT NOT NULL,
    id_sam_erp VARCHAR(32),
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    company VARCHAR(256),
    address_1 VARCHAR(256),
    address_2 VARCHAR(256),
    city VARCHAR(64),
    state_ VARCHAR(64),
    postcode VARCHAR(16),
    country VARCHAR(64),
    email VARCHAR(64),
    phone VARCHAR(64),
    PRIMARY KEY (id_wp_customer)
);

CREATE TABLE shipping_addresses(
    id INT NOT NULL AUTO_INCREMENT,
    id_sam_erp VARCHAR(32),
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    company VARCHAR(256),
    address_1 VARCHAR(256),
    address_2 VARCHAR(256),
    city VARCHAR(64),
    state_ VARCHAR(64),
    postcode VARCHAR(16),
    country VARCHAR(64),
    PRIMARY KEY (id)
);

CREATE TABLE customers_shipping_addresses(
    id INT NOT NULL AUTO_INCREMENT,
    shipping_address_id INT NOT NULL,
    customer_id INT NOT NULL,
    address_book VARCHAR(16) DEFAULT 'address_0',
    PRIMARY KEY (id),
    UNIQUE KEY unique_together (shipping_address_id, customer_id, address_book)
);

CREATE TABLE orders(
    id_wp INT NOT NULL,
    id_sam_erp VARCHAR(32),
    currency VARCHAR(3),
    date_created VARCHAR(32),
    discount_total FLOAT DEFAULT 0,
    discount_tax FLOAT DEFAULT 0,
    shipping_total FLOAT DEFAULT 0,
    shipping_tax FLOAT DEFAULT 0,
    cart_tax FLOAT DEFAULT 0,
    total FLOAT DEFAULT 0,
    total_tax FLOAT DEFAULT 0,
    customer_id INT NOT NULL,
    shipping_address_id INT NOT NULL,
    customer_note TEXT,
    shipping_first_name VARCHAR(128),
    shipping_last_name VARCHAR(128),
    shipping_company VARCHAR(256),
    shipping_address_1 VARCHAR(256),
    shipping_address_2 VARCHAR(256),
    shipping_city VARCHAR(64),
    shipping_state VARCHAR(64),
    shipping_postcode VARCHAR(16),
    shipping_country VARCHAR(64),
    PRIMARY KEY (id_wp)
);

CREATE TABLE order_products(
    id INT NOT NULL AUTO_INCREMENT,
    order_id_wp INT NOT NULL,
    sku VARCHAR(32) NOT NULL,
    quantity INT NOT NULL,
    subtotal FLOAT DEFAULT 0,
    subtotal_tax FLOAT DEFAULT 0,
    total FLOAT DEFAULT 0,
    total_tax FLOAT DEFAULT 0,
    price FLOAT DEFAULT 0,
    uploaded_image VARCHAR(256),
    preview_image VARCHAR(256),
    cliche_position VARCHAR(8),
    PRIMARY KEY (id),
    UNIQUE KEY unique_together (order_id_wp, sku)
);