'''
i % 2 == 1 for half*
i % 3 == 0 for third
i % 4 == 0 for quarter
i % 4 != 0 for 3quarter

* to keep half and quarter lists distinct, either use (i % 2 == 1 and i % 4 == 0) or (i % 2 == 0 and i % 4 == 1)
'''

with open('rockyou_sorted_preprocessed.txt', encoding='utf-8') as f:
    lines = f.readlines()

    with open('rockyou_half_preprocessed.txt', 'a', encoding='utf-8') as w:
        i = 0
        for line in lines:
            if i % 2 == 1:
                w.write(line)
            i += 1
