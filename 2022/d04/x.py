def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    first_count = 0
    second_count = 0
    for line in lines:
        [first, second] = line.split(',')
        firstStart, firstEnd = tuple(map(int, first.split('-')))
        secondStart, secondEnd = tuple(map(int, second.split('-')))

        overlap = False
        overlap |= firstStart <= secondStart and secondEnd <= firstEnd
        overlap |= secondStart <= firstStart and firstEnd <= secondEnd

        if overlap:
            first_count += 1

        # 5-10,6-10
        overlap |= firstStart <= secondStart <= firstEnd or firstStart <= secondEnd <= firstEnd
        overlap |= secondStart <= firstStart <= secondEnd or secondStart <= firstEnd <= secondEnd

        if overlap:
            second_count += 1

    print(first_count)
    print(second_count)

main()
