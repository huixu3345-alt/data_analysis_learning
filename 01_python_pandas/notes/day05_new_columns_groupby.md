# Day 5 新增列和 groupby 分组统计

## 今天学习内容

今天我学习了如何在 pandas 中新增列，以及如何使用 groupby 做分组统计。

## 我的理解

df["新列名"] = ... 可以给 DataFrame 新增一列。

total_score 是 math_score、english_score、python_score 三门课的总分。

avg_score 是 total_score 除以 3 得到的平均分。

groupby("city") 表示按照 city 这一列分组。

groupby("gender") 表示按照 gender 这一列分组。

mean() 表示计算平均值。

count() 表示计数。

agg() 可以一次性计算多个统计指标。

## 今日练习

1. 新增 total_score 列。
2. 新增 avg_score 列。
3. 按 city 统计 avg_score 平均值。
4. 按 gender 统计 avg_score 平均值。
5. 按 city 统计学生人数。
6. 按 gender 统计 python_score 平均值。
7. 使用 agg() 按城市统计人数、平均分、最高分、最低分。

## 今日结论

在这份学生成绩数据中，Osaka 和 Tokyo 的 avg_score 平均值相同，都是 87.777778。

Nagoya 的 avg_score_min 最低。

女生的 python_score 平均值是 85.25，男生的 python_score 平均值是 83.75。

## 还需要继续熟悉

- groupby 后为什么结果会变成 Series 或 DataFrame
- agg() 中每个统计指标的写法
- count、mean、max、min 的使用场景