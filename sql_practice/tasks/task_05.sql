-- Задача 5.
-- Дізнатись який покупець витратив найбільшу суму грошей.
-- Вивести id, ім'я, фамілію, суму, середню суму, кількість інвойсів,
-- Суму та середню суму закруглити до сотих і форматувати.
--
-- GROUP BY, ORDER BY, Limit
-- Використання функцій CONCAT, SUM, AVG, ROUND, COUNT




















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