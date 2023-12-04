import csv

file_path = "./input/input.txt"

with open(file_path) as f:
    reader = csv.reader(f)
    data = list(reader)

print(data)

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

        
