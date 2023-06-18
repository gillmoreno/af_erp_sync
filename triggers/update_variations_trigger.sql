DELIMITER $$
CREATE TRIGGER `update_variations_trigger` BEFORE UPDATE ON `variations` FOR EACH ROW
BEGIN 
    IF NEW.id_parent_sam_erp <> OLD.id_parent_sam_erp OR 
       NEW.id_wp <> OLD.id_wp OR 
       NEW.id_wp_en <> OLD.id_wp_en OR 
       NEW.description_it <> OLD.description_it OR 
       NEW.description_en <> OLD.description_en OR 
       NEW.configurator_en <> OLD.configurator_en OR 
       NEW.configurator_en <> OLD.configurator_en OR 
       NEW.configurator_page_it <> OLD.configurator_page_it OR 
       NEW.configurator_page_it <> OLD.configurator_page_it OR 
       NEW.quantity_min <> OLD.quantity_min OR 
       NEW.stock <> OLD.stock OR 
       NEW.sale_price <> OLD.sale_price OR 
       NEW.image_ <> OLD.image_ OR 
       NEW.variation_colors_id <> OLD.variation_colors_id OR 
       NEW.variation_dimensions_id <> OLD.variation_dimensions_id OR 
       NEW.length_ <> OLD.length_ OR 
       NEW.width <> OLD.width OR 
       NEW.height <> OLD.height OR 
       NEW.is_active <> OLD.is_active THEN
        SET NEW.in_sync = 0;
    END IF;
END$$
DELIMITER ;
