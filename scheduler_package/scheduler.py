from utils import employees_to_csv, tuesday_schedule

employees = employees_to_csv("models/employees.csv", "models/employees_key.txt")
tuesday = tuesday_schedule(employees, "July 29, 2025")

print(tuesday)