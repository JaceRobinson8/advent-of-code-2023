from pathlib import Path
from common.utils import parse_input

file_path = Path("./days/day 1/challenge 1/input/input.txt")

data = parse_input(file_path)

res = []
for id, val in enumerate(data):
    my_string = val[0]
    first = "0"
    last = "0"
    first_digit = True
    for id_inner, val_inner in enumerate(my_string):
        print(id_inner)
        print(val_inner)
        if val_inner.isdigit():
            if first_digit:
                first = val_inner
                first_digit = False
            last = val_inner
    res.append(int(first + last))

print(res)

sum = 0
for val in res:
    sum += val

print(sum)
