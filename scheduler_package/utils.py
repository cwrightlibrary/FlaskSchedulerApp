from csv import reader
from datetime import datetime
from employees import Employee
from pathlib import Path
from prettytable import PrettyTable, TableStyle
from typing import List


class GenerateSchedule:
    """
    Generates a formatted `prettytable.PrettyTable` schedule for a given day.

    Args:
        employees (List[Employee]): A list of employees.
        date (str): Date string in the format *"Month Day, Year"*.
    
    Methods:
        str: Formatted string with header and content tables.
    """
    def __init__(self, employees_file: str, employees_key: str, templates_dir: str = "", date: datetime = datetime.today()):
        self.employees_key = None
        self.employees = self.load_employees(employees_file, employees_key)

        if Path(templates_dir).exists():
            self.templates_dir = Path(templates_dir)
            self.templates = self.load_templates()
        else:
            self.templates_dir = templates_dir
            self.templates = {}
        
        self.template = {}

        self.date = date
        self.weekday = self.date.strftime("%A")
        self.print_date = self.date.strftime("%A, %B ") + str(self.date.day) + self.date.strftime(", %Y")

        self.header_table = None
        self.schedule_table = None
    
    def load_employees(self, employees_file: str, employees_key: str = "") -> List[Employee]:
        """
        Parses a CSV of employee data and optionally decodes names using a key text file.

        Args:
            employees_file (str): Path to the formatted CSV file containing all employee information
            employees_key (str): Path to the `employees_key.txt` file to decode randomized names.
        
        Returns:
            list[Employee]: A list of Employee objects.
        """
        with open(employees_file, "r") as csvfile:
            csvreader = reader(csvfile)
            headers = next(csvreader)
            rows = list(csvreader)
        
        key_map = {}
        if Path(employees_key).exists():
            with open(employees_key, "r") as keyfile:
                for line in keyfile:
                    encoded, decoded = line.split("= ")
                    key_map[encoded.strip()] = decoded.strip()
                    self.employees_key = key_map
        
        employees = []
        for row in rows:
            name = key_map.get(row[0], row[0])
            employee = Employee()
            employee.name = name
            employee.first_name = name.split(" ")[0]
            employee.initials = "".join(part[0].upper() for part in name.replace("-", " ").split() if part)
            employee.rank = row[1]
            employee.position = row[2]

            for i in range(3, len(headers)):
                value = row[i]
                key = headers[i]
                if value not in {"off", "none"}:
                    start, end = value.split("-")
                    employee.hours[key] = [start, end]
                else:
                    employee.hours[key] = None
            
            employee.string_to_hours()
            employees.append(employee)
        
        return employees
    
    def load_templates(self):
        templates = {}
        for item in self.templates_dir.iterdir():
            templates[item.stem.replace("_", " ").replace(" template", "")] = item.name
        
        return templates

    def load_template(self, weekday: str):
        if weekday in self.templates.keys():
            template_path = f"{self.templates_dir}/{self.templates[weekday]}"
            if Path(template_path).exists():
                with open(template_path, "r", newline="") as csvfile:
                    csvreader = reader(csvfile)
                    data = list(csvreader)
                headers = data[0]
                rows = data[1:]
                info = [list(col) for col in zip(*rows)]
                employees = []

                if self.employees_key:
                    first_name_lookup = {key.split()[0].lower(): value.split()[0] for key, value in self.employees_key.items()}
                    for row in info:
                        new_row = []
                        for cell in row:
                            if cell.lower() == "none":
                                new_row.append("none")
                            elif "/" in cell:
                                parts = cell.split("/")
                                sublist = []
                                for part in parts:
                                    name = part.strip().lower()
                                    if name in first_name_lookup:
                                        sublist.append(first_name_lookup[name])
                                    elif name.isdigit():
                                        sublist.append(name)
                                    else:
                                        sublist.append(name)
                                new_row.append(sublist)
                            else:
                                name = cell.strip().lower()
                                new_row.append(first_name_lookup.get(name, name))
                        employees.append(new_row)
                
                for idx, key in enumerate(headers):
                    self.template[key] = employees[idx]
    
    def create_header(self):
        self.header_table = PrettyTable(["full time", "part time", "security", "lunch breaks", "schedule changes"])
        ft_employees = {}
        pt_employees = {}
        sc_employees = {}
        
        lunch_breaks = {}
        schedule_changes = {}

        for employee in self.employees:
            if employee.position in ["manager", "assistant manager", "supervisor", "full time"]:
                if employee.print_hours[f"{self.weekday.lower()}-hours"] != []:
                    if "-".join(employee.print_hours[f"{self.weekday.lower()}-hours"]) not in ft_employees:
                        ft_employees["-".join(employee.print_hours[f"{self.weekday.lower()}-hours"])] = []
                    ft_employees["-".join(employee.print_hours[f"{self.weekday.lower()}-hours"])].append(employee.name.split()[0])
            elif employee.position in ["part time", "shelver"]:
                if employee.print_hours[f"{self.weekday.lower()}-hours"] != []:
                    if "-".join(employee.print_hours[f"{self.weekday.lower()}-hours"]) not in pt_employees:
                        pt_employees["-".join(employee.print_hours[f"{self.weekday.lower()}-hours"])] = []
                    pt_employees["-".join(employee.print_hours[f"{self.weekday.lower()}-hours"])].append(employee.name.split()[0])
            elif employee.position in ["security full time", "security part time"]:
                if employee.print_hours[f"{self.weekday.lower()}-hours"] != []:
                    if "-".join(employee.print_hours[f"{self.weekday.lower()}-hours"]) not in sc_employees:
                        sc_employees["-".join(employee.print_hours[f"{self.weekday.lower()}-hours"])] = []
                    sc_employees["-".join(employee.print_hours[f"{self.weekday.lower()}-hours"])].append(employee.name.split()[0])
        
        ft_employees = dict(sorted(ft_employees.items(), key=lambda item: self._parse_dict_by_start_time(item[0])))
        pt_employees = dict(sorted(pt_employees.items(), key=lambda item: self._parse_dict_by_start_time(item[0])))
        sc_employees = dict(sorted(sc_employees.items(), key=lambda item: self._parse_dict_by_start_time(item[0])))

        ft_string = ""
        pt_string = ""
        sc_string = ""
        lunch_string = ""
        schedule_changes_string = ""

        for key, value in ft_employees.items():
            if len(value) >= 8:
                value1, value2 = value[:3], value[4:]
                ft_string += f"{key}: {', '.join(value1)}\n"
                ft_string += f"{', '.join(value2)}\n\n"
            else:
                ft_string += f"{key}: {', '.join(value)}\n\n"
        ft_string = ft_string.strip()

        for key, value in pt_employees.items():
            if len(value) >= 8:
                value1, value2 = value[:3], value[4:]
                pt_string += f"{key}: {', '.join(value1)}\n"
                pt_string += f"{', '.join(value2)}\n\n"
            else:
                pt_string += f"{key}: {', '.join(value)}\n\n"
        pt_string = pt_string.strip()

        for key, value in sc_employees.items():
            if len(value) >= 8:
                value1, value2 = value[:3], value[4:]
                sc_string += f"{key}: {', '.join(value1)}\n"
                sc_string += f"{', '.join(value2)}\n\n"
            else:
                sc_string += f"{key}: {', '.join(value)}\n\n"
        sc_string = sc_string.strip()
        
        self.header_table.add_row([ft_string, pt_string, sc_string, lunch_string, schedule_changes_string])

        for field in self.header_table.field_names:
            self.header_table.align[field] = "l"
        
        self.header_table.set_style(TableStyle.SINGLE_BORDER)

        print(self.header_table)
    
    def _parse_dict_by_start_time(self, key):
        start_str, end_str = key.split("-")
        if ":" not in start_str:
            start_str += ":00"
        if ":" not in end_str:
            end_str += ":00"
        
        start_hour, start_minute = map(int, start_str.split(":"))
        end_hour, end_minute = map(int, end_str.split(":"))
        
        if 1 <= start_hour <= 6:
            start_hour += 12
        if 1 <= end_hour <= 6:
            end_hour += 12
        
        start = datetime.strptime(f"{start_hour:02}:{start_minute:02}", "%H:%M")
        end = datetime.strptime(f"{end_hour:02}:{end_minute:02}", "%H:%M")

        return (start, end)


schedule = GenerateSchedule("models/employees.csv", "models/employees_key.txt", "models/templates", datetime(2025, 7, 29))

schedule.load_template("tuesday")
schedule.create_header()