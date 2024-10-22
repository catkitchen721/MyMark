"""Symbol: !! Single-side: False"""
from datetime import datetime, timedelta

def countdown(date_string):
    try:
        target_date = datetime.strptime(date_string, "%Y-%m-%d")
        now = datetime.now()
        time_left = target_date - now
        
        if time_left.total_seconds() <= 0:
            return f"日期 {date_string} 已經過去了"
        
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"距離 {date_string} 還有:<br>{days} 天 {hours} 小時 {minutes} 分鐘 {seconds} 秒"
    except ValueError:
        return "日期格式錯誤,請使用 YYYY-MM-DD 格式"
