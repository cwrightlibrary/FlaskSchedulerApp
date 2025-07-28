from csv import reader
from datetime import datetime
from employees import Employee
from prettytable import PrettyTable


def employees_to_csv(employees_file: str, employees_key: str = "") -> list[Employee]:
    """
    Creates a list of employees from a properly-formatted CSV file. *Optionally decodes the employee names*

    Args:
        employees_file (str): Path to the formatted CSV file containing all employee information.
        employees_key (str): Path to the `employees_key.txt` file to decode randomized names.
    
    Returns:
        list: A list of each employee.
    """
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
                names = [line[: line.index("= ")], line[line.index("= ") + 2 :].strip()]
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

def tuesday_schedule(employees: list=[], date: str="Month XX, 20XX") -> str:
    """
    Generates a `prettytable` list formatted like the library ones with names appropriately added.

    Args:
        employees (list): A list created with the `employees_to_csv` function.
        date (str): A string of the current date formatted: `Month Day, Year`.
    
    Returns:
        str: The **current date** followed by the **header `prettytable`** of work hours and schedule adjustments and a **content `prettytable`** of the incremented shifts.
    """
    current_date = f"Tuesday {date}"
    header_table = PrettyTable(["who works today", "lunch breaks", "schedule changes"])
    content_table = PrettyTable(["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"])

    full_time = "FULL-TIME:\n"
    part_time = "PART-TIME:\n"
    security = "SECURITY:\n"

    ft_employees = {}
    pt_employees = {}
    sc_employees = {}
    hours_key = []
    for employee in employees:
        if employee.hours["tuesday-hours"]:
            day_hours = "-".join(employee.hours["tuesday-hours"])
            employee_first_name = employee.name.split(" ")[0]
            if employee.position in ["manager", "assistant manager", "supervisor", "full time"]:
                _employee_type_processor(day_hours, ft_employees, employee_first_name)
            elif employee.position in ["part time", "shelver"]:
                _employee_type_processor(day_hours, pt_employees, employee_first_name)
            elif employee.position in ["security full time", "security part time"]:
                _employee_type_processor(day_hours, sc_employees, employee_first_name)
            if employee.hours["tuesday-hours"] not in hours_key:
                hours_key.append(employee.hours["tuesday-hours"])
    
    ft_employees = dict(sorted(ft_employees.items(), key=lambda item: int(item[0].split("-")[0])))
    pt_employees = dict(sorted(pt_employees.items(), key=lambda item: int(item[0].split("-")[0])))
    sc_employees = dict(sorted(sc_employees.items(), key=lambda item: int(item[0].split("-")[0])))
    hours_key = sorted(hours_key, key=lambda x: int(x[0]))

    for hours, employees in ft_employees.items():
        start_time = _time_convert_to_12(hours.split("-")[0])
        end_time = _time_convert_to_12(hours.split("-")[1])
        full_time += f"{start_time}-{end_time}: {', '.join(employees)}\n"
    for hours, employees in pt_employees.items():
        start_time = _time_convert_to_12(hours.split("-")[0])
        end_time = _time_convert_to_12(hours.split("-")[1])
        part_time += f"{start_time}-{end_time}: {', '.join(employees)}\n"
    for hours, employees in sc_employees.items():
        start_time = _time_convert_to_12(hours.split("-")[0])
        end_time = _time_convert_to_12(hours.split("-")[1])
        security += f"{start_time}-{end_time}: {', '.join(employees)}\n"
    
    print(full_time)
    print(part_time)
    print(security)
    return ft_employees

def _employee_type_processor(day_hours: str, employee_type: dict, employee_first_name: str):
    if not day_hours in employee_type:
        employee_type[day_hours] = []
        employee_type[day_hours].append(employee_first_name)
    else:
        employee_type[day_hours].append(employee_first_name)

def _time_convert_to_12(time_24: str):
    dt = datetime.strptime(time_24, "%H%M")
    hour = dt.strftime("%I").lstrip("0")
    minute = dt.minute

    if minute == 0:
        return hour
    else:
        return f"{hour}:{dt.strftime("%M")}"