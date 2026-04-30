import time
import schedule
import pandas as pd
from datetime import datetime

# 模拟自动更新经济数据（正式版可对接真实数据源）
def update_economic_data():
    print(f"[{datetime.now()}] 开始自动更新宏观经济数据...")
    
    # 1. 读取现有数据（模拟）
    try:
        df = pd.read_csv("data/economic_data.csv")
        print("数据文件加载成功")
    except FileNotFoundError:
        print("未找到数据文件，创建初始数据...")
        df = pd.DataFrame({
            "date": pd.date_range(start="2023-01-01", periods=12, freq="M"),
            "indicator": ["GDP", "CPI", "PMI"] * 4,
            "value": [5.2, 2.1, 50.8, 5.5, 2.3, 51.2, 5.8, 2.5, 50.9,
                      6.0, 2.2, 51.5]
        })

    # 2. 添加一条最新月份数据
    new_row = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "indicator": "GDP",
        "value": round(5.2 + (datetime.now().month * 0.1), 1)
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # 3. 保存更新后的数据
    df.to_csv("data/economic_data.csv", index=False, encoding="utf-8")
    print(f"[{datetime.now()}] 数据自动更新完成！")

# 每日凌晨2点执行一次自动更新
def start_scheduler():
    schedule.every().day.at("02:00").do(update_economic_data)
    print("自动化调度已启动 → 每天02:00自动更新经济数据")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# 主程序入口
if __name__ == "__main__":
    update_economic_data()  # 启动时先执行一次更新
    start_scheduler()
