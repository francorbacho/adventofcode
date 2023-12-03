# this just processes the data, you can use unix tools after to find the
# solutions to both parts.

def main():
    with open('input.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    current = 0
    for line in lines:
        if line == "":
            print(current)
            current = 0
            continue
        current += int(line)

if __name__ == '__main__':
    main()
