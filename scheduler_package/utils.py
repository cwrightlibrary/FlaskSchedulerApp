from csv import reader

from .employees import Employee

def employees_to_csv(employees_file: str, employees_key: str="") -> list[Employee]:
    csv_fields = []
    csv_rows = []

    valid_key = False
    txt_rows = []

    employees = []

    with open(employees_file, "r") as csvfile:
        csvreader = reader(csvfile)
        csv_fields = next(csvreader)

        for row in csvreader:
            csv_rows.append(row)
    
    if employees_key != "":
        valid_key = True
        with open(employees_key, "r") as key:
            for line in key:
                names = [line[:line.index("= ")], line[line.index("= ") + 2:-1]]
                txt_rows.append(names)
    
    for csv_row in csv_rows:
        employee = Employee()
        if valid_key:
            for txt_row in txt_rows:
                if csv_row[0] in txt_row[0]:
                    employee.name = txt_row[1]
        else:
            employee.name = csv_row[0]
        employee.rank = csv_row[1]
        employee.position = csv_row[2]

        for i in range(3, len(csv_fields)):
            if csv_row[i] not in ["off", "none"]:
                start_hour = csv_row[i].split("-")[0]
                end_hour = csv_row[i].split("-")[1]
                both_hours = [start_hour, end_hour]

                employee.hours[csv_fields[i]] = both_hours
            else:
                employee.hours[csv_fields[i]] = None
        
        employee.string_to_hours()
        employees.append(employee)
    
    return employees
