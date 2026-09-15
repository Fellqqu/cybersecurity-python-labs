# Вхідні дані для Варіанту 11
users = {
    "risk_manager": {
        "role": "risk_analyst",
        "clearance": 4,
        "department": "Risk Management",
        "active": True,
    },
    "business_analyst": {
        "role": "business_analyst",
        "clearance": 2,
        "department": "Business",
        "active": True,
    },
    "legal_counsel": {
        "role": "legal",
        "clearance": 3,
        "department": "Legal",
        "active": True,
    },
    "contractor_dev": {
        "role": "contractor",
        "clearance": 2,
        "department": "Contract",
        "active": True,
    },
    "obsolete_system": {
        "role": "legacy_system",
        "clearance": 1,
        "department": "Legacy",
        "active": False,
    },
}

resources = [
    ("risk_registers", 4),
    ("business_requirements", 2),
    ("legal_documents", 3),
    ("contract_code", 2),
    ("governance_framework", 4),
    ("meeting_minutes", 1),
    ("regulatory_reports", 3),
    ("executive_dashboards", 4),
    ("project_specs", 2),
    ("public_statements", 1),
]

# Виправлено одруківку з методички (було зайве Use")
security_levels = ("Public", "Internal Use", "Restricted", "Highly Restricted")

blocked_users = {"obsolete_system", "contract_expired", "legal_hold"}

print("--- СПИСОК РЕСУРСІВ ---")
# Виводимо ресурси, замінюючи цифру на текст (віднімаємо 1, бо індекси починаються з 0)
for res_name, res_level in resources:
    level_name = security_levels[res_level - 1]
    print(f"Ресурс: {res_name} | Рівень: {level_name}")

print("\n--- ПЕРЕВІРКА ДОСТУПУ ---")
# Щоб перевірити всі умови, створимо список користувачів для перевірки.
# Беремо існуючих користувачів + додаємо заблокованого + додаємо неіснуючого
users_to_test = list(users.keys()) + ["unknown_hacker"]

# Перевіряємо кожного користувача до кожного ресурсу
for username in users_to_test:
    for res_name, res_level in resources:
        # 1. Перевірка на існування в системі
        if username not in users:
            print(f"user={username} resource={res_name} -> DENY (User not found)")
            continue  # Йдемо до наступного ресурсу

        # 2. Перевірка на блокування
        if username in blocked_users:
            print(f"user={username} resource={res_name} -> DENY (User is blocked)")
            continue

        # 3. Перевірка на активність акаунта
        user_data = users[username]
        if not user_data["active"]:
            print(f"user={username} resource={res_name} -> DENY (Account inactive)")
            continue

        # 4 та 5. Перевірка рівня допуску
        if user_data["clearance"] >= res_level:
            print(f"user={username} resource={res_name} -> ALLOW")
        else:
            print(
                f"user={username} resource={res_name} -> DENY (Insufficient clearance)"
            )

    print("-" * 30)  # Візуальний розділювач між користувачами
