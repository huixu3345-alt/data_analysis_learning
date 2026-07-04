from pathlib import Path

import numpy as np
import pandas as pd


# =========================
# 1. 设置路径
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "students_dirty_day2.csv"
OUTPUT_PATH = BASE_DIR / "outputs" / "cleaning_summary_day2.md"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# =========================
# 2. 读取数据
# =========================

df = pd.read_csv(DATA_PATH)

print("========== 原始数据前5行 ==========")
print(df.head())

print("\n========== 数据基本信息 ==========")
print(df.info())

print("\n========== 数值字段统计信息 ==========")
print(df.describe())


# =========================
# 3. 检查重复值
# =========================

print("\n========== 整行重复检查 ==========")

full_duplicate_mask = df.duplicated()
full_duplicate_rows = df[full_duplicate_mask]

print("整行重复数量：", full_duplicate_mask.sum())
print(full_duplicate_rows)


print("\n========== 按 student_id 检查重复 ==========")

id_duplicate_mask = df.duplicated(subset=["student_id"], keep=False)
id_duplicate_rows = df[id_duplicate_mask].sort_values("student_id")

print("student_id 重复记录数量：", id_duplicate_mask.sum())
print(id_duplicate_rows)


# =========================
# 4. 删除重复值
# =========================

# 第一步：删除完全重复的记录
df_no_full_dup = df.drop_duplicates()

# 第二步：按 student_id 保留第一条记录
# 注意：真实业务中不能盲目保留第一条，需要看更新时间、数据来源或业务规则。
df_no_dup = df_no_full_dup.drop_duplicates(subset=["student_id"], keep="first")

print("\n========== 删除重复值后的数据规模 ==========")
print("原始行数：", len(df))
print("删除整行重复后行数：", len(df_no_full_dup))
print("按 student_id 去重后行数：", len(df_no_dup))


# =========================
# 5. 检查异常值
# =========================

score_cols = ["math", "english", "python"]

print("\n========== 用 describe 初步发现异常 ==========")
print(df_no_dup[score_cols].describe())

print("\n========== 用排序查看极端值 ==========")
for col in score_cols:
    print(f"\n{col} 从小到大排序：")
    print(df_no_dup[["student_id", "name", col]].sort_values(col).head(3))

    print(f"\n{col} 从大到小排序：")
    print(df_no_dup[["student_id", "name", col]].sort_values(col, ascending=False).head(3))


# 成绩合理范围：0 到 100
abnormal_score_mask = (df_no_dup[score_cols] < 0) | (df_no_dup[score_cols] > 100)

rows_with_abnormal_score = df_no_dup[abnormal_score_mask.any(axis=1)]

print("\n========== 异常成绩记录 ==========")
print(rows_with_abnormal_score)


# =========================
# 6. 处理异常值
# =========================

df_clean = df_no_dup.copy()

# 先把异常成绩设为 NaN
for col in score_cols:
    invalid_mask = (df_clean[col] < 0) | (df_clean[col] > 100)
    df_clean.loc[invalid_mask, col] = np.nan

print("\n========== 异常值改为缺失值后的缺失数量 ==========")
print(df_clean[score_cols].isnull().sum())

# 再用中位数填充
# 为什么用中位数：相比均值，中位数不容易被极端值影响。
for col in score_cols:
    median_value = df_clean[col].median()
    df_clean[col] = df_clean[col].fillna(median_value)

print("\n========== 异常值处理后的统计信息 ==========")
print(df_clean[score_cols].describe())


# =========================
# 7. 新增指标字段
# =========================

df_clean["total_score"] = df_clean[score_cols].sum(axis=1)
df_clean["avg_score"] = df_clean[score_cols].mean(axis=1).round(2)

print("\n========== 清洗后数据 ==========")
print(df_clean)


# =========================
# 8. 按班级分组统计
# =========================

class_summary = (
    df_clean
    .groupby("class_name")
    .agg(
        student_count=("student_id", "count"),
        avg_math=("math", "mean"),
        avg_english=("english", "mean"),
        avg_python=("python", "mean"),
        avg_score=("avg_score", "mean"),
    )
    .round(2)
    .reset_index()
)

print("\n========== 清洗后班级统计 ==========")
print(class_summary)


# =========================
# 9. 输出数据质量报告
# =========================

summary_text = f"""# 第2周 Day2 数据清洗报告：重复值与异常值处理

## 1. 数据背景

本次练习使用学生成绩数据，模拟真实业务数据中常见的重复记录和异常值问题。

字段包括：

- student_id：学生ID
- name：姓名
- class_name：班级
- gender：性别
- math：数学成绩
- english：英语成绩
- python：Python成绩
- enroll_date：入学日期

## 2. 原始数据规模

- 原始行数：{len(df)}
- 原始列数：{df.shape[1]}

## 3. 重复值检查

### 3.1 整行重复

- 整行重复数量：{full_duplicate_mask.sum()}

整行重复通常说明数据被重复导入，可以优先考虑删除。

### 3.2 student_id 重复

- student_id 重复记录数量：{id_duplicate_mask.sum()}

student_id 是学生唯一标识。若同一个 student_id 出现多次，需要判断是重复录入、数据更新，还是业务上允许多条记录。

本次练习为了形成一人一行的学生成绩表，先删除完全重复记录，再按 student_id 保留第一条记录。

## 4. 异常值检查

本次设定学生成绩的合理范围为 0 到 100。

异常值判断规则：

- 小于 0：异常
- 大于 100：异常

发现的异常记录行数：{len(rows_with_abnormal_score)}

## 5. 异常值处理策略

本次处理方式：

1. 先将异常成绩标记为缺失值 NaN；
2. 再使用该科目的中位数填充；
3. 重新计算 total_score 和 avg_score。

选择中位数的原因：

- 中位数比均值更不容易受到极端异常值影响；
- 适合在练习阶段演示异常值修正逻辑；
- 真实业务中仍需要结合数据来源、录入规则和业务负责人判断。

## 6. 清洗后数据规模

- 删除整行重复后行数：{len(df_no_full_dup)}
- 按 student_id 去重后行数：{len(df_no_dup)}
- 最终清洗后行数：{len(df_clean)}

## 7. 清洗后班级统计

{class_summary.to_markdown(index=False)}

## 8. 今日学习结论

1. 重复值不能直接删除，要先判断是整行重复还是关键字段重复。
2. student_id 这类唯一标识字段非常重要，常用于判断一条业务记录是否重复。
3. 异常值不能只靠肉眼判断，可以结合 describe、sort_values 和条件筛选。
4. 成绩类字段有明确业务范围，低于 0 或高于 100 都应该被标记为异常。
5. 清洗完成后要重新计算 total_score、avg_score 和 groupby 结果。
6. 数据清洗不是单纯改数据，而是要说明判断依据、处理方式和对分析结果的影响。

## 9. 和第1周 pandas 基础的连接

- head：快速查看数据长什么样。
- info：查看字段类型、非空数量和数据规模。
- describe：查看 min、max、均值和分位数，用于发现异常线索。
- sort_values：查看最高值和最低值，定位极端记录。
- 条件筛选：找出异常记录。
- 新增字段：清洗后重新计算 total_score 和 avg_score。
- groupby：按班级汇总，形成可解释的分析结果。

## 10. 业务化理解

在真实业务中，重复值和异常值可能对应：

- 订单重复提交；
- 用户重复注册；
- 商品金额录入错误；
- 活动数据重复统计；
- 渠道归因异常；
- 销售额、GMV、ROI 被异常值扭曲。

所以数据分析师不能只会写代码，还要能解释数据问题对业务指标的影响。
"""

OUTPUT_PATH.write_text(summary_text, encoding="utf-8")

print(f"\n数据质量报告已生成：{OUTPUT_PATH}")