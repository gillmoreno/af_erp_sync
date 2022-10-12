# WooCommerce and ERP sync API

## DB Frontiera structure

The file db_frontiera.sql defines the tables that are meant to exchange information between SAM ERP and Woocommerce.

While inside SAM ERP the products are contained in a single table, in Woocommerce two tables are needed: one for the generic product and one for the specific product variation (the thing that is actually being sold).

A new table for the "generic" or "parent" product should be created inside SAM ERP.

### The table products

| Field                 | Type           | Null  | Key   | Default   | Extra   |
| --------------------- | -------------- | ----- | ----- | --------- | ------- |
| id_wp                 | int            | NO    |       | NULL      |         |
| id_wp_en              | int            | YES   |       | NULL      |         |
| in_sync               | tinyint(1)     | YES   |       | NULL      |         |
| id_sam_erp            | varchar(32)    | NO    | PRI   |           |         |
| title_it              | varchar(64)    | NO    |       | NULL      |         |
| title_en              | varchar(64)    | NO    |       | NULL      |         |
| category              | varchar(64)    | NO    |       | NULL      |         |
| tags                  | varchar(64)    | YES   |       | NULL      |         |
| meta_description_it   | varchar(256)   | NO    |       | NULL      |         |
| meta_description_en   | varchar(256)   | NO    |       | NULL      |         |
| cover_image           | varchar(256)   | NO    |       | NULL      |         |
| gallery               | varchar(2056)  | YES   |       | NULL      |         |
| description_it        | text           | NO    |       | NULL      |         |
| description_en        | text           | NO    |       | NULL      |         |
| short_description_it  | text           | NO    |       | NULL      |         |
| short_description_en  | text           | NO    |       | NULL      |         |
| dimensions_options    | varchar(512)   | NO    |       |           |         |
| colors_options_it     | varchar(512)   | NO    |       | NULL      |         |
| colors_options_en     | varchar(512)   | NO    |       | NULL      |         |

### The table variations

| Field                 | Type          | Null  | Key   | Default  | Extra   |
| --------------------- | ------------- | ----- | ----- | -------- | ------- |
| id_wp                 | int           | NO    |       | NULL     |         |
| id_wp_en              | int           | YES   |       | NULL     |         |
| in_sync               | tinyint(1)    | YES   |       | NULL     |         |
| id_parent_sam_erp     | varchar(32)   | NO    |       |          |         |
| is_active             | tinyint(1)    | NO    |       | 1        |         |
| sku                   | varchar(32)   | NO    | PRI   | NULL     |         |
| description_it        | text          | NO    |       | NULL     |         |
| description_en        | text          | NO    |       | NULL     |         |
| quantity_minimum      | int           | YES   |       | NULL     |         |
| quantity_multiplier   | int           | YES   |       | NULL     |         |
| stock                 | floa          | NO    |       | NULL     |         |
| price                 | floa          | NO    |       | NULL     |         |
| image_                | varchar(256)  | YES   |       | NULL     |         |
| length_               | smallint      | YES   |       | NULL     |         |
| width                 | smallint      | YES   |       | NULL     |         |
| height                | smallint      | YES   |       | NULL     |         |
| color_it              | varchar(64)   | YES   |       | NULL     |         |
| color_en              | varchar(64)   | YES   |       | NULL     |         |
| dimensions            | varchar(64)   | YES   |       | NULL     |         |
| configurator_it       | int           | YES   |       | NULL     |         |
| configurator_en       | int           | YES   |       | NULL     |         |
| configurator_page_it  | int           | YES   |       | NULL     |         |
| configurator_page_en  | int           | YES   |       | NULL     |         |

## The APIS

Inside the apis folder, there are the scripts that will be called when:

- Loading the initial content (the very first import from SAM EPR to WooCommerce) [1 time only]
- Sincronizing products (generic or variation) [Cronjob twice a day]
- Sincronizing customers [Cronjob twice a day]
- Sincronizing orders [Cronjob twice an hour]

## Considerazioni per dopo

- Cosa sucede quando si deve creare una nuova varizione (con attributi nuovi)?
  - La gestione degli atributi dovrebbe fatta da una tabella aparte, con attributi standard
  - Il problema è che le traduzioni sono "difficili" da sincronizzare
