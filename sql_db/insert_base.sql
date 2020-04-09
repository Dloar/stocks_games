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


