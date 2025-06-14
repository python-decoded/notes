-- Задача 7.
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