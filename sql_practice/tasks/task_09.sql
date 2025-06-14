-- Задача 9.
-- Який спад продажів був для треків AC/DC від року до року.
--
-- 1. Спосіб: Доступ до попереднього рядка задопомогою Window функції LAG.


























WITH yearSales AS (
	SELECT
		artist."Name",
		DATE_PART('year',invoice."InvoiceDate") AS "Year",
		SUM(invoiceLine."Quantity") AS "TotalSold"
	FROM public."InvoiceLine" invoiceLine
	INNER JOIN public."Invoice" invoice ON invoiceLine."InvoiceId" = invoice."InvoiceId"
	INNER JOIN public."Track" track ON invoiceLine."TrackId" = track."TrackId"
	INNER JOIN public."Album" album ON track."AlbumId" = album."AlbumId"
	INNER JOIN public."Artist" artist ON album."ArtistId" = artist."ArtistId"
	WHERE artist."Name" = 'AC/DC'
	GROUP BY artist."Name", DATE_PART('year', invoice."InvoiceDate")
)
select
  "Name",
  LAG("TotalSold", 1) OVER (ORDER BY "Year") AS "PrevTotalSold",
  "TotalSold",
  LAG("Year", 1) OVER (ORDER BY "Year") AS "PrevYear",
  "Year",
  ("TotalSold"::FLOAT / (LAG("TotalSold", 1) OVER (ORDER BY "Year"))::FLOAT) * 100 - 100 AS "SalesGrowth"
FROM yearSales;







-- 2. Спосіб: Виконання Селф Джойну де Year = Year - 1.

























WITH yearSales AS (
	SELECT
		artist."Name",
		DATE_PART('year',invoice."InvoiceDate") AS "Year",
		SUM(invoiceLine."Quantity") AS "TotalSold"
	FROM public."InvoiceLine" invoiceLine
	INNER JOIN public."Invoice" invoice ON invoiceLine."InvoiceId" = invoice."InvoiceId"
	INNER JOIN public."Track" track ON invoiceLine."TrackId" = track."TrackId"
	INNER JOIN public."Album" album ON track."AlbumId" = album."AlbumId"
	INNER JOIN public."Artist" artist ON album."ArtistId" = artist."ArtistId"
	WHERE artist."Name" = 'AC/DC'
	GROUP BY artist."Name", DATE_PART('year', invoice."InvoiceDate")
)
SELECT
  _left."Name",
  _right."TotalSold" AS "PrevTotalSold",
  _left."TotalSold",
  _right."Year" AS "PrevYear",
  _left."Year",
  (_left."TotalSold"::FLOAT / _right."TotalSold"::FLOAT) * 100 - 100 AS "SalesGrowth"
FROM yearSales _left
LEFT JOIN yearSales _right
ON _left."Year" = _right."Year" + 1
AND _left."Name" = _right."Name";