# Day 3 pandas读取CSV

## 今天学习内容

今天我学习了用 pandas 读取 students.csv，并查看表格的基本信息。

## 我的理解

DataFrame 是 pandas 中的表格数据结构，可以理解成一张表。

df 是一个变量名，里面保存的是读取出来的 DataFrame。

pd.read_csv(csv_path) 可以把 CSV 文件读取成 DataFrame。

df.head() 默认查看前 5 行数据。

df.shape 可以查看数据有几行几列。

df.columns 可以查看所有列名。

df.dtypes 可以查看每一列的数据类型。

df.info() 可以查看行数、列数、缺失值情况和数据类型。

df.describe() 可以查看数值列的统计信息。

## 今日练习结果

students.csv 有 8 行、8 列。

math_score 的平均值是 81.875。

python_score 的最高分是 95。

## 还需要继续熟悉

- DataFrame 和 Series 的区别
- describe() 中 mean、std、min、max 的含义
- 为什么有些列是 str，有些列是 int64