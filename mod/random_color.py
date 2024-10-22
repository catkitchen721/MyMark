"""Symbol: $$ Single-side: True"""
import random

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    hex_color = f'#{r:02x}{g:02x}{b:02x}'
    return f'<span style="background-color: {hex_color}; padding: 2px 5px; border-radius: 3px; color: white;">隨機顏色: {hex_color}</span>'
