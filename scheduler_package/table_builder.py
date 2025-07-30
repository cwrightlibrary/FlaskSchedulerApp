class TableBuilder:
    def __init__(self, headers: list, title: str = ""):
        self.title = title
        self.headers = [headers]
        self.sections = [[""] * len(headers)]
        self.cells = [[""] * len(headers)]
        self.order = ["header"]

        self.minimum_width = 10
        self.maximum_width = 22
    
    def set_title(self, title: str):
        self.title = title
    
    def set_headers(self, headers: list):
        self.headers = [headers]
    
    def add_row(self, row: list, section: bool = False):
        if section:
            empty = [""] * len(self.headers[0])
            sec = [""] * len(self.headers[0])
            sec[0] = row[0]
            self.sections.append(sec)
            self.cells.append(empty)
            self.order.append("section")
        else:
            if len(row) != len(self.headers[0]):
                raise ValueError(f"Expected list of length {len(self.headers[0])}, got {len(row)}: {row}")
            else:
                empty = [""] * len(self.headers[0])
                self.cells.append(row)
                self.sections.append(empty)
                self.order.append("cell")
    
    def set_minimum_width(self, width: int):
        self.minimum_width = width
    
    def set_maximum_width(self, width: int):
        self.maximum_width = width
    
    def build_table(self):
        widths_rows = self.headers + self.sections + self.cells
        widths_num_cols = len(self.headers[0])

        widths = []
        for col in range(widths_num_cols):
            max_len = max((len(row[col]) for row in widths_rows if col < len(row)), default=0)
            widths.append(min(max(max_len + 2, self.minimum_width), self.maximum_width))
        
        all_rows = []
        for idx, instance in enumerate(self.order):
            last_cell, current_cell, next_cell = "", "", ""
            top_mid_bot = ["", "", ""]
            
            if idx == 0:
                last_cell = ""
                current_cell = self.order[idx]
                next_cell = self.order[idx + 1]
            if idx > 0 and idx < len(self.order) - 1:
                last_cell = self.order[idx - 1]
                current_cell = self.order[idx]
                next_cell = self.order[idx + 1]
            if idx == len(self.order) - 1:
                last_cell = self.order[idx - 1]
                current_cell = self.order[idx]
                next_cell = ""

            if current_cell == "header":
                cell_type = "header"
            elif current_cell == "section":
                cell_type = "section"
            elif current_cell == "cell" and next_cell == "cell":
                cell_type = "cell_a"
            elif current_cell == "cell" and next_cell == "section":
                cell_type = "cell_b"
            elif current_cell == "cell" and next_cell == "":
                cell_type = "cell_c"


            if instance == "header":
                column_data = self.headers[idx]
            elif instance == "section":
                column_data = self.sections[idx]
            elif instance == "cell":
                column_data = self.cells[idx]

            for column in range(len(column_data)):
                if column == 0:
                    loc = "start"
                elif column > 0 and column < len(column_data) - 1:
                    loc = "mid"
                elif column == len(column_data) - 1:
                    loc = "end"
                # if cell_type == "section":
                #     print(loc)
                self._create_row(top_mid_bot, column_data[column], widths[column], loc, cell_type)
            
            if cell_type != "header":
                top_mid_bot = [top_mid_bot[1], top_mid_bot[2]]
            all_rows.append(top_mid_bot)
        
        title_text = self.title
        full_width = len("\n".join(all_rows[0]).split("\n")[0])
        self.title = self._center_text(title_text, full_width)

        full_string = f"{self.title}\n"
        for row in all_rows:
            full_string += f"{'\n'.join(row)}\n"

        return full_string

    def _center_text(self, text, size):
        if len(text) > size:
            return text[:size]
        left = (size - len(text)) // 2
        right = size - len(text) - left
        return " " * left + text + " " * right
    
    def _create_border(self, text: str, size: int, pos: str, instance: str):
        header = {
            "topl": "┏", "topr": "┓", "topsp": "┳",
            "botl": "┣", "botr": "┫", "botsp": "┻",
            "horz": "━", "vert": "┃"
        }
        section = {
            "botl": "┡", "botr": "┩", "botsp": "┯",
            "horz": "━", "vert": "┃"
        }
        cell_a = {
            "botl": "├", "botr": "┤", "botsp": "┼",
            "horz": "─", "vert": "│"
        }
        cell_b = {
            "botl": "┢", "botr": "┪", "botsp": "┷",
            "horz": "━", "vert": "│"
        }
        cell_c = {
            "botl": "└", "botr": "┘", "botsp": "┴",
            "horz": "─", "vert": "│"
        }

        if instance == "header":
            border = header
        elif instance == "section":
            border = section
        elif instance == "cell_a":
            border = cell_a
        elif instance == "cell_b":
            border = cell_b
        elif instance == "cell_c":
            border = cell_c
        
        text_size = size - 2
        if text == "" and pos != "start":
            mid = f" {' ' * size}{border['vert']}"
        else:
            if pos == "start" and instance != "section":
                mid = f"{border['vert']} {self._center_text(text, text_size)} {border['vert']}"
            elif instance != "section":
                mid = f" {self._center_text(text, text_size + 1)} {border['vert']}"
        
        if instance == "section":
            if pos == "start":
                mid = f"{border['vert']} {text}{' ' * (size-len(text))}"
            if pos == "mid":
                mid = f"{' ' * size}  "
            if pos == "end":
                mid = f"{" " * size} {border['vert']}"

        if pos == "start":
            if instance == "header":
                top = border["topl"] + border["horz"] * size + border["topsp"]
            bot = border["botl"] + border["horz"] * size + border["botsp"]
        elif pos == "mid":
            if instance == "header":
                top = border["horz"] + border["horz"] * size + border["topsp"]
            bot = border["horz"] + border["horz"] * size + border["botsp"]
        elif pos == "end":
            if instance == "header":
                top = border["horz"] + border["horz"] * size + border["topr"]
            bot = border["horz"] + border["horz"] * size + border["botr"]
        
        if instance == "header":
            return (top, mid, bot)
        else:
            return ("", mid, bot)
    
    def _create_row(self, top_mid_bot: list, header_section_cell: str, size: int, pos: str, instance: str):
        temp_top, temp_mid, temp_bot = self._create_border(header_section_cell, size, pos, instance)
        top_mid_bot[0] += temp_top
        top_mid_bot[1] += temp_mid
        top_mid_bot[2] += temp_bot
    
    def _get_cell_type(self, last_cell: str, current_cell: str, next_cell: str):
        if not last_cell:
            return f"{current_cell}_{next_cell}_bot"
        if current_cell == "header":
            return f"{current_cell}_only" if not next_cell else f"{current_cell}_{next_cell}_bot"
        if current_cell == "section":
            return f"{current_cell}_{last_cell}_top"
        if current_cell == "cell":
            if last_cell in {"header", "section"}:
                return f"{current_cell}_{last_cell}_top"
            if last_cell == "cell":
                if next_cell == "section":
                    return f"{current_cell}_{next_cell}_bot"
                if not next_cell:
                    return f"{current_cell}_end"
    
    def save(self):
        with open("schedule_table.txt", "w") as f:
            f.write(self.build_table())

    def __str__(self):
        return f"{self.build_table()}"

test = TableBuilder(["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"], "Test")
test.add_row(["workroom"], section=True)
test.add_row(["pick-up window", "Jess", "Yami", "Chris", "Shawn", "Cheryl", "Deborah"])
test.add_row(["floor lead", "Chris", "Janet", "", "Janet", "", "Sonaite"])
test.add_row(["computer desk"], section=True)
test.add_row(["service pt 1", "Janet", "Cat", "Jess", "Chris", "Wendy", "Cheryl"])
test.add_row(["service pt 1", "", "Emaleigh", "", "Lea", "Emaleigh", "Shawn"])
test.add_row(["staff/time permitting"], section=True)
test.add_row(["meetings/programs", "", "", "", "", "", ""])
test.add_row(["project time", "RF, AY, YE", "RF, LS, JB", "LS, EK, LT, CA", "RF, AY, YE, SDK, EK", "MD, SS; LS; RF, YE, JB, CW, LT, JH, AY", "MD, LT"])

print(test)
# test.save()