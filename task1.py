f_r = open('4dayMyself.yaml', 'r', encoding='utf-8')
f_w = open('4dayMyself.json', 'w', encoding='utf-8')
s = f_r.readlines()
new_string = ''
string = ''
f_w.write('{\n')
for i in range(len(s)-1):
    i += 1
    new_string = ''
    string = ''
    t = 0
    space_count = 2
    if s[i].count(':') == 1:
        s[i] = s[i].replace(':', ': {')

    while s[i][t] == ' ':
        space_count += 1
        t += 1
        if s[i][t] == ':':
            break

    s[i] = s[i].strip()
    t = 0

    for t in range(len(s[i])):
        if s[i][t] == ':':
            break
        string += s[i][t]
        t += 1

    new_string = (space_count * ' ') + '"' + string + '"'
    s[i] = s[i].replace(string, new_string)

    f_w.write(s[i] + '\n')


