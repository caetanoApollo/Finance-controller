from datetime import datetime

def formatar_data(data):
    return data.strftime("%d-%m-%Y")

def calcular_total(valores):
    return sum(valores)