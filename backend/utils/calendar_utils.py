"""
Utilitários para trabalhar com calendário, feriados e dias úteis
"""
import datetime
from typing import Set

# Feriados nacionais brasileiros fixos
BRAZILIAN_FIXED_HOLIDAYS = {
    (1, 1): "Ano Novo",
    (4, 21): "Tiradentes",
    (5, 1): "Dia do Trabalho",
    (9, 7): "Independência do Brasil",
    (10, 12): "Nossa Senhora Aparecida",
    (11, 2): "Finados",
    (11, 15): "Proclamação da República",
    (12, 25): "Natal",
}

def calculate_easter(year: int) -> datetime.date:
    """
    Calcula a data da Páscoa para um ano específico usando o algoritmo de Meeus/Jones/Butcher
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)

def get_brazilian_holidays(year: int) -> Set[datetime.date]:
    """
    Retorna o conjunto de feriados brasileiros para um ano específico
    Inclui feriados fixos e móveis (Carnaval, Sexta-feira Santa, Corpus Christi)
    """
    holidays = set()
    
    # Adicionar feriados fixos
    for (month, day), name in BRAZILIAN_FIXED_HOLIDAYS.items():
        holidays.add(datetime.date(year, month, day))
    
    # Calcular feriados móveis baseados na Páscoa
    easter = calculate_easter(year)
    
    # Carnaval (47 dias antes da Páscoa)
    carnival = easter - datetime.timedelta(days=47)
    holidays.add(carnival)
    
    # Sexta-feira Santa (2 dias antes da Páscoa)
    good_friday = easter - datetime.timedelta(days=2)
    holidays.add(good_friday)
    
    # Corpus Christi (60 dias depois da Páscoa)
    corpus_christi = easter + datetime.timedelta(days=60)
    holidays.add(corpus_christi)
    
    return holidays

def is_holiday(date: datetime.date) -> bool:
    """
    Verifica se uma data é feriado brasileiro
    """
    holidays = get_brazilian_holidays(date.year)
    return date in holidays

def is_weekend(date: datetime.date) -> bool:
    """
    Verifica se uma data é final de semana (sábado ou domingo)
    """
    return date.weekday() >= 5

def is_business_day(date: datetime.date) -> bool:
    """
    Verifica se uma data é dia útil (não é feriado nem final de semana)
    """
    return not is_weekend(date) and not is_holiday(date)

def next_business_day(date: datetime.date) -> datetime.date:
    """
    Retorna o próximo dia útil a partir de uma data
    """
    next_day = date
    while not is_business_day(next_day):
        next_day += datetime.timedelta(days=1)
    return next_day

def add_business_days(start_date: datetime.date, num_days: int) -> datetime.date:
    """
    Adiciona um número de dias úteis a uma data
    Retorna a data final (último dia útil trabalhado)
    """
    if num_days <= 0:
        return start_date
    
    current_date = start_date
    days_counted = 0
    
    while days_counted < num_days:
        if is_business_day(current_date):
            days_counted += 1
            if days_counted < num_days:
                current_date += datetime.timedelta(days=1)
        else:
            current_date += datetime.timedelta(days=1)
    
    return current_date

def count_business_days(start_date: datetime.date, end_date: datetime.date) -> int:
    """
    Conta o número de dias úteis entre duas datas (inclusive)
    """
    if start_date > end_date:
        return 0
    
    count = 0
    current_date = start_date
    
    while current_date <= end_date:
        if is_business_day(current_date):
            count += 1
        current_date += datetime.timedelta(days=1)
    
    return count
