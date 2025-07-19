import app

print("App imported successfully!")
print("Flask routes:")
for rule in app.app.url_map.iter_rules():
    print(f"- {rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")