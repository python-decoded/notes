-- Задача 1.
-- Покупці із США та Канади, у яких у профілі вказана назва компанії.
--
-- Простий СЕЛЕКТ та пара фільтрів.























SELECT "FirstName", "LastName", "Company", "Email"
FROM public."Customer"
WHERE "Country" IN ('USA', 'Canada')
AND "Company" IS NOT NULL;




-- Задача 2.
-- Дізнатись загальну кількість треків, 
-- та cередню тривалість у хвилинах, закруглену до 1 символа після коми.
--
-- Використання агрегаційних функцій COUNT, AVG,
-- використання математичних операцій - ділення, заокруглення.деяких функцій.




















SELECT
  COUNT(*) AS "TotalTrackCount",
  ROUND(AVG("Milliseconds") / 1000 / 60, 1) AS "AvgMinutes"
FROM public."Track";







-- Задача 3.
-- Отримати 5 інвойсів у США за 2012 рік з найбільшою сумою.
--
-- Сортування та ліміт, робота з датою та часом.




















SELECT
    "CustomerId", "InvoiceDate", "Total"
FROM public."Invoice"
WHERE "BillingCountry" = 'USA'
AND DATE_PART('year', "InvoiceDate") = 2012
ORDER BY "Total" DESC LIMIT 5;







-- Задача 4.
-- Отримати 5 інвойсів у США за 2012 рік з найбільшою сумою.
-- Додати інформацію про покупця.
--
-- Left Join.



















SELECT
    customer."FirstName",  customer."LastName",  customer."Email",
    invoice."CustomerId", invoice."InvoiceDate", invoice."Total"
FROM public."Invoice" invoice
LEFT JOIN public."Customer" customer ON invoice."CustomerId" = customer."CustomerId"
WHERE "BillingCountry" = 'USA'
AND DATE_PART('year', "InvoiceDate") = 2012
ORDER BY "Total" DESC LIMIT 5;






-- Задача 5.
-- Дізнатись який покупець витратив найбільшу суму грошей.
-- Вивести id, ім'я, фамілію, суму, середню суму, кількість інвойсів,
-- Суму та середню суму закруглити до сотих і форматувати.
--
-- GROUP BY, ORDER BY, Limit
-- Використання функцій CONCAT, SUM, AVG, ROUND




















SELECT
	customer."CustomerId", customer."FirstName", customer."LastName",
	CONCAT(SUM(invoice."Total"), ' $') AS "TotalPurchased",
	CONCAT(ROUND(AVG(invoice."Total"), 2), ' $') AS "AvgPurchase",
	COUNT(*) AS "InvoceCount"
FROM public."Customer" customer
LEFT JOIN public."Invoice" invoice ON invoice."CustomerId" = customer."CustomerId"
GROUP BY customer."CustomerId", customer."FirstName", customer."LastName"
ORDER BY SUM(invoice."Total") DESC
LIMIT 1;








-- Задача 6.
-- Кількість покупців по рокам, які зробили в такому році більше 1 покупки.
--
-- Групування згрупованих значеннь - розрахунок у 2 етапи задопомогою Sub Query або WITH Block
-- 1. Групування за Id Користувача і Роком - GROUP BY Having, Sub Query or WITH Block.
-- 2. Групування за Роком - ще один GROUP BY та Сортування.




















WITH usersInvoicesPerYear AS (
	SELECT
	invoice."CustomerId",
	DATE_PART('year', "InvoiceDate") AS "Year",
	COUNT(*) AS "InvoicesCOUNT"
	FROM public."Invoice" invoice
	GROUP BY invoice."CustomerId", DATE_PART('year', "InvoiceDate") HAVING COUNT(*) > 1
)
SELECT
	usersInvoicesPerYear."Year",
	COUNT(*) AS "CustomersCount"
FROM usersInvoicesPerYear
GROUP BY usersInvoicesPerYear."Year"
ORDER BY usersInvoicesPerYear."Year";









-- Задача 7.
-- Дізнатись найменш популярний жанр.
-- Розрахувати відсоток пісень для кожного жанру, які жодного разу не були продані за увесь час.
-- Відсортувати усі жанри за таким відсотком, від найбільшого до найменшого.
--
-- 1. Спосіб:
-- left join, WITH block, GROUP BY, convert to float, case when then




















WITH sold_not_sold AS (
	SELECT DISTINCT
     genre."Name",
     COUNT(track."TrackId") AS "TotalCOUNT",
     SUM(CASE WHEN invoice_line."TrackId" IS NULL
		THEN 1
		ELSE 0
		END) AS "TotalUnsoldCOUNT"
	FROM public."Track" track
	LEFT JOIN public."InvoiceLine" invoice_line ON track."TrackId" = invoice_line."TrackId"
	LEFT JOIN public."Genre" genre ON track."GenreId" = genre."GenreId"
	GROUP BY genre."Name"
)
SELECT
	*,
	("TotalUnsoldCOUNT"::FLOAT / "TotalCOUNT"::FLOAT) * 100 AS "UnsoldPercent"
FROM sold_not_sold
ORDER BY "TotalUnsoldCOUNT"::FLOAT / "TotalCOUNT"::FLOAT DESC;




-- 2. Спосіб:
-- left join, WITH block, window function, SELECT distinct, convert to float, case when then






















WITH sold_not_sold AS (
	SELECT DISTINCT
		 genre."Name",
		 COUNT(track."TrackId") OVER (PARTITION BY genre."Name") AS "TotalCOUNT",
		 SUM(CASE WHEN invoice_line."TrackId" IS NULL
			THEN 1
			ELSE 0
			END) OVER (PARTITION BY genre."Name") AS "TotalUnsoldCOUNT"
	FROM public."Track" track
	LEFT JOIN public."InvoiceLine" invoice_line ON track."TrackId" = invoice_line."TrackId"
	LEFT JOIN public."Genre" genre ON track."GenreId" = genre."GenreId"
)
select
	*,
	("TotalUnsoldCOUNT"::FLOAT / "TotalCOUNT"::FLOAT) * 100 AS "UnsoldPercent"
FROM sold_not_sold
ORDER BY "TotalUnsoldCOUNT"::FLOAT / "TotalCOUNT"::FLOAT DESC;










-- Задача 8.
-- скільки треків AC/DC купували кожного року.
--
-- Ланцюжок джойнів. Групування






















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
GROUP BY artist."Name", DATE_PART('year',invoice."InvoiceDate");










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









-- Задача 10.
-- Який спад у кількості проданих одиниць був для треків усіх виконавців від року до року.
-- Знайти виконавця і рік із найбільшим спадом та зростом продажів.
--
-- Декілька WITH блоків, partition by, Union, ORDER BY Nulls Last
























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
	select
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
