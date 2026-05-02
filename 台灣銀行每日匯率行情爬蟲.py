import pandas as pd
import sqlite3
from datetime import datetime
from time import sleep
import random

# 建立資料庫連接
conn = sqlite3.connect("台灣匯率.db")

# 取得今天的日期，並生成從2025-01-01到今天的日期列表
today = datetime.now()
allday = pd.date_range("2025-01-01", today)
for d in allday:
    d = str(d)[:10]

    sql = f'Select * from 匯率 where 日期 = "{d}"'
    try:
        df = pd.read_sql(sql, conn)
    except:
        df = pd.DataFrame()
    if len(df) > 0:
        print(f"{d} 已存在資料庫中，跳過抓取。")
        continue
    else:
        # 隨機等待5到10秒，避免過度頻繁的請求
        sleep(random.randint(5, 10))
        # 抓取台灣銀行每日匯率行情報
        url = f"https://rate.bot.com.tw/xrt/all/{d}"

        df = pd.read_html(url)[0]

        if len(df) < 2:
            print(f"{d} 當日沒有營業。")
            continue
        else:
            # 只保留前五欄，並重新命名欄位名稱
            df = df.iloc[:, :5]
            df.columns = ["幣別", "現金買入", "現金賣出", "即期買入", "即期賣出"]

            # 插入日期、幣別名稱、幣別代碼欄位，並將匯率欄位轉換為數字格式
            df.insert(0, "日期", d)
            df.insert(1, "幣別名稱", df["幣別"].str.split().str[0])
            df.insert(2, "幣別代碼", df["幣別"].str.split().str[1].str.strip("()"))
            df.drop("幣別", axis=1, inplace=True)

            for i in df.columns[3:]:
                df[i] = pd.to_numeric(df[i], errors="coerce")

            # 將資料插入資料庫
            df.to_sql("匯率", conn, if_exists="append", index=False)
            print(f"{d} 的匯率資料已成功儲存。")

            # print(df)
