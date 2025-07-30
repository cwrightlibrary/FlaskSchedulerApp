row = 0
while row < len(self.order):
    for col in range(len(self.cells[row])):
        if len(self.cells[row][col]) > self.maximum_width:
            print(self.cells[row][col])
            empty_newline = [""] * len(self.headers[0])
            newline = [""] * len(self.headers[0])
            # Find the last space before maximum_width
            for i in range(self.maximum_width, 0, -1):
                if self.cells[row][col][i] == " ":
                    print("yes")
                    # Split text at the space
                    newline[col] = self.cells[row][col][i + 1:]
                    self.cells[row][col] = self.cells[row][col][:i]
                    break
            # Insert new row
            self.order.insert(row + 1, "newline")
            self.sections.insert(row + 1, empty_newline)
            self.cells.insert(row + 1, newline)
            # Do not increment row so that we reprocess the newly added row
            continue  # Re-check the new split in the next iteration
    row += 1  # Only increment if no split was needed
