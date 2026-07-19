WITH score_demo(name, score) AS (
    VALUES
        ('学生A', 100),
        ('学生B', 90),
        ('学生C', 90),
        ('学生D', 80)
)

SELECT
    name,
    score,

    ROW_NUMBER() OVER (
        ORDER BY score DESC
    ) AS row_number_rank,

    RANK() OVER (
        ORDER BY score DESC
    ) AS rank_result,

    DENSE_RANK() OVER (
        ORDER BY score DESC
    ) AS dense_rank_result

FROM score_demo
ORDER BY score DESC;