DELIMITER $$
CREATE TRIGGER `update_variation_colors_trigger` BEFORE UPDATE ON `variation_colors` FOR EACH ROW
BEGIN 
    IF NEW.id_sam_erp <> OLD.id_sam_erp OR 
       NEW.id_wp <> OLD.id_wp OR 
       NEW.value_it <> OLD.value_it OR
       NEW.value_en <> OLD.value_en THEN
        SET NEW.in_sync = 0;
    END IF;
END$$
DELIMITER ;
