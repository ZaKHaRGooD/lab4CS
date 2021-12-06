f_r = open('4dayMyself.yaml', 'r', encoding='utf-8')
f_w = open('4dayMyself.json', 'w', encoding='utf-8')
s = f_r.readlines()
new_string = ''
string = ''
f_w.write('{\n')  # ничего лучше, чем записать вручную открывающиюся фигурную скобку, я не придумал

count_format = 0
count_brace = 1

for i in range(len(s) - 1):
    space_count = 2  # количество пробелов в текущей строке
    space_count_next = 2  # считаем количество пробелов в следующей строке
    new_string = ''
    string = ''
    format_string = ''

    # считаем количество пробелов в текущей строке
    for t in range(len(s[i])):
        if s[i][t] != ' ':
            break
        space_count += 1
        if s[i] == 'timetable:':
            space_count = 2
            break

    # считаем количество пробелов в следующей строке
    for t in range(len(s[i + 1])):
        if s[i + 1][t] != ' ':
            break
        space_count_next += 1
    s[i] = s[i].strip()

    # находим ключ и записывам его значение в string
    for t in range(len(s[i])):
        if s[i][t] == ':':
            break
        string += s[i][t]

    # конвретируем ключ из yaml в json
    new_string = space_count * ' ' + '"' + string + '"'
    string += ':'

    # заменяем ключ в синтаксисе yaml на ключ в синтаксисе json
    if space_count != space_count_next or s[i] == 'timetable:':
        final_string = new_string + ': {'  # нужно для последующего удаления ключа из s[i]
        s[i] = s[i].replace(string, new_string + ': {')
        count_brace += 1  # считаю количество открывающихся фигурных скобок
    else:
        final_string = new_string + ':'  # нужно для последующего удаления ключа из s[i]
        s[i] = s[i].replace(string, new_string + ':')

    # заменяем ключ format в синтаксисе yaml на ключ format в синтаксисе json
    if '"format": {' in s[i]:
        final_string = space_count * ' ' + '"format":'

    # записываем получившийся ключ в синтаксисе json в файл
    f_w.write(final_string)

    print(s[i])
    # удаляю ключ из s[i], чтобы легче было конвертировать значение
    if '"format":' in s[i]:
        format_string = s[i].replace(new_string + ': ', '')
        count_format += 1  # подсчитываю количество ключей format, так как после последнего ключа format не должно быть запятой
    if space_count != space_count_next or s[i] == 'timetable:':
        s[i] = s[i].replace(new_string + ': {', '')
    else:
        s[i] = s[i].replace(new_string + ': ', '')

    string = s[i]
    print(string)
    # значение в синтаксисе yaml конвертируем в значение в синтаксисе json
    if format_string != '':
        new_string = string.replace(string, '"' + string + '"')
    else:
        new_string = string.replace(string, '"' + string + '",')

    # записываю в файл значение в формате json
    if new_string == '"",':
        f_w.write('\n')
    elif format_string != '' and count_format <= 2:
        f_w.write(' ' + new_string + '\n' + (space_count - 2) * ' ' + '},\n')
    elif format_string != '' and count_format == 3:  # после послежнего ключа format не должно быть запятой
        f_w.write(' ' + new_string + '\n' + (space_count - 2) * ' ' + '}\n')
    else:
        f_w.write(' ' + new_string + '\n')

count_brace -= count_format * 2
# записываю в файл закрывающиеся фигурные скобки
for i in range(count_brace - 1, -1, -1):
    f_w.write((2 * i * ' ') + '}\n')
# EOF
