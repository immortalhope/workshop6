import re
import plotly
import plotly.graph_objs as go

# Функція, що повертає потрібний елемент
def get_element(line):
    result = re.split(r",", line, maxsplit=1)
    element = result[0].strip()
    return element, result

# Функція, що повертає ID школи, що складається з шести цифр
def get_ID(line):
    result = re.split(r",", line, maxsplit=1)
    id = re.findall(r"\d{6}", result[0])
    return id, result

# Функція, що повертає назву школи
def get_name(line):
    for elm in line:
        if elm[0] == '"':
            result = re.split(r'"', str(line), maxsplit=2)
            name = result[1].strip()
            return name, result
        else:
            name, line = get_element(str(line))
            return name[2:], line

# Функція, що повертає повну назву школи.
def get_full_name(line):
    for elm in line:
        if elm[0] == '"':
            result = re.split(r'"', str(line), maxsplit=2)
            f_name = result[1].strip()
            return f_name, result
        else:
            f_name, line = get_element(str(line))
            return f_name[2:], line

# Функція, що повертає повторну назву школи.
def get_name2(line):
    for elm in line:
        if elm[0] == '"':
            result = re.split(r'"', str(line), maxsplit=2)
            name_2 = result[1].strip()
            return name_2, result
        else:
            name_2, line = get_element(str(line))
            return name_2[2:], line

# Creating the dictionary.
dataset = dict()
try:
    # Opening of the file.
    with open("D:\\workshop6\\schools.csv", encoding="utf-8", mode="r") as file:
        # Marking out of the first line with names of columns.
        header = file.readline()
        header = [word.strip() for word in header.split(",")]
        line_number = 1
        # Going through lines in file.
        for line in file:
            line = line.strip().rstrip()
            line_number += 1
            # With functions, program gets the first 4 columns from the file,
            # and add them into our dataset.
            if not line:
                continue
            school_id, line = get_ID(line)
            tail = line[1:]
            school_name, tail = get_name(tail)
            tail_1 = tail[1:]
            full_name, tail_1 = get_full_name(tail_1)
            tail_2 = tail_1[1:]
            second_name, tail_2 = get_name2(tail_2)
            # Defining key and Value of dataset.
            key = str(school_id)[2:-2]
            value = {header[1]: school_name, header[2]: full_name}
            # print(value)
            data = {key: value}
            dataset.update(data)
    print(dataset)

    # Counting the number of high, middle, elementary schools and academies.
    high_schools = 0
    elementary_schools = 0
    middle_schools = 0
    academies = 0
    schools = 0
    school_variaty = ['High Schools', 'Elementary Schools', 'Middle Schools', 'Academies']
    school_variaty_num = []
    for values in dataset.values():
        for elm in values.values():
            list_with_elm = elm.split(" ")
            for word in list_with_elm:
                if re.match(r"High", word):
                    elementary_schools += 1
                elif re.match(r"Elementary", word):
                    high_schools += 1
                elif re.match(r"Middle", word):
                    middle_schools += 1
                elif re.match(r"Academy", word):
                    academies += 1
                elif re.match(r"School", word):
                    schools += 1
    school_variaty_num.append(high_schools)
    school_variaty_num.append(elementary_schools)
    school_variaty_num.append(middle_schools)
    school_variaty_num.append(academies)
    # print(high_schools, elementary_schools, middle_schools, academies)
    # building a bar for the amount of high, middle, elementary schools and academies.
    bar = go.Bar(x=school_variaty,
                 y=school_variaty_num)
    plotly.offline.plot([bar])

    # Pie with amount of schools that have first num of ID 4 or 6.
    amount_6 = 0
    amount_4 = 0
    for keys in dataset:
        for elm in keys:
            if elm[0] == '6':
                amount_6 += 1
            elif elm[0] == '4':
                amount_4 += 1
    list_with_amount = []
    list_with_amount.append(amount_6)
    list_with_amount.append(amount_4)
    list_for_pie = ["ID with first number 6", "ID with first number 4"]
    pie = go.Pie(labels = list_for_pie,
                 values = list_with_amount)
    plotly.offline.plot([pie])

    list_for_pie2 = ["Schools", "Academies"]
    list_with_amount1 = []
    list_with_amount1.append(schools)
    list_with_amount1.append(academies)
    pie2 = go.Pie(labels = list_for_pie2,
                  values = list_with_amount1)
    plotly.offline.plot([pie2])


except IOError as e:
   print("I/O error({0}): {1}".format(e.errno, e.strerror))

except ValueError as ve:
    print("Value error {0} in line {1}".format(ve, line_number))
