'''
put passwords with the same length in a group (mark each group as a "potential group")

put ungrouped passwords in their own group (mark this group as a "wrong group")

for each "potential group"
    if the number of passwords in this group < number of websites used
        remove "potential group" mark from this group and mark this group as a "wrong group"

for each "potential group"
    add the first word of this group to its own group (mark this group as a "guessing group")
    for the rest of the words in this "potential group"
        if the current word matches with any of the words in any "guessing group"
            add the current word to that "guessing group"
        if the current word differs from all of the words in all of the "guessing groups"
            form a new "guessing group" with the current word

find the "guessing group" that has the same number of elements as the number of websites used
pick one password in this "guessing group"
replace * with letters from other passwords

(matches means ith character of both words are the same or the ith character of one of the words is a *)
(differs means ith character of both words are different)
'''

def group_intersection_attack(passwords, num_websites):
    potential_groups = {} # {password_length => [password1, password2, ...]}
    wrong_group = []
    guessing_groups = []

    for password in passwords:
        if len(password) in potential_groups:
            potential_groups[len(password)].append(password)
        else:
            potential_groups[len(password)] = [password]

    # print(potential_groups)

    to_delete = []
    for password_length, potential_group in potential_groups.items():
        if len(potential_group) < num_websites:
            wrong_group.append(potential_group)
            to_delete.append(password_length)

    for password_length in to_delete:
        del potential_groups[password_length]

    # print(potential_groups)
    # print(wrong_group)

    for password_length, potential_group in potential_groups.items():
        guessing_groups.append([potential_group[0]])
        for password in potential_group[1:]:
            match_found = False
            for guessing_group in guessing_groups:
                if all_characters_match(guessing_group, password):
                    match_found = True
                    guessing_group.append(password)
                    break
            if not match_found:
                guessing_groups.append([password])

    # print(guessing_groups)

    passwords = []
    for guessing_group in guessing_groups:
        if len(guessing_group) >= num_websites:
            passwords.append(intersect_passwords(guessing_group))

    return passwords

def all_characters_match(guessing_group, password):
    for p in guessing_group:
        if len(p) != len(password):
            return False
        for i in range(len(p)):
            if p[i] != '*' and password[i] != '*' and p[i] != password[i]:
                return False
    return True

def intersect_passwords(guessing_group):
    password = list(guessing_group[0])

    for p in guessing_group[1:]:
        for i in range(len(p)):
            if password[i] == '*':
                password[i] = p[i]

    return ''.join(password)

if __name__ == '__main__':
    while True:
        print('\n=============== BEGIN ATTACK ===============\n')

        while True:
            try:
                num_websites = int(input('Enter number of websites used: '))
                break
            except KeyboardInterrupt:
                exit()
            except:
                pass
        if num_websites <= 1:
            print("Don't use this script for 1 website, take a guess!")
            exit()

        while True:
            try:
                k = int(input('Enter k: '))
                break
            except KeyboardInterrupt:
                exit()
            except:
                pass

        passwords = []
        for i in range(num_websites):
            print(f'Enter passwords from site{i+1}:')
            for j in range(k):
                passwords.append(input(f'password {j+1}: '))

        print('-----------------------------------------')
        print(group_intersection_attack(passwords, num_websites))
        print('NOTE: due to the random placement of *, the password may not always be correct')

        if k > 1:
            print("Don't forget about the other passwords entered above. They may be helpful, even if they're not the correct password!")
