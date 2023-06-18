DELIMITER $$
CREATE TRIGGER `update_variation_pricelists_trigger` BEFORE UPDATE ON `variation_pricelists` FOR EACH ROW
BEGIN 
    IF NEW.sku <> OLD.sku OR 
       NEW.quantity <> OLD.quantity OR 
       NEW.unit_price <> OLD.unit_price THEN
        SET NEW.in_sync = 0;
    END IF;
END$$
DELIMITER ;