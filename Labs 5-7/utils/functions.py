import re


def is_constant(token):
    return re.match(r'^(0|[+-]?[1-9][0-9]*)$|^(0|[+-]?[1-9][0-9]*),[0-9]*|^`.`$|^`.*`$', token) is not None


def is_string_constant(token):
    return re.match(r"^'.'$|^'.*'$", token) is not None


def read_seq(file_name):
    sequence = []
    file = open(file_name, 'r')
    lines = file.readlines()

    for line in lines:
        sequence.append(line.strip())
    return sequence


def read_pif(filename):
    sequence = []
    with open(filename, 'r') as file:
        for line in file:
            elem = line.split(":")[0].strip()
            type = line.split(",")[-1].strip()
            if type == '0':
                if is_string_constant(elem):
                    sequence.append('string')
                elif is_constant(elem):
                    sequence.append('integer')
                else:
                    sequence.append('constant')
            elif type == '1':
                sequence.append('identifier')
            else:
                sequence.append(elem)
    print("Sequence from PIF: ", sequence)
    return sequence