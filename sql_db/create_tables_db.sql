--------------------------------------------------------
-- Purpose of this is script is to create a database. --
--                                                    --
--------------------------------------------------------

DROP TABLE stocks_list;

CREATE TABLE `stocks_list` (
  `stock_id` MEDIUMINT NOT NULL AUTO_INCREMENT,
  `stock_name` varchar(255) DEFAULT NULL,
  `stock_symbol` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

DROP TABLE stocks_volume;

CREATE TABLE stocks_volume (
    stock_id numeric(3,0),
    cur_volume numeric(13,0)
);

DROP TABLE exposures;

CREATE TABLE exposures (
    cur_date DATE,
    exposure numeric(13,0)
);


DROP TABLE purchases;

CREATE TABLE stocks_purchases (
    cur_date DATE,
    stock_id numeric(3,0),
    buy_price numeric(13,0),
    buy_amount numeric(13,0)
);

DROP TABLE sells;

CREATE TABLE stocks_sells (
    cur_date DATE,
    stock_id numeric(3,0),
    sell_price numeric(13,0),
    sell_amount numeric(13,0)
);

