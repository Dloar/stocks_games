SELECT sp.stock_name, (sp.volume - coalesce(volume_sell, 0)) as curr_volume
FROM (
	SELECT stock_name, sum(volume) as volume 
	FROM stocks_purchases
    GROUP BY stock_name
    ) sp
LEFT JOIN (
	SELECT stock_name, sum(volume) as volume_sell 
	FROM stocks_sells
    GROUP BY stock_name
) as ss
 on sp.stock_name = ss.stock_name