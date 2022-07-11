with open('rockyou_sorted_preprocessed.txt', encoding='utf-8') as f:
    lines = f.readlines()

    with open('rockyou_quarter_preprocessed.txt', 'a', encoding='utf-8') as w:
        i = 0
        for line in lines:
            if i % 4 == 0:
                w.write(line)
            i += 1

