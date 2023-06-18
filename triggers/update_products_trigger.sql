DELIMITER $$
CREATE TRIGGER `update_products_trigger` BEFORE UPDATE ON `products` FOR EACH ROW
BEGIN 
    IF NEW.id_sam_erp <> OLD.id_sam_erp OR 
       NEW.id_wp <> OLD.id_wp OR 
       NEW.id_wp_en <> OLD.id_wp_en OR 
       NEW.title_it <> OLD.title_it OR 
       NEW.title_en <> OLD.title_en OR 
       NEW.category <> OLD.category OR 
       NEW.tags <> OLD.tags OR 
       NEW.product_brand_id <> OLD.product_brand_id OR 
       NEW.meta_description_it <> OLD.meta_description_it OR 
       NEW.meta_description_en <> OLD.meta_description_en OR 
       NEW.cover_image <> OLD.cover_image OR 
       NEW.gallery <> OLD.gallery OR 
       NEW.description_it <> OLD.description_it OR 
       NEW.description_en <> OLD.description_en OR 
       NEW.short_description_it <> OLD.short_description_it OR 
       NEW.short_description_en <> OLD.short_description_en THEN 
        SET NEW.in_sync = 0;
    END IF;
END$$

DELIMITER ;