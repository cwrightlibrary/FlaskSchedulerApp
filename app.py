import csv
from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # app.run(debug=True)

    employees_file = "models/employees.csv"
    employees_key = "models/employees_key.txt"

    with open(employees_file, mode="r") as file:
        csv_file = csv.reader(file)
        for lines in csv_file:
            key = open(employees_key, mode="r")
            for line in key:
                start_loc = line.index("= ")
                old_name = line[:start_loc]
                new_name = line[start_loc + 2:]

                print(old_name + "\n" + new_name)

