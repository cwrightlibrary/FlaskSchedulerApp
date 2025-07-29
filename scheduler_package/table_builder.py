class TableBuilder:
    def __init__(self, headers: list, title: str = ""):
        self.title = title
        self.headers = [headers]
        self.sections = [[""] * len(headers)]
        self.cells = [[""] * len(headers)]
        self.order = ["header"]

        self.minimum_width = 10
    
    def set_title(self, title: str):
        self.title = title
    
    def set_headers(self, headers: list):
        self.headers = [headers]
        self.order.append("header")
    
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
    
    def build_table(self):
        widths = []
        for idx in range(len(self.headers)):
            col_idx = []
            for col in range(len(self.headers[idx])):
                current_width = self.minimum_width
                if len(self.headers[idx][col]) > current_width:
                    current_width = len(self.headers[idx][col])
                if len(self.cells[idx][col]) > current_width:
                    current_width = len(self.cells[idx][col])
                widths.append(current_width)
            # for col in range(len(self.headers[idx])):
            #     current_col = self.minimum_width
            #     if len(self.headers[idx][col]) > current_col:
            #         current_col = len(self.headers[idx][col])
            #     if len(self.cells[idx][col]) > current_col:
            #         current_col = len(self.cells[idx][col])
            #     widths.append(current_col)
        
        all_rows = []
        # for row in range(len(self.headers)):
        #     if len(self.headers[row]) == 1:
        #         pass
        #     else:
        #         top_mid_bot = ["", "", ""]
        #         for column in range(len(self.headers[row])):               
        #             if column == 0:
        #                 self._create_row(top_mid_bot, self.headers[row][column], self.minimum_width, "start", "header")
        #             if column > 0 and column < len(self.headers[row]) - 1:

        #                 self._create_row(top_mid_bot, self.headers[row][column], self.minimum_width, "mid", "header")
        #             if column == len(self.headers[row]) - 1:
        #                 self._create_row(top_mid_bot, self.headers[row][column], self.minimum_width, "end", "header")
        #         all_rows.append(top_mid_bot)
        #         print("\n".join(all_rows[0]))
        for idx, instance in enumerate(self.order):
            last_cell, current_cell, next_cell = "", "", ""
            top_mid_bot = ["", "", ""]

            # current_cell = instance
            # if idx == 0:
            #     next_cell = self.order[idx + 1]
            # elif idx > 0 and idx < len(self.order) - 1:
            #     last_cell = self.order[idx - 1]
            #     next_cell = self.order[idx + 1]
            
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
            
            # cell_type = self._get_cell_type(last_cell, current_cell, next_cell)
            if current_cell == "header" and next_cell == "section":
                cell_type = "header_section_bot"
            if current_cell == "section" and next_cell == "cell":
                cell_type = "section_header_top"
            if current_cell == "section" and last_cell == "cell":
                cell_type = "section_cell_top"
            if current_cell == "cell" and last_cell == "section":
                cell_type = "cell_section_top"
            if current_cell == "cell" and next_cell == "section":
                cell_type = "cell_section_bot"
            if current_cell == "cell" and next_cell == "cell":
                cell_type = "cell_cell_bot"
            if current_cell == "cell" and next_cell == "":
                cell_type = "cell_end"

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
                self._create_row(top_mid_bot, column_data[column], self.minimum_width, loc, cell_type)
            
            all_rows.append(top_mid_bot)
            print("\n".join(top_mid_bot))


        return ""

    def _center_text(self, text, size):
        if len(text) > size:
            return text[:size]
        left = (size - len(text)) // 2
        right = size - len(text) - left
        return " " * left + text + " " * right
    
    def _create_border(self, text: str, size: int, pos: str, instance: str):
        header_only = {
            "topl": "┏", "topr": "┓", "topsp": "┳",
            "botl": "┗", "botr": "┛", "botsp": "┻",
            "horz": "━", "vert": "┃"
        }
        header_section_bot = {
            "topl": "┏", "topr": "┓", "topsp": "┳",
            "botl": "┣", "botr": "┫", "botsp": "┻",
            "horz": "━", "vert": "┃"
        }
        header_cell_bot = {
            "topl": "┏", "topr": "┓", "topsp": "┳",
            "botl": "┡", "botr": "┩", "botsp": "╇",
            "horz": "━", "vert": "┃"
        }
        section_header_top = {
            "topl": "┣", "topr": "┫", "topsp": "┻",
            "botl": "┡", "botr": "┩", "botsp": "┯",
            "horz": "━", "vert": "┃"
        }
        section_cell_top = {
            "topl": "┢", "topr": "┪", "topsp": "┷",
            "botl": "┡", "botr": "┩", "botsp": "┯",
            "horz": "━", "vert": "┃"
        }
        cell_header_top = {
            "topl": "┡", "topr": "┩", "topsp": "╇",
            "botl": "├", "botr": "┤", "botsp": "┼",
            "horz": "─", "vert": "│"
        }
        cell_section_top = {
            "topl": "┡", "topr": "┩", "topsp": "┯",
            "botl": "├", "botr": "┤", "botsp": "┼",
            "horz": "─", "vert": "│"
        }
        cell_section_bot = {
            "topl": "├", "topr": "┤", "topsp": "┼",
            "botl": "┢", "botr": "┪", "botsp": "┷",
            "horz": "─", "vert": "│"
        }
        cell_cell_bot = {
            "topl": "├", "topr": "┤", "topsp": "┼",
            "botl": "├", "botr": "┤", "botsp": "┼",
            "horz": "─", "vert": "│"
        }
        cell_end = {
            "topl": "├", "topr": "┤", "topsp": "┼",
            "botl": "└", "botr": "┘", "botsp": "┴",
            "horz": "─", "vert": "│"
        }

        if instance == "header_only":
            border = header_only
        elif instance == "header_section_bot":
            border = header_section_bot
        elif instance == "header_cell_bot":
            border = header_cell_bot
        elif instance == "section_header_top":
            border = section_header_top
        elif instance == "section_cell_top":
            border = section_cell_top
        elif instance == "section_cell_top":
            border = section_cell_top
        elif instance == "cell_header_top":
            border = cell_header_top
        elif instance == "cell_section_top":
            border = cell_section_top
        elif instance == "cell_section_bot":
            border = cell_section_bot
        elif instance == "cell_cell_bot":
            border = cell_cell_bot
        elif instance == "cell_end":
            border = cell_end
        
        text_size = size - 2
        if text == "":
            mid = f"{border['vert']}{' ' * size}{border['vert']}"
        else:
            if pos == "start":
                mid = f"{border['vert']} {self._center_text(text, text_size)} {border['vert']}"
            else:
                mid = f" {self._center_text(text, text_size + 1)} {border['vert']}"

        if pos == "only":
            top = border["topl"] + border["horz"] * size + border["topr"]
            bot = border["botl"] + border["horz"] * size + border["botr"]
        elif pos == "start":
            top = border["topl"] + border["horz"] * size + border["topsp"]
            bot = border["botl"] + border["horz"] * size + border["botsp"]
        elif pos == "mid":
            top = border["horz"] + border["horz"] * size + border["topsp"]
            bot = border["horz"] + border["horz"] * size + border["botsp"]
        elif pos == "end":
            top = border["horz"] + border["horz"] * size + border["topr"]
            bot = border["horz"] + border["horz"] * size + border["botr"]
        
        return (top, mid, bot)
    
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
    
    def __str__(self):
        return self.build_table()

test = TableBuilder(["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"], "Test")
test.add_row(["workroom"], True)
test.add_row(["pick-up window", "Chris", "Sonaite", "Emaleigh", "Shawn", "Wil", "Deborah"])

print(test)

"""
       TABLE
┏━━━━━━━━┳━━━━━━━━┓
┃        ┃        ┃
┣━━━━━━━━┻━━━━━━━━┫
┃                 ┃
┡━━━━━━━━┯━━━━━━━━┩
│        │        │
├────────┼────────┤
│        │        │
┢━━━━━━━━┷━━━━━━━━┪
┃                 ┃
┡━━━━━━━━┯━━━━━━━━┩
│        │        │
├────────┼────────┤
│        │        │
└────────┴────────┘

┏━━━━━━━━┳━━━━━━━━┓
┃        ┃        ┃
┡━━━━━━━━╇━━━━━━━━┩
│        │        │
┢━━━━━━━━┷━━━━━━━━┪
┃                 ┃
┡━━━━━━━━┯━━━━━━━━┩
│        │        │
├────────┼────────┤
│        │        │
└────────┴────────┘
"""