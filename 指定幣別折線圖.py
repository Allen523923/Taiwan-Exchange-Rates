import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# 建立資料庫連接
conn = sqlite3.connect("台灣匯率.db")
sql = "Select * from 匯率"
# 讀取資料庫中的匯率資料
df = pd.read_sql(sql, conn)
# 列出所有幣別名稱，讓使用者選擇要繪製哪一個幣別的折線圖
print(df["幣別名稱"].unique())
# 讓使用者輸入指定幣別名稱，並過濾出該幣別的資料，按照日期排序
jessica = input("請輸入指定幣別： ").strip()
df = df[df["幣別名稱"] == jessica].sort_values("日期")
# 繪製指定幣別的現金買入匯率折線圖
plt.figure(figsize=(16, 10), dpi=120)
plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"

plt.plot(df["日期"], df["現金買入"], label=df["幣別名稱"].iloc[0], color="#F30AF5")
# 設定x軸和y軸的標籤、圖表標題、x軸的刻度、圖例和網格
plt.xlabel("日期", fontsize=16)
plt.ylabel("現\n金\n買\n入", fontsize=16, rotation=0, labelpad=10)
plt.title(f"{df['幣別名稱'].iloc[0]} 現金買入匯率走勢圖", fontsize=24)
plt.xticks(np.linspace(0, len(df) - 1, 12))
plt.legend()
plt.grid()

plt.tight_layout()
# 將圖表保存為PNG檔案，檔名包含幣別名稱
plt.savefig(f"{df['幣別名稱'].iloc[0]} 現金買入匯率走勢圖.png")
plt.show()
