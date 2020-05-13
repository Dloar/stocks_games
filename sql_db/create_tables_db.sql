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
  currency varchar(32),
  market varchar(32),
  PRIMARY KEY (`stock_id`)
);

-- Table 2
DROP TABLE exposures;

CREATE TABLE exposures (
    cur_date DATE,
    exposure DECIMAL(10,1)
);

-- Table 3
DROP TABLE stocks_purchases;

CREATE TABLE stocks_purchases (
  provider varchar(255) NOT NULL,
  stock_name varchar(255) NOT NULL,
  market varchar(32),
  volume DECIMAL(10,1),
  currency varchar(32),
  purchase_date DATE,
  price DECIMAL(10,5),
  fee DECIMAL(10,5)
);

-- Table 4
DROP TABLE stocks_sells;

CREATE TABLE stocks_sells (
  provider varchar(255) NOT NULL,
  stock_name varchar(255) NOT NULL,
  market varchar(32),
  volume DECIMAL(10,1),
  currency varchar(32),
  purchase_date DATE,
  price DECIMAL(10,5),
  fee DECIMAL(10,5)
);

-- Table 5
DROP TABLE exchange_rates;

CREATE TABLE exchange_rates (
  cur_name varchar(32),
  source_date DATE,
  cur_rate DECIMAL(10,5));
