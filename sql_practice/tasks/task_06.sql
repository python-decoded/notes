-- Задача 6.
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