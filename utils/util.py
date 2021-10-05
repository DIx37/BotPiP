"""Преобразование значений в смайлы"""
def smile(sost):
    if sost == "0":
        res = "🔴"
    elif sost == "1":
        res = "🟢"
    elif sost == "-":
        res = "-"
    else:
        res = "❌"
    return res