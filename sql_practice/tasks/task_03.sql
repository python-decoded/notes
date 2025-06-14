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