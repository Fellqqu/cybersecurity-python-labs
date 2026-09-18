#ДОБАВИТИ ВАЛІДАЦІЮ КОЛИ ВВОДИТЬСЯ ТІЛЬКИ ПАРОЛЬ АБО ТІЛЬКИ ЛОГІН




import csv
import hashlib
import json
import os
from datetime import datetime, timezone


#гарна помилка для хороших паролів
class ValidationError(Exception):
    pass


#сіль
PERSONAL_SALT = "00011"


#хешування паролів blake2b
def generate_hash(password: str, salt: str = "00000") -> str:
    if not password or not salt:
        raise ValueError("пароль або сіль не можуть бути порожніми")
    if len(password) < 12:
        raise ValidationError(f"пароль надто короткий мінімум 12 символів введено: {len(password)}")

    combined = password + salt
    hash_object = hashlib.blake2b(combined.encode("utf-8"))
    return hash_object.hexdigest()


#10 юзерів
users_to_register = (
    ("admin", "SuperPyperPass3!"),
    ("manager", "LoNgPass228@2"),
    ("user1", "gIgAmEgapass161!"),
    ("user2", "DuperSuperpass!!3"),
    ("guest", "sKiLLissuepass2!"),
    ("developer", "DeVBackpass5@1"),
    ("analyst", "TestPass1489@!j"),
    ("tester", "Plz5Pointlab5@"),
    ("auditor", "EzPasswordEz45!"),
    ("support", "Packettracerpass2!"),
    (" ", "ASSDXXssda2!ss"),
    ("fdsdf", " ")
)

#створення кортежу
def create_user(username, password):
    #додано перевірку на логін
    if not username or not username.strip():
        raise ValueError("Логін не може бути порожнім або складатися лише з пробілів.")

    hash_value = generate_hash(password, PERSONAL_SALT)
    return (username, hash_value)

#створює дату та юзер.цсв
def create_users(users_list):
    current_dir = os.path.dirname(os.path.abspath(__file__))#прихована змінна яка завжди зберігає ім'я поточного скрипта
    data_dir = os.path.join(current_dir, "data")
    csv_path = os.path.join(data_dir, "users.csv")

    try:
        os.makedirs(data_dir, exist_ok=True)
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:#віз закриває файл при помилці
            writer = csv.writer(file)
            for username, password in users_list:
                try:
                    writer.writerow(create_user(username, password))
                except (ValidationError, ValueError) as e:
                    print(f"Помилка створення {username}: {e}")
        print(f"Базу даних успішно створено! Файл: {csv_path}")
    except (OSError, PermissionError) as e:
        print(f"Помилка доступу до файлу: {e}")


#декоратор запису у джейсон
def log_event(func):
    def wrapper(username, password, users_db):
        status = "failure"
        try:
            result = func(username, password, users_db)
            status = "success" if result else "failure"
            return result
        except Exception:
            status = "failure"
            raise
        finally:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            log_path = os.path.join(current_dir, "data", "log.json")

            log_entry = {
                "event": "login",
                "user": username,
                "result": status,
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "args": [username, "***"],
                "kwargs": {},
            }

            try:
                logs_list = []
                if os.path.exists(log_path):
                    with open(log_path, "r", encoding="utf-8") as f:
                        if os.path.getsize(log_path) > 0:
                            logs_list = json.load(f)

                logs_list.append(log_entry)

                with open(log_path, "w", encoding="utf-8") as f:
                    json.dump(logs_list, f, indent=4)
            except (OSError, PermissionError) as log_error:
                print(f"Помилка запису логів: {log_error}")

    return wrapper


#функ читання ситає цсв і будує табличку
def read_users_db():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "data", "users.csv")
    users_db = []

    try:
        with open(csv_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    users_db.append((row[0], row[1]))

        print("\n--- База користувачів ---")
        print(f"{'Логін':<15} | {'Хеш пароля'}")
        print("-" * 50)
        for user, p_hash in users_db:
            print(f"{user:<15} | {p_hash[:20]}...")

        return users_db
    except FileNotFoundError:
        print("Помилка: Файл users.csv не знайдено.")
        return []
    except (OSError, PermissionError) as e:
        print(f"Помилка читання файлу: {e}")
        return []


#перевірка на прохід чи пароль валідний
@log_event
def login(username: str, password: str, users_db: list) -> bool:
    if not username or not password:
        raise ValueError("Логін або пароль не можуть бути порожніми.")

    login_hash = generate_hash(password, PERSONAL_SALT)

    for db_user, db_hash in users_db:
        if db_user == username:
            #пряме повернення результату порівняння
            return db_hash == login_hash

    return False


#головна функ
def main():
    print("--- реєстрація користувачів ---")
    create_users(users_to_register)

    print("\n--- зчитування бази ---")
    db = read_users_db()

    print("\n--- тестування входу ---")
    if db:
        try:
            print("спроба 1: успішний вхід (admin) ", login("admin", "SuperPyperPass3!", db))
            print("спроба 2: неправильний пароль (user1) ", login("user1", "WrongPass123", db))
            print("спроба 3: неіснуючий логін (hacker) ", login("hacker", "SuperPyperPass3!", db))
            print("спроба 4: пусті дані ", login("", "", db))
        except (ValueError, ValidationError) as e:
            print(f"Спроба 4 завершилася помилкою: {e}")


if __name__ == "__main__":
    main()
