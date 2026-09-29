import sys
file = sys.argv[1]
with open(file, 'r') as f:
    lines = f.readlines()
with open(file, 'w') as f:
    for line in lines:
        if line.startswith('pick '):
            f.write(line.replace('pick ', 'edit '))
        else:
            f.write(line)
