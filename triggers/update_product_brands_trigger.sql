DELIMITER $$
CREATE TRIGGER `update_product_brands_trigger` BEFORE UPDATE ON `product_brands` FOR EACH ROW
BEGIN 
    IF NEW.id_sam_erp <> OLD.id_sam_erp OR 
       NEW.id_wp <> OLD.id_wp OR 
       NEW.value_ <> OLD.value_ THEN
        SET NEW.in_sync = 0;
    END IF;
END$$
DELIMITER ;