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
        
        for row in range(len(self.headers)):
            if len(self.headers[row]) == 1:
                pass
            else:
                for column in range(len(self.headers[row])):
                    if column < len(self.headers[row]) - 1:
                        print(self.headers[row][column])

        return ""

    def _center_text(self, text, size):
        if len(text) > size:
            return text[:size]
        left = (size - len(text)) // 2
        right = size - len(text) - left
        return " " * left + text + " " * right
    
    def _create_border(self, text: str, size: int, pos: str):
        header = {
            "topl": "┏", "topr": "┓", "topsp": "┳",
            "botl": "┣", "botr": "┫", "botsp": "┻",
            "horz": "━", "vert": "┃"
        }
        section = {
            "topl": "┢", "topr": "┪", "topsp": "┷",
            "botl": "┡", "botr": "┩", "botsp": "┯",
            "horz": "━", "vert": "┃"
        }
        cell = {
            "topl": "├", "topr": "┤", "topsp": "┼",
            "botl": "└", "botr": "┘", "botsp": "┴",
            "horz": "─", "vert": "│"
        }
        if text == "":
            mid = " " * size
        else:
            mid = self._center_text(text, size)
        
    
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
"""