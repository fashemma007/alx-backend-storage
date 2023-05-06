-- This SQL script select band_name, and lifespan column which is difference
-- select the band name
SELECT band_name,
    -- check if split value is NULL and use this year
    (IFNULL(split, YEAR(NOW())) - formed) AS lifespan
FROM metal_bands -- WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
WHERE style LIKE '%Glam rock%' -- all bands whoo have Glam rock style
ORDER BY lifespan DESC;
-- sort in descending order