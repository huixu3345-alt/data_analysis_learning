import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("Python 环境测试成功！")
print("pandas 版本：", pd.__version__)
print("numpy 版本：", np.__version__)

data = {
    "姓名": ["小明", "小红", "小刚", "小李"],
    "数学": [85, 92, 78, 88],
    "英语": [90, 86, 80, 95],
    "编程": [88, 91, 84, 89]
}

df = pd.DataFrame(data)
df["平均分"] = df[["数学", "英语", "编程"]].mean(axis=1)

print(df)