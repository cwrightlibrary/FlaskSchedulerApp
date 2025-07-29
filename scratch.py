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
cell_end = {
    "topl": "├", "topr": "┤", "topsp": "┼",
    "botl": "└", "botr": "┘", "botsp": "┴",
    "horz": "─", "vert": "│"
}

instance = ""

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
elif instance == "cell_end":
    border = cell_end

def _get_cell_type(last_cell: str, current_cell: str, next_cell: str):
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

instances = ["header", "section", "cell", "cell", "section", "cell", "cell"]

for i in range(len(instances)):
    last_cell, current_cell, next_cell = "", "", ""
    current_cell = instances[i]
    if i < len(instances) - 1:
        next_cell = instances[i + 1]
    if i > 0:
        last_cell = instances[i - 1]
    print(_get_cell_type(last_cell, current_cell, next_cell))