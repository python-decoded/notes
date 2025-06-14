-- Задача 8.
-- Дізнатись найменш популярний жанр.
-- Розрахувати відсоток пісень для кожного жанру, які жодного разу не були продані за увесь час.
-- Відсортувати усі жанри за таким відсотком, від найбільшого до найменшого.
--
-- 1. Спосіб:
-- left join, WITH block, GROUP BY, convert to float, case when then




















WITH sold_not_sold AS (
	SELECT
     genre."Name",
     COUNT(track."TrackId") AS "TotalCount",
     SUM(CASE WHEN invoice_line."TrackId" IS NULL
		THEN 1
		ELSE 0
		END) AS "TotalUnsoldCount"
	FROM public."Track" track
	LEFT JOIN public."InvoiceLine" invoice_line ON track."TrackId" = invoice_line."TrackId"
	LEFT JOIN public."Genre" genre ON track."GenreId" = genre."GenreId"
	GROUP BY genre."Name"
)
SELECT
	*,
	("TotalUnsoldCount"::FLOAT / "TotalCount"::FLOAT) * 100 AS "UnsoldPercent"
FROM sold_not_sold
ORDER BY "TotalUnsoldCount"::FLOAT / "TotalCount"::FLOAT DESC;






-- 2. Спосіб:
-- left join, WITH block, window function, SELECT distinct, convert to float, case when then






















WITH sold_not_sold AS (
	SELECT DISTINCT
		 genre."Name",
		 COUNT(track."TrackId") OVER (PARTITION BY genre."Name") AS "TotalCount",
		 SUM(CASE WHEN invoice_line."TrackId" IS NULL
			THEN 1
			ELSE 0
			END) OVER (PARTITION BY genre."Name") AS "TotalUnsoldCount"
	FROM public."Track" track
	LEFT JOIN public."InvoiceLine" invoice_line ON track."TrackId" = invoice_line."TrackId"
	LEFT JOIN public."Genre" genre ON track."GenreId" = genre."GenreId"
)
select
	*,
	("TotalUnsoldCount"::FLOAT / "TotalCount"::FLOAT) * 100 AS "UnsoldPercent"
FROM sold_not_sold
ORDER BY "TotalUnsoldCount"::FLOAT / "TotalCount"::FLOAT DESC;
