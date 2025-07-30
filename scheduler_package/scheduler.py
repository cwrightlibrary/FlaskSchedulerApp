from utils import GenerateSchedule

schedule = GenerateSchedule("models/employees.csv", "models/employees_key.txt", "models/templates")

schedule.load_template("tuesday")