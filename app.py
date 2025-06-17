from flask import Flask, render_template, url_for

from scheduler_package.utils import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # app.run(debug=True)

    employees_file = "models/employees.csv"
    employees_key = "models/employees_key.txt"

    employees = employees_to_csv(employees_file, employees_key)

    monday_hours = {}
    
    for employee in employees:
        joined_hours = "-".join(employee.print_hours["monday-hours"])
        monday_hours.setdefault(joined_hours, []).append(employee.name)
    
    for keys, values in monday_hours.items():
        print(keys)
        print(values)
        print("\n")
