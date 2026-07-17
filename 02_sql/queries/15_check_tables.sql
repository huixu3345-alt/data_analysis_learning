SELECT
    name AS table_name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;