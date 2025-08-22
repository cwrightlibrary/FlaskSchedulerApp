from prettytable import PrettyTable

# ----- Employee information ----- #

EMPLOYEES = {
  "Michelle": {
    "name": "Michelle DuPre",
    "hours": "9-5:30"
  },
  "Rod": {
    "name": "Rod Franco",
    "hours": "9-5:30"
  },
  "Jess": {
    "name": "Jess Bryant",
    "hours": "9-5:30"
  },
  "Chris": {
    "name": "Chris Wright",
    "hours": "9-5:30"
  },
  "Wil": {
    "name": "Wil Meade",
    "hours": "2-8"
  },
  "Janet": {
    "name": "Janet Henson",
    "hours": "2-8"
  },
  "Emaleigh": {
    "name": "Emaleigh Kitchen",
    "hours": "2-8"
  },
  "Lindsey": {
    "name": "Lindsey Taunton",
    "hours": "2-8"
  }
}

# ----- Header table ----- #

header = PrettyTable(["Who works today", "Changes"])

work_today = {}
for employee in EMPLOYEES.keys():
  if EMPLOYEES[employee]["hours"] not in work_today:
    work_today[EMPLOYEES[employee]["hours"]] = []
  work_today[EMPLOYEES[employee]["hours"]].append(EMPLOYEES[employee]["name"].split()[0])

work_today_str = ""
for k, v in work_today.items():
  work_today_str += f"{k}:\n{", ".join(v)}\n"

header_info = [work_today_str.strip(), ""]

header.add_row(header_info)

# ----- Schedule information ----- #

TEMPLATE = {
  "pick-up window":   ["Chris", "Jess", "Rod", "Wil", "Janet", "Emaleigh"],
  "service point 1":  ["Jess", "Rod", "Chris", "Janet", "Emaleigh", "Wil"],
  "service point 2":  ["Rod", "Chris", "Jess", "Emaleigh", "Wil", "Janet"],
}

hours = ["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"]
time_comp = [[9, 11], [11, 13], [13, 14], [14, 16], [16, 18], [18, 20]]

template = PrettyTable(hours)

updated_template = {}
for location, employees in TEMPLATE.items():
  if location not in updated_template:
    updated_template[location] = [""] * (len(hours) - 1)
  for idx, employee in enumerate(employees):
    updated_template[location][idx] = EMPLOYEES[employee]["name"].split()[0]

num_slots = len(next(iter(updated_template.values())))

def check_slots(test, slots):
  start, end = test
  proof = []
  

off_desk = []
for i in range(num_slots):
  on_desk = {updated_template[station][i] for station in updated_template}
  off_desk_at_i = [EMPLOYEES[name]["name"] for name in EMPLOYEES.keys() if name not in on_desk]
  off_desk_at_i = []
  for name in EMPLOYEES.keys():
    if name not in on_desk:
      start_time = float(EMPLOYEES[name]["hours"].split("-")[0]) + 12 if float(EMPLOYEES[name]["hours"].split("-")[0]) < 8 else float(EMPLOYEES[name]["hours"].split("-")[0])
      end_time = float(EMPLOYEES[name]["hours"].split("-")[1].replace(":30", ".5"))
      if start_time <= time_comp[i][0] or (start_time < time_comp[i][0] and end_time < time_comp[i][1]):
        off_desk_at_i.append(EMPLOYEES[name]["name"])
			
  off_desk.append(off_desk_at_i)

project_time = []
for employees in off_desk:
  employee_names = [f"{e.split()[0][0]}{e.split()[1][0]}" for e in employees]
  project_time.append(", ".join(employee_names))

updated_template["project time"] = project_time

locations = []
for location, employees in updated_template.items():
  loc = [location]
  for employee in employees:
    loc.append(employee)
  locations.append(loc)

for l in locations:
  template.add_row(l, divider=True)

# ----- Print tables ----- #

print(header)
print(template)