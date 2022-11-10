import sys

from sys import stdin

reg_dict = {'R0': '000',
            'R1': '001',
            'R2': '010',
            'R3': '011',
            'R4': '100',
            'R5': '101',
            'R6': '110',
            'FLAGS': '111'}


complete_input = sys.stdin.read()

label_mem = {}

output_list = []

var_list = []


def reg_typos(line_split):
    for i in line_split:
        if i not in reg_dict.keys():
            output_list.append("Illegal register names")
            return True

    return False


def ill_imm(line_split):
    for i in line_split[1:]:
        if i[0] == '$':
            if 0 > int(i[1:]) or int(i[1:]) > 255:
                output_list.append("Illegal immediate values")
                return True
    return False


def FLAGS_error(line_split):
    if (line_split[0] != 'mov') and ('FLAGS' in line_split):
        output_list.append('Illegal use of FLAGS register')
        return True

    elif (line_split[0] == 'mov') and ('FLAGS' in line_split[0:2]):
        output_list.append('Illegal use of FLAGS register')
        return True

    return False


def undefined_var(str):
    if (str not in var_list):
        output_list.append("Use of undefined variable")
        return True


def undefined_label(str):
    if (str not in label_mem):
        output_list.append("Use of undefined label")
        return True

    return False


ins_list = complete_input.split('\n')

var_check = 0
error_check = 0

for i,line in enumerate(ins_list):

    ins_list[i] = line.lstrip().rstrip()
    line_split = ins_list[i].split(' ')

    if line_split[0] != 'var':
        var_check = 1

    if line_split[0] == 'var':
        if var_check == 1:
            output_list.append("Variables not declared at the beginning")
            error_check = 1
            break
        if len(line_split) == 2:
            var_list.append(line_split[1])
        else:
            output_list.append('General Syntax Error')
            error_check = 1
            break

ins_list = [i for i in ins_list if i != '']
ins_list = [i for i in ins_list if i.split()[0] != 'var']


if error_check == 0:
    hlt_check = 0
    for line in ins_list:
        if 'hlt' in line:
          hlt_check = 1
          if ins_list.index(line) !=  len(ins_list)-1:
            output_list.append('hlt not being used as the last instruction')
            error_check = 1
            break
    if hlt_check == 0:
        output_list.append('Missing hlt instruction')
        error_check = 1  




if error_check == 0:

    for addr, line in enumerate(ins_list):
        line_split = line.split(' ')
        if line_split[0][-1] == ':':
            label_mem[line_split[0][:-1]] = f'{addr:08b}'


    for line in ins_list:

        line_split = line.split(' ')

        if line_split[0][-1] == ':':
            line_split.remove(line_split[0])

        if line_split[0] == 'add':
            if len(line_split) != 4:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos(line_split[1:]):
                break

            output_list.append(
                '00000' + '00' + reg_dict[line_split[1]] + reg_dict[line_split[2]] + reg_dict[line_split[3]])

        elif line_split[0] == 'sub':
            if len(line_split) != 4:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos(line_split[1:]):
                break

            output_list.append(
                '00001' + '00' + reg_dict[line_split[1]] + reg_dict[line_split[2]] + reg_dict[line_split[3]])

        elif line_split[0] == 'mov':
            if len(line_split) != 3:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos([line_split[1]]):
                break
            if line_split[2][0] == '$':
                if ill_imm(line_split):
                    break
                a = int(line_split[2][1:])
                output_list.append('00010' + reg_dict[line_split[1]] + f'{a:08b}')

            elif reg_typos([line_split[2]]):
                break
            else:
                output_list.append('00011' +'00000' + reg_dict[line_split[1]] + reg_dict[line_split[2]])


        elif line_split[0] == 'ld':
            if len(line_split) != 3:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos([line_split[1]]):
                break
            if (line_split[2] in label_mem):
                output_list.append('Misuse of label as variable')
                break
            if undefined_var(line_split[2]):
                break

            a = len(ins_list) + var_list.index(line_split[2])
            output_list.append('00100' + reg_dict[line_split[1]] + f'{a:08b}')


        elif line_split[0] == 'st':
            if len(line_split) != 3:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos([line_split[1]]):
                break
            if (line_split[2] in label_mem):
                output_list.append('Misuse of label as variable')
                break
            if undefined_var(line_split[2]):
                break

            a = len(ins_list) + var_list.index(line_split[2])
            output_list.append('00101' + reg_dict[line_split[1]] + f'{a:08b}')


        elif line_split[0] == 'mul':
            if len(line_split) != 4:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos(line_split[1:]):
                break

            output_list.append(
                '00110' + '00' + reg_dict[line_split[1]] + reg_dict[line_split[2]] + reg_dict[line_split[3]])


        elif (line_split[0] == 'div'):
            if len(line_split) != 3:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos(line_split[1:]):
                break
            output_list.append('00111' + '00000' + reg_dict[line_split[1]] + reg_dict[line_split[2]])


        elif (line_split[0] == 'rs'):
            if len(line_split) != 3:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos([line_split[1]]):
                break
            if ill_imm(line_split):
                break
            a = int(line_split[2][1:])
            output_list.append('01000' + reg_dict[line_split[1]] + f'{a:08b}')

        elif (line_split[0] == 'ls'):
            if len(line_split) != 3:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos([line_split[1]]):
                break
            if ill_imm(line_split):
                break
            a = int(line_split[2][1:])
            output_list.append('01001' + reg_dict[line_split[1]] + f'{a:08b}')

        elif (line_split[0] == 'xor'):
            if len(line_split) != 4:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos(line_split[1:]):
                break
            output_list.append('01010' + '00' + reg_dict[line_split[1]] + reg_dict[line_split[2]] + reg_dict[line_split[3]])

        elif (line_split[0] == 'or'):
            if len(line_split) != 4:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos(line_split[1:]):
                break
            output_list.append('01011' + '00' + reg_dict[line_split[1]] + reg_dict[line_split[2]] + reg_dict[
                line_split[3]])

        elif (line_split[0] == 'and'):
            if len(line_split) != 4:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos(line_split[1:]):
                break
            output_list.append('01100' + '00' + reg_dict[line_split[1]] + reg_dict[line_split[2]] + reg_dict[
                line_split[3]])

        elif (line_split[0] == 'not'):
            if len(line_split) != 3:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos(line_split[1:]):
                break
            output_list.append('01101' + '00000' + reg_dict[line_split[1]] + reg_dict[line_split[2]])

        elif (line_split[0] == 'cmp'):
            if len(line_split) != 3:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if reg_typos(line_split[1:]):
                break
            output_list.append('01110' + '00000' + reg_dict[line_split[1]] + reg_dict[line_split[2]])

        elif (line_split[0] == 'jmp'):
            if len(line_split) != 2:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if (line_split[1] in var_list):
                output_list.append('Misuse of variable as label')
                break
            if undefined_label(line_split[1]):
                break
            if line_split[1] in label_mem:
                output_list.append("01111" + "000" + label_mem[line_split[1]])

        elif (line_split[0] == 'jlt'):
            if len(line_split) != 2:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if (line_split[1] in var_list):
                output_list.append('Misuse of variable as label')       #changed misuse of label as variable in jump instructions
                break
            if undefined_label(line_split[1]):
                break
            if line_split[1] in label_mem:
                output_list.append('10000' + '000' + label_mem[line_split[1]])

        elif (line_split[0] == 'jgt'):
            if len(line_split) != 2:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if (line_split[1] in var_list):
                output_list.append('Misuse of variable as label')        
                break
            if undefined_label(line_split[1]):
                break
            if line_split[1] in label_mem:
                output_list.append("10001" + "000" + label_mem[line_split[1]])

        elif (line_split[0] == 'je'):
            if len(line_split) != 2:
                output_list.append('General Syntax Error')
                break
            if FLAGS_error(line_split):
                break
            if (line_split[1] in var_list):
                output_list.append('Misuse of variable as label')
                break
            if undefined_label(line_split[1]):
                break
            if line_split[1] in label_mem:
                output_list.append('10010' + '000' + label_mem[line_split[1]])

        elif (line_split[0] == 'hlt'):
            output_list.append('10011' + '00000000000')


        else:
            output_list.append("Typos in instruction name")
            break

for i in output_list:
    print(i)





