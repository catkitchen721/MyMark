"""Symbol: # Single-side: False"""
import random
def random_num(text):
       try:
           text_num = int(text)
           random_number = random.randint(0, text_num)
           return f'{random_number}'
       except ValueError:
           return text