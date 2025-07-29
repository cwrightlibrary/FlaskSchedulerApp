from utils import employees_to_csv, GenerateSchedule

employees = employees_to_csv("models/employees.csv", "models/employees_key.txt")

tuesday = GenerateSchedule(employees)

