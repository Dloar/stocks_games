--------------------------------------------------------
-- Purpose of this is script is to create a database. --
--                                                    --
--------------------------------------------------------
-- Table 1
DROP TABLE stocks_list;

CREATE TABLE stocks_list (
  stock_id MEDIUMINT NOT NULL AUTO_INCREMENT,
  stock_name varchar(255) NOT NULL,
  stock_symbol varchar(32) NOT NULL,
  currency numeric(13,5),
  market varchar(32)
  PRIMARY KEY (`stock_id`)
);

-- Table 2
DROP TABLE stocks_volume;

CREATE TABLE stocks_volume (
    stock_name varchar(255) DEFAULT NULL,
    cur_volume numeric(13,0)
);

-- Table 3
DROP TABLE exposures;

CREATE TABLE exposures (
    cur_date DATE,
    exposure numeric(13,0)
);

-- Table 4
DROP TABLE stocks_purchases;

CREATE TABLE stocks_purchases (
  provider varchar(255) NOT NULL,
  stock_name varchar(255) NOT NULL,
  market varchar(32),
  volume numeric(13,0),
  currency numeric(13,5),
  purchase_date DATE,
  price numeric(13,0),
  fee numeric(6,5)
);

-- Table 5
DROP TABLE stocks_sells;

CREATE TABLE stocks_sells (
  provider varchar(255) NOT NULL,
  stock_name varchar(255) NOT NULL,
  market varchar(32),
  volume numeric(13,0),
  currency numeric(13,5),
  purchase_date DATE,
  price numeric(13,0),
  fee numeric(6,5)
);

