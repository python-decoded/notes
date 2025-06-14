-- Задача 10.
-- Який спад у кількості проданих одиниць був для треків усіх виконавців від року до року.
-- Знайти виконавця і рік із найбільшим спадом та зростом продажів.
--
-- Декілька WITH блоків, UNION ALL, ORDER BY NULLS LAST
-- 1. Спосіб: Доступ до попереднього рядка задопомогою Window функції LAG ... ORDER BY ... PARTITION BY























WITH
yearSales AS (
	SELECT
		artist."Name",
		DATE_PART('year',invoice."InvoiceDate") AS "Year",
		SUM(invoiceLine."Quantity") AS "TotalSold"
	FROM public."InvoiceLine" invoiceLine
	INNER JOIN public."Invoice" invoice ON invoiceLine."InvoiceId" = invoice."InvoiceId"
	INNER JOIN public."Track" track ON invoiceLine."TrackId" = track."TrackId"
	INNER JOIN public."Album" album ON track."AlbumId" = album."AlbumId"
	INNER JOIN public."Artist" artist ON album."ArtistId" = artist."ArtistId"
	GROUP BY artist."Name", DATE_PART('year',invoice."InvoiceDate")
),
salesGrowth AS (
	SELECT
      "Name",
	  LAG("TotalSold", 1) OVER (partition BY yearSales."Name" ORDER BY "Year") AS "PrevTotalSold",
	  "TotalSold",
	  LAG("Year", 1) OVER (partition BY yearSales."Name" ORDER BY "Year") AS "PrevYear",
	  "Year",
	  ("TotalSold"::FLOAT / (LAG("TotalSold", 1) OVER (partition BY yearSales."Name" ORDER BY "Year"))::FLOAT) * 100 - 100 AS "SalesGrowth"
	FROM yearSales
)
(SELECT * FROM salesGrowth ORDER BY salesGrowth."SalesGrowth" NULLS LAST LIMIT 1)
  UNION ALL
(SELECT * FROM salesGrowth ORDER BY salesGrowth."SalesGrowth" DESC NULLS LAST LIMIT 1);



-- 2. Спосіб: Виконання Селф Джойну де Year = Year - 1.






















WITH
yearSales AS (
	SELECT
		artist."Name",
		DATE_PART('year',invoice."InvoiceDate") AS "Year",
		SUM(invoiceLine."Quantity") AS "TotalSold"
	FROM public."InvoiceLine" invoiceLine
	INNER JOIN public."Invoice" invoice ON invoiceLine."InvoiceId" = invoice."InvoiceId"
	INNER JOIN public."Track" track ON invoiceLine."TrackId" = track."TrackId"
	INNER JOIN public."Album" album ON track."AlbumId" = album."AlbumId"
	INNER JOIN public."Artist" artist ON album."ArtistId" = artist."ArtistId"
	GROUP BY artist."Name", DATE_PART('year',invoice."InvoiceDate")
),
salesGrowth AS (
    SELECT
      _left."Name",
	  _right."TotalSold" AS "PrevTotalSold",
	  _left."TotalSold",
	  _right."Year" AS "PrevYear",
	  _left."Year",
	  (_left."TotalSold"::FLOAT / _right."TotalSold"::FLOAT) * 100 - 100 AS "SalesGrowth"
	FROM yearSales _left LEFT JOIN yearSales _right
	ON _left."Year" = _right."Year" + 1
    AND _left."Name" = _right."Name"
)
(SELECT * FROM salesGrowth ORDER BY salesGrowth."SalesGrowth" NULLS LAST LIMIT 1)
  UNION ALL
(SELECT * FROM salesGrowth ORDER BY salesGrowth."SalesGrowth" DESC NULLS LAST LIMIT 1);

