'''
i % 2 == 0 for half
i % 3 == 0 for third
i % 4 == 0 for quarter
i % 4 != 0 for 3quarter
'''

with open('rockyou_sorted_preprocessed.txt', encoding='utf-8') as f:
    lines = f.readlines()

    with open('rockyou_quarter_preprocessed.txt', 'a', encoding='utf-8') as w:
        i = 0
        for line in lines:
            if i % 4 == 0:
                w.write(line)
            i += 1

