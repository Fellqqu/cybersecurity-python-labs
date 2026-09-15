import os
import random
import sys

# Підключення ваших даних з папки shared
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER

print(f"Студент: {STUDENT_NAME}, Група: {GROUP_NAME}, Варіант: {VARIANT_NUMBER}\n")

# --- ВАШІ ДАНІ ДЛЯ 11 ВАРІАНТУ (замініть на свої) ---
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
# ----------------------------------------------------


# 1. Вибираємо 3 випадкові паролі зі списку
random_passwords = random.sample(passwords, 3)
print("--- Перевірка 3 випадкових паролів ---")

# 2. Перевіряємо кожен вибраний пароль
for pwd in random_passwords:
    print(f"\nПеревіряємо пароль: {pwd}")

    # Перевірка 1: Чи є пароль у списку заборонених
    if pwd.lower() in forbidden_passwords:
        print("Статус: Ненадійний (пароль знаходиться у списку заборонених)")
        continue  # Переходимо до наступного пароля, цей вже не пройшов

    # Перевірка 2: Довжина пароля
    if len(pwd) < criteria["min_length"]:
        print(f"Статус: Ненадійний (коротший за {criteria['min_length']} символів)")
        continue

    # Перевірка 3: Наявність цифр
    if criteria["require_digits"]:
        has_digits = any(char.isdigit() for char in pwd)
        if not has_digits:
            print("Статус: Ненадійний (не містить жодної цифри)")
            continue

    # Перевірка 4: Наявність великих літер
    if criteria["require_upper"]:
        has_upper = any(char.isupper() for char in pwd)
        if not has_upper:
            print("Статус: Ненадійний (не містить великих літер)")
            continue

    # Перевірка 5: Наявність спеціальних символів (все, що не буква і не цифра)
    if criteria["require_special"]:
        has_special = any(not char.isalnum() for char in pwd)
        if not has_special:
            print("Статус: Ненадійний (не містить спеціальних символів)")
            continue

    # Якщо код дійшов сюди, значить пароль пройшов абсолютно всі перевірки
    print("Статус: Надійний пароль!")
