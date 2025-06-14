-- Задача 1.
-- Покупці із США та Канади, у яких у профілі вказана назва компанії.
--
-- Простий СЕЛЕКТ та пара фільтрів.























SELECT "FirstName", "LastName", "Company", "Email"
FROM public."Customer"
WHERE "Country" IN ('USA', 'Canada')
AND "Company" IS NOT NULL;
