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

security_levels = ("Public", "Internal Use", "Restricted", "Highly Restricted")

blocked_users = {"obsolete_system", "contract_expired", "legal_hold"}

print("--- список ресурсів ---")
#виводи ресурси , цифри переводим в текст віднімаючи 1 , бо порядок з 0
for res_name, res_level in resources:
    level_name = security_levels[res_level - 1]
    print(f"ресурс: {res_name} | рівень: {level_name}")

print("\n--- перевірка доступу ---")
#список для перевірки умов , + 1 рандомний щоб перевірити як відреагує програма
users_to_test = list(users.keys()) + ["unknown_hacker"]

#перевірка кожного юзера до ресурсу
for username in users_to_test:
    for res_name, res_level in resources:
        #перевірка чи є в системі
        if username not in users:
            print(f"user={username} resource={res_name} -> DENY (user not found)")
            continue

        #перевірка на блокіровку
        if username in blocked_users:
            print(f"user={username} resource={res_name} -> DENY (user is blocked)")
            continue

        #перевірка на тру
        user_data = users[username]
        if not user_data["active"]:
            print(f"user={username} resource={res_name} -> DENY (account inactive)")
            continue

        #перевірка ассес контролу
        if user_data["clearance"] >= res_level:
            print(f"user={username} resource={res_name} -> ALLOW")
        else:
            print(
                f"user={username} resource={res_name} -> DENY (insufficient clearance)"
            )

    print("-" * 30)
