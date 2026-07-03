# Day 4 pandas筛选、排序、列选择

## 今天学习内容

今天我学习了 pandas 中的列选择、条件筛选和排序。

## 我的理解

df["name"] 可以选择一列。

df[["name", "python_score"]] 可以选择多列。

df["python_score"] >= 90 会得到一组 True / False。

df[条件] 可以筛选出条件为 True 的行。

多个条件同时成立时，可以使用 &，每个条件需要用括号包起来。

sort_values(by="列名", ascending=False) 可以按照某列从高到低排序。

## 今日练习

1. 筛选 math_score >= 85 的学生。
2. 按 english_score 从高到低排序。
3. 筛选 city 是 Osaka 且 python_score >= 80 的学生。

## 还需要继续熟悉

- 一个中括号和两个中括号的区别
- & 和 | 的区别
- 筛选后索引为什么保留原始编号