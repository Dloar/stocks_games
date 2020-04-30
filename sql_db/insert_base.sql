delete from stocks_list;
INSERT INTO stocks_list
    (stock_name, stock_symbol, currency, market)
VALUES
    ('Merck', 'MRK', 'USD', 'NYQ'),
    ('Amazon com Inc', 'AMZN', 'USD', 'NSQ'),
    ('BMW', 'BMW.DE', 'EUR', 'GER'),
    ('Boeing', 'BA', 'USD', 'NYQ'),
    ('NVIDIA', 'NVDA', 'USD', 'NSQ'),
    ('Veolia Environ', 'VIE,PA', 'EUR', 'PAR'),
    ('Avast', 'AVST.PR', 'CZK', 'PRA'),
    ('Qualcomm', 'QCOM', 'USD', 'NSQ'),
    ('Microsoft', 'MSFT', 'USD', 'NSQ'),
    ('Intel', 'INTC', 'USD', 'NSQ'),
    ('KOMERCNI BANKA', 'KOMB.PR', 'CZK', 'PRA'),
    ('Total SA', 'TOT', 'EUR', 'PAR'),
    ('Alibaba', 'BABA', 'USD', 'NYQ'),
    ('Amgen Inc', 'AMGN', 'USD', 'NSQ'),
    ('Activision Inc', 'ATVI', 'USD', 'NSQ'),
    ('MONETA MONEY BANK', 'MONET,PR', 'CZK', 'PRA'),
    ('Apache Corp', 'APA', 'USD', 'NYQ'),
    ('Walt Disney Co', 'DIS', 'USD', 'NYQ'),
    ('Agree Realty', 'ADC', 'USD', 'NYQ'),
    ('Grupa Lotos', 'LTS', 'PLN', 'WSE'),
    ('WISDOMTREE WTI CRUDE OIL', 'CRUD.L', 'USD', 'LSE');

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
    ('Total', 23),
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
    ('2020-03-02', -100000),
    ('2020-04-08', 140000);

delete from stocks_purchases;
INSERT INTO stocks_purchases (provider, stock_name, market, volume, currency, purchase_date, price, fee)
VALUES
    ('patria', 'WISDOMTREE WTI CRUDE OIL', 'LSE', 160, 'USD', '20.04.2020', 2.8550, 18.35),
    ('patria', 'Apache Corp', 'NYQ', 40, 'USD', '09.04.2020', 8.7000, 14.9),
    ('patria', 'Apache Corp', 'NYQ', 60, 'USD', '09.04.2020', 9.7799, 14.9),
    ('patria', 'Walt Disney Co', 'NYQ', 10, 'USD', '09.04.2020', 105.2600, 14.9),
    ('patria', 'Agree Realty', 'NYQ', 13, 'USD', '09.04.2020', 68.4000, 14.9),
    ('patria', 'Wizz Air', 'LSE', 30, 'GBP', '09.04.2020', 28.5200, 14.86),
    ('patria', 'Veolia Environ', 'PAR', 30, 'EUR', '08.04.2020', 18.5050, 16.9),
    ('patria', 'Microsoft', 'NSQ', 15, 'USD', '06.04.2020', 161.5900, 14.9),
    ('patria', 'Qualcomm Inc', 'NSQ', 20, 'USD', '01.04.2020', 67.1400, 14.9),
    ('patria', 'Boeing', 'NYQ', 10, 'USD', '01.04.2020', 138.9200, 14.9),
    ('patria', 'NVIDIA', 'NSQ', 4, 'USD', '01.04.2020', 255.9700, 14.9),
    ('patria', 'BMW', 'GER', 16, 'EUR', '01.04.2020', 44.7900, 16.9),
    ('patria', 'Total SA', 'PAR', 10, 'EUR', '01.04.2020', 33.6650, 16.9),
    ('patria', 'KOMERCNI BANKA', 'PRA', 25, 'CZK', '01.04.2020', 468.0000, 80),
    ('patria', 'Grupa Lotos', 'WSE', 30, 'PLN', '27.03.2020', 53.1000, 60),
    ('patria', 'NVIDIA', 'NSQ', 5, 'USD', '23.03.2020', 209.3900, 14.9),
    ('patria', 'Intel', 'NSQ', 30, 'USD', '23.03.2020', 48.2400, 14.9),
    ('patria', 'AVAST', 'PRA', 295, 'CZK', '31.01.2020', 126.0000, 167.27),
    ('patria', 'Merck', 'NYQ', 11, 'USD', '09.01.2020', 88.9400, 14.9),
    ('patria', 'AVAST', 'PRA', 1600, 'CZK', '10.09.2019', 107.0000, 713.6),
    ('patria', 'Activision Inc', 'NSQ', 24, 'USD', '27.06.2019', 47.0900, 14.9),
    ('patria', 'Intel', 'NSQ', 35, 'USD', '19.06.2019', 47.3700, 14.9),
    ('patria', 'Arotech Corp.', 'NSQ', 300, 'USD', '19.06.2019', 2.0400, 14.9),
    ('patria', 'Total SA', 'PAR', 13, 'EUR', '11.04.2019', 50.1700, 16.9),
    ('patria', 'Amazon com Inc', 'NSQ', 1, 'USD', '18.03.2019', 1736.4000, 14.9),
    ('patria', 'Amgen Inc', 'NSQ', 6, 'USD', '25.02.2019', 188.1700, 14.9),
    ('patria', 'Veolia Environ', 'PAR', 50, 'EUR', '25.02.2019', 19.7350, 16.9),
    ('patria', 'Alibaba Group', 'NYQ', 8, 'USD', '18.10.2018', 146.1500, 14.9),
    ('patria', 'AVAST', 'PRA', 105, 'CZK', '26.09.2018', 85.0000, 80),
    ('patria', 'KOMERCNI BANKA', 'PRA', 25, 'CZK', '15.05.2018', 899.0000, 101.14),
    ('patria', 'CETV', 'PRA', 35, 'CZK', '07.02.2018', 95.7000, 80),
    ('patria', 'STOCK', 'PRA', 200, 'CZK', '07.02.2018', 82.6000, 80),
    ('patria', 'STOCK', 'PRA', 50, 'CZK', '23.01.2018', 89.6000, 80),
    ('patria', 'Grupa Lotos', 'WSE', 17, 'PLN', '23.01.2018', 61.8200, 60),
    ('patria', 'MONETA MONEY BANK', 'PRA', 100, 'CZK', '23.01.2018', 85.1500, 80),
    ('patria', 'STOCK', 'PRA', 65, 'CZK', '09.01.2018', 77.5000, 80),
    ('patria', 'CETV', 'PRA', 150, 'CZK', '09.01.2018', 99.5000, 80),
    ('patria', 'CETV', 'PRA', 200, 'CZK', '04.01.2018', 100.4000, 90.36);

delete from stocks_sells;
INSERT INTO stocks_sells (provider, stock_name, market, volume, currency, purchase_date, price, fee)
VALUES
    ('patria', 'CETV', 'PRA', 15, 'CZK', '31.03.2020', 79.0000, 80),
    ('patria', 'Intel', 'NSQ', 30, 'USD', '25.03.2020', 51.3000, 14.9),
    ('patria', 'NVIDIA', 'NSQ', 5, 'USD', '25.03.2020', 255.0100, 14.9),
    ('patria', 'AVAST', 'PRA', 1000, 'CZK', '25.03.2020', 115.0000, 545),
    ('patria', 'Amazon com Inc', 'NSQ', 1, 'USD', '19.03.2020', 1900.2000, 14.9),
    ('patria', 'Alibaba Group', 'NYQ', 8, 'USD', '10.03.2020', 201.6900, 14.9),
    ('patria', 'Intel', 'NSQ', 35, 'USD', '31.01.2020', 64.7900, 14.9),
    ('patria', 'Amgen Inc', 'NSQ', 6, 'USD', '31.01.2020', 212.2100, 14.9),
    ('patria', 'Activision Inc', 'NSQ', 24, 'USD', '31.01.2020', 59.0100, 14.9),
    ('patria', 'MONETA MONEY BANK', 'PRA', 100, 'CZK', '10.01.2020', 83.9000, 80),
    ('patria', 'STOCK', 'PRA', 315, 'CZK', '10.01.2020', 63.6000, 90.15),
    ('patria', 'CETV', 'PRA', 120, 'CZK', '03.12.2018', 76.2000, 80),
    ('patria', 'CETV', 'PRA', 300, 'CZK', '22.03.2018', 87.6000, 98.55);







