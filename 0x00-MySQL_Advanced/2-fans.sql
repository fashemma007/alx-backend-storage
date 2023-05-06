-- This SQL script select origin column, and sum of fans column as nb_fans.
SELECT origin,
    -- create temp column using alias
    SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin -- group by the origins
ORDER BY nb_fans DESC;
-- sort in descending order