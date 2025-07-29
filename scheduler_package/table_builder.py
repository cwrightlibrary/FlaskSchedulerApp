class TableBuilder:
    def __init__(self, headers: list, title: str = ""):
        self.title = title
        self.headers = [headers]
        self.sections = []
        self.cells = []

        self.minimum_width = 10
    
    def set_title(self, title: str):
        self.title = title
    
    def set_headers(self, headers: list):
        self.headers = [headers]
    
    def add_row(self, row: list, section: bool = False):
        if section:
            sec = [""] * len(self.headers)
            sec[0] = row[0]

        else:
            if len(row) != len(self.headers[0]):
                raise ValueError(f"Expected list of length {len(self.headers[0])}, got {len(row)}: {row}")
            else:
                self.cells.append(row)
    
    def set_minimum_width(self, width: int):
        self.minimum_width = width
    
    def build_table(self):
        widths = []
        for idx in range(len(self.headers)):
            col_idx = []
            for col in range(len(self.headers[idx])):
                current_col = self.minimum_width
                if len(self.headers[idx][col]) > current_col:
                    current_col = len(self.headers[idx][col])
                if len(self.cells[idx][col]) > current_col:
                    current_col = len(self.cells[idx][col])
                widths.append(current_col)
        
        all_rows = []
        for row in range(len(self.headers)):
            if len(self.headers[row]) == 1:
                pass
            else:
                top_mid_bot = ["", "", ""]
                for column in range(len(self.headers[row])):
                    if column == 0:
                        self._create_row(top_mid_bot, self.headers[row][column], self.minimum_width, "start", "header")
                    if column > 0 and column < len(self.headers[row]) - 1:
                        self._create_row(top_mid_bot, self.headers[row][column], self.minimum_width, "mid", "header")
                    if column == len(self.headers[row]) - 1:
                        self._create_row(top_mid_bot, self.headers[row][column], self.minimum_width, "end", "header")

                all_rows.append(top_mid_bot)
                print("\n".join(all_rows[0]))
        
        return ""

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

        }
        cell_section_bot = {

        }
        cell_end = {
            "topl": "├", "topr": "┤", "topsp": "┼",
            "botl": "└", "botr": "┘", "botsp": "┴",
            "horz": "─", "vert": "│"
        }
        if instance == "header":
            border = header
        elif instance == "section":
            border = section
        elif instance == "cell":
            border = cell
        
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