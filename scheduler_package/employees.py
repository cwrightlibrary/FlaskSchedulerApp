class Employee:
    def __init__(self):
        self.name = ""
        self.rank = ""
        self.position = ""

        self.hours = {}
        self.print_hours = {}
    
    def string_to_hours(self):
        self.print_hours = {key: [] for key in self.hours}
        for key, hours in self.hours.items():
            if hours != None:
                hour1 = int(hours[0][:2])
                hour2 = int(hours[1][:2])
                minutes1 = int(hours[0][2:])
                minutes2 = int(hours[1][2:])

                hour1_12 = hour1 % 12 or 12
                hour2_12 = hour2 % 12 or 12

                converted_hours = []

                if minutes1 == 0:
                    converted_hours.append(f"{hour1_12}")
                else:
                    converted_hours.append(f"{hour1_12}:{minutes1:02}")
                
                if minutes2 == 0:
                    converted_hours.append(f"{hour2_12}")
                else:
                    converted_hours.append(f"{hour2_12}:{minutes2:02}")

                self.print_hours[key] = converted_hours
