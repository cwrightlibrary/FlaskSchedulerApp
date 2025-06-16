import csv

from scheduler_package.employees import Employee


if __name__ == "__main__":
    employees_file = "models/employees.csv"
    all_nums = "allnums.txt"

    allnums = open(all_nums, "w")
    
    with open(employees_file, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            for subrow in row:
                if "-" in subrow:
                    allnums.write(subrow + "\n")
