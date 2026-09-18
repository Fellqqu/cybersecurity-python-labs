import os
import random
import sys

#папка шерд
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER

print(f"Студент: {STUDENT_NAME}, Група: {GROUP_NAME}, Варіант: {VARIANT_NUMBER}\n")

#вихідні паролі
passwords = [
    "APT@Detect10n",
    "simple",
    "Red@Team2023",
    "participant",
    "Blue@T3am",
    "common123",
    "Purple@T34m",
    "regular123",
    "Gr33n@Team",
    "normal123",
    "qqq"
]

criteria = {
    "min_length": 7,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}

forbidden_passwords = {
    "simple",
    "participant",
    "common123",
    "regular123",
    "normal123",
    "test",
}

#дублікат паролів
random_indices = random.sample(range(len(passwords)), 3)
for idx in random_indices:
    passwords.append(passwords[idx])

#таблиця
print("--- результати аналізу надійності паролів ---")
print(f"{'пароль':<16} | {'статус':<15} | {'довжина':<7} | {'унікальний'}")
print("-" * 62)

#початок оцінки
for pwd in passwords:
    #базовий перевірка на 1 рівень
    is_forbidden = pwd.lower() in forbidden_passwords or len(pwd) < criteria["min_length"]
    length = len(pwd)
    is_unique = passwords.count(pwd) == 1

    #решта перевірки
    has_lower = any(c.islower() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(not c.isalnum() for c in pwd)

    #підрахунок критеріїв від 0 до 4
    met_groups = sum([has_lower, has_upper, has_digit, has_special])
    meets_all = met_groups == 4

    #присвоєння статусу
    if is_forbidden:
        status = "заборонений"
    elif meets_all and length >= (criteria["min_length"] + 4) and is_unique:
        status = "дуже сильний"
    elif meets_all:
        status = "сильний"
    elif met_groups >= 2:
        status = "середній"
    elif met_groups >= 1:
        status = "слабкий"
    else:
        status = "невиачений"

    #вивід
    unique_str = "так" if is_unique else "ні"
    print(f"{pwd:<16} | {status:<15} | {length:<7} | {unique_str}")
