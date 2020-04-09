delete from stocks_list;
INSERT INTO stocks_list
    (stock_name, stock_symbol)
VALUES
    ('Merck', 'MRK'),
    ('Amazon', 'AMZN'),
    ('BMW', 'BMW.DE'),
    ('Boeing', 'BA'),
    ('NVIDIA', 'NVDA'),
    ('Veolia', 'VIE.PA'),
    ('Avast', 'AVST.PR'),
    ('Qualcomm', 'QCOM'),
    ('Microsoft', 'MSFT'),
    ('Intel', 'INTC'),
    ('KB', 'KOMB.PR'),
    ('Total SA', 'TOT'),
    ('Alibaba', 'BABA'),
    ('Amgen', 'AMGN'),
    ('Blizzard', 'ATVI'),
    ('Moneta', 'MONET.PR'),
    ('Apache', 'APA'),
    ('Walt', 'DIS'),
    ('Agree', 'ADC');

delete from stocks_volume;
INSERT INTO stocks_volume (stock_name, cur_volume)
VALUES
    ('Merck', 11),
    ('Amazon', 0),
    ('BMW', 16),
    ('Boeing', 10),
    ('Microsoft', 15),
    ('NVIDIA', 4),
    ('Veolia', 80),
    ('Avast', 1000),
    ('Qualcomm', 20),
    ('Intel', 0),
    ('KB', 50),
    ('Total SA', 23),
    ('Alibaba', 0),
    ('Amgen', 0),
    ('Blizzard', 0),
    ('Moneta', 0),
    ('Apache', 100),
    ('Walt', 10),
    ('Agree', 13);

delete from exposures;
INSERT INTO exposures (cur_date, exposure)
VALUES
    ('2018-05-09', 30000),
    ('2018-10-18', 30000),
    ('2018-09-11', 15000),
    ('2019-01-09', 15000),
    ('2019-02-08', 15000),
    ('2019-03-08', 15000),
    ('2019-03-11', 34000),
    ('2019-04-09', 15000),
    ('2019-05-09', 30000),
    ('2019-05-22', 20000),
    ('2019-06-07', 15000),
    ('2019-06-27', 5000),
    ('2019-07-09', 15000),
    ('2019-08-09', 15000),
    ('2019-08-29', -25000),
    ('2019-08-30', 200000),
    ('2019-11-28', -25000),
    ('2020-03-02', -100000)
    ('2020-04-08', 140000);

