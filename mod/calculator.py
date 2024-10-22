"""Symbol: == Single-side: False"""
import re

def calculator(expression):
    try:
        # 移除所有空白字符
        expression = re.sub(r'\s+', '', expression)
        
        # 使用 eval() 計算結果,但限制可用的操作符
        allowed_chars = set('0123456789+-*/().') 
        if not all(char in allowed_chars for char in expression):
            raise ValueError("不允許的字符")
        
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"計算錯誤: {str(e)}"
