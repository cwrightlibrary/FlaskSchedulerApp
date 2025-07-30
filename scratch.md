i have this python script:

```
class Strings:
    def __init__(self, strings: list):
        self.minimum_size = 10
        self.maximum_size = 25
        self.table_width = 0

        self.strings = strings
        self.final = ""
    
    def set_table_width(self, width: int):
        self.table_width = width
    
    def create_table(self):
        strings_string = ""
        for s in self.strings:
            strings_string += f"{'=' * self.minimum_size}\n"
        
        self.final = strings_string
    
    def __str__(self):
        return self.final


data = ["", "", ""]

test = Strings(data)
test.set_table_width(139)
test.create_table()

print(test)
```

adjust `set_table_width` so that it sets `self.minimum_width` to add up to `self.table_width` for each element in `self.strings`. For example, the loop would end up looking something like:

```
`strings_string += f"{'=' * 46}\n"
`strings_string += f"{'=' * 46}\n"
`strings_string += f"{'=' * 47}\n"
```