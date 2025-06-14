-- Задача 4.
-- Отримати 5 інвойсів у США за 2012 рік з найбільшою сумою.
-- Додати інформацію про покупця.
--
-- Left Join.



















SELECT
    customer."FirstName",  customer."LastName",  customer."Email",
     invoice."InvoiceDate", invoice."Total"
FROM public."Invoice" invoice
LEFT JOIN public."Customer" customer ON invoice."CustomerId" = customer."CustomerId"
WHERE "BillingCountry" = 'USA'
AND DATE_PART('year', "InvoiceDate") = 2012
ORDER BY "Total" DESC LIMIT 5;