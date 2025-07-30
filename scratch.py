from pathlib import Path

directory_path = Path("/path/to/directory")
for item in directory_path.iterdir():
    print(item.name)
