"""Symbol: +* Single-side: False"""
import string

def _caesar_cipher(text, shift=3):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet + alphabet.upper(), shifted_alphabet + shifted_alphabet.upper())
    return text.translate(table)

def caesar_cipher(text):
    parts = text.split('|')
    if len(parts) == 2:
        try:
            shift = int(parts[0])
            return _caesar_cipher(parts[1], shift)
        except ValueError:
            return "{錯誤：請在 | 前提供有效的整數作為位移值}"
    else:
        return _caesar_cipher(text, 3)  # 默認位移 3