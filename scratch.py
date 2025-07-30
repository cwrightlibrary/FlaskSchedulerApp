header = [["", "9-11", "11-1", "1-2", "2-4", "4-6", "6-8"]]
section = [["", "", "", "", "", "", ""], ["workroom", "", "", "", "", "", ""], ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""]]
cell = [["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""], ["pick-up window", "Chris", "Sonaite", "Emaleigh", "Shawn", "Wil", "Deborah"]]

all_rows = header + section + cell
num_cols = len(header[0])

widths = []
for col in range(num_cols):
    max_len = max((len(row[col]) for row in all_rows if col < len(row)), default=0)
    widths.append(max(max_len, 10))

print(widths)
