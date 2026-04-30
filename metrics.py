import pandas as pd
import numpy as np

def calculate_key_metrics(df):
    """
    自动计算核心宏观经济指标
    包括：同比增速、环比变化、移动平均趋势、风险等级
    """
    # 确保日期列格式正确
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # 按指标分组计算（避免不同指标互相干扰）
    df = df.sort_values(['indicator', 'date'])
    
    # 1. 同比增速 (12个月前对比)
    df['同比增速(%)'] = df.groupby('indicator')['value'].pct_change(12) * 100
    
    # 2. 环比变化 (上月对比)
    df['环比变化'] = df.groupby('indicator')['value'].diff()
    
    # 3. 3个月移动平均 (平滑趋势)
    df['3月均线'] = df.groupby('indicator')['value'].rolling(3).mean().reset_index(0, drop=True)
    
    # 4. 风险状态自动标记
    def label_risk(growth_rate):
        if pd.isna(growth_rate):
            return "待更新"
        elif growth_rate < -1.0:
            return "下行风险"
        elif growth_rate < 1.5:
            return "平稳运行"
        elif growth_rate < 3.0:
            return "温和扩张"
        else:
            return "过热预警"
    
    df['运行状态'] = df['同比增速(%)'].apply(label_risk)
    
    # 保留两位小数，界面更整洁
    df = df.round({'同比增速(%)': 2, '环比变化': 2, '3月均线': 2})
    
    return df

def get_latest_indicators(df):
    """获取每个指标的最新数据卡片"""
    latest = df.sort_values('date').groupby('indicator').tail(1)
    return latest
