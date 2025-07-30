from csv import DictReader, reader
from datetime import datetime
from employees import Employee
from pathlib import Path
from typing import List, Optional


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
                with open(template_path, "r") as csvfile:
                    csvreader = DictReader(csvfile)
                    data = [row for row in csvfile]
                print(data)