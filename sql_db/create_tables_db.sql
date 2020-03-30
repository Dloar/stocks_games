--------------------------------------------------------
-- Purpose of this is script is to create a database. --
--                                                    --
--------------------------------------------------------

DROP TABLE stocks_list;

CREATE TABLE stocks_list (
    stock_id numeric(3,0),
    stock_name varchar(255),
    stock_symbol varchar(32)
);

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

DROP TABLE exposures;

CREATE TABLE exposures (
    cur_date DATE,
    exposure numeric(13,0)
);

DROP TABLE purchases;

CREATE TABLE purchases (
    cur_date DATE,
    stock_id numeric(3,0),
    buy_price numeric(13,0),
    buy_amount numeric(13,0)
);

DROP TABLE sells;

CREATE TABLE sells (
    cur_date DATE,
    stock_id numeric(3,0),
    sell_price numeric(13,0),
    sell_amount numeric(13,0)
);

