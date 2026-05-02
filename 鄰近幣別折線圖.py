import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# 建立資料庫連接
conn = sqlite3.connect("台灣匯率.db")
sql = "Select * from 匯率"
# 讀取資料庫中的匯率資料
df = pd.read_sql(sql, conn)
# 顯示幣別名稱的唯一值，讓使用者選擇指定幣別
print(df["幣別名稱"].unique())
# 讓使用者輸入指定幣別，並去除前後空白
jessica = input("請輸入指定幣別： ").strip()
# 先列出所有幣別的現金買入平均值，並排序
s1 = df.groupby("幣別名稱")["現金買入"].mean().sort_values()
print(s1)
# 篩選出現金買入平均值在指定幣別的80%到120%之間的幣別，作為鄰近幣別
s2 = s1[s1.between(s1[jessica] * 0.8, s1[jessica] * 1.2)]
# 繪製圖紙大小和解析度，並設定字體為微軟正黑體
plt.figure(figsize=(16, 10), dpi=120)
plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
# 繪製指定幣別的現金買入匯率走勢圖
for i in s2.index:
    df1 = df[df["幣別名稱"] == i].sort_values("日期")
    plt.plot(df1["日期"], df1["現金買入"], label=i)
# 設定x軸標籤、y軸標籤、圖表標題、x軸刻度、圖例和網格
plt.xlabel("日期", fontsize=16)
plt.ylabel("現\n金\n買\n入", fontsize=16, rotation=0, labelpad=10)
plt.title(f"{jessica} 現金買入匯率及鄰近幣別走勢圖", fontsize=24)
plt.xticks(np.linspace(0, len(df1) - 1, 12))
plt.legend()
plt.grid()
plt.tight_layout()
# 儲存圖表為PNG檔案，檔名包含指定幣別名稱
plt.savefig(f"{jessica} 現金買入匯率及鄰近幣別走勢圖.png")
plt.show()
