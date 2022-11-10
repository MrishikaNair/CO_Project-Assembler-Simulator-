import matplotlib.pyplot as plt
import sys

from sys import stdin

reg_value = {'000': 0,
             '001': 0,
             '010': 0,
             '011': 0,
             '100': 0,
             '101': 0,
             '110': 0,
             '111': 0}

bin_input = sys.stdin.read()

bin_list = bin_input.split('\n')
for i in range(256 - len(bin_list)):
    bin_list.append('0000000000000000')

output_list = []
mem_plot = []
cycle_plot = []

i = 0
k = 0

while bin_list[i] != '1001100000000000':
    output_str = ''

    if (bin_list[i][:5] == '00000'):  # add
        reg_value['111'] = 0

        if ((reg_value[bin_list[i][10:13]] + reg_value[bin_list[i][13:16]]) < 2 ** 16):
            reg_value[bin_list[i][7:10]] = reg_value[bin_list[i][10:13]] + reg_value[bin_list[i][13:16]]
        else:
            reg_value['111'] = 8
            reg_value[bin_list[i][7:10]] = 2 ** 16 - 1

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1


    elif (bin_list[i][:5] == '00001'):  # sub
        reg_value['111'] = 0

        if ((reg_value[bin_list[i][10:13]] - reg_value[bin_list[i][13:16]]) >= 0):
            reg_value[bin_list[i][7:10]] = reg_value[bin_list[i][10:13]] - reg_value[bin_list[i][13:16]]
        else:
            reg_value['111'] = 8
            reg_value[bin_list[i][7:10]] = 0

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1



    elif (bin_list[i][:5] == '00010'):  # mov imm
        reg_value['111'] = 0
        reg_value[bin_list[i][5:8]] = int(bin_list[i][8:16], 2)

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1

    elif (bin_list[i][:5] == '00011'):  # mov reg
        reg_value[bin_list[i][10:13]] = reg_value[bin_list[i][13:16]]
        reg_value['111'] = 0
        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1

    elif (bin_list[i][:5] == '00100'):  # load
        reg_value['111'] = 0
        reg_value[bin_list[i][5:8]] = bin_list[int(bin_list[i][8:16], 2)]
        output_str += f'{i:08b} '

        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        plt.scatter(k, int(bin_list[i][8:16], 2))
        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1


    elif (bin_list[i][:5] == '00101'):  # store
        reg_value['111'] = 0
        bin_list[int(bin_list[i][8:16], 2)] = f'{reg_value[bin_list[i][5:8]]:016b}'
        output_str += f'{i:08b} '

        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        plt.scatter(k, int(bin_list[i][8:16], 2))
        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1

    elif (bin_list[i][:5] == '00110'):  # mul
        reg_value['111'] = 0

        if ((reg_value[bin_list[i][10:13]] * reg_value[bin_list[i][13:16]]) < 2 ** 16):
            reg_value[bin_list[i][7:10]] = reg_value[bin_list[i][10:13]] * reg_value[bin_list[i][13:16]]
        else:
            reg_value['111'] = 8
            reg_value[bin_list[i][7:10]] = 2 ** 16 - 1

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1

    elif (bin_list[i][:5] == '00111'):  # div
        reg_value['111'] = 0
        reg_value['000'] = int(bin_list[10:13], 2) // int(bin_list[13:16], 2)
        reg_value['001'] = int(bin_list[10:13], 2) % int(bin_list[13:16], 2)

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1


    elif (bin_list[i][:5] == '01000'):  # right shift
        reg_value['111'] = 0
        a = int(f'{reg_value[bin_list[i][5:8]]:08b}', 2)
        b = int(reg_value[bin_list[i][8:16]], 2)
        a = a >> b
        reg_value[bin_list[i][5:8]] = a

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1


    elif (bin_list[i][:5] == '01001'):  # left shift
        reg_value['111'] = 0

        a = int(f'{reg_value[bin_list[i][5:8]]:08b}', 2)
        b = int(reg_value[bin_list[i][8:16]], 2)
        a = a << b
        reg_value[bin_list[i][5:8]] = a

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1

    elif (bin_list[i][:5] == '01010'):  # exor
        reg_value['111'] = 0
        reg_value[bin_list[i][7:10]] = (int(f'{reg_value[bin_list[i][10:13]]:08b}', 2)) ^ (
            int(f'{reg_value[bin_list[i][13:16]]:08b}', 2))

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1


    elif (bin_list[i][:5] == '01011'):  # or
        reg_value['111'] = 0
        reg_value[bin_list[i][7:10]] = (int(f'{reg_value[bin_list[i][10:13]]:08b}', 2)) | (
            int(f'{reg_value[bin_list[i][13:16]]:08b}', 2))

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1


    elif (bin_list[i][:5] == '01100'):  # and
        reg_value['111'] = 0
        reg_value[bin_list[i][7:10]] = (int(f'{reg_value[bin_list[i][10:13]]:08b}', 2)) & (
            int(f'{reg_value[bin_list[i][13:16]]:08b}', 2))

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1


    elif (bin_list[i][:5] == '01101'):  # invert
        reg_value['111'] = 0
        reg_value[bin_list[i][10:13]] = ~(int(f'{reg_value[bin_list[i][13:16]]:08b}', 2))

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1

    elif (bin_list[i][:5] == '01110'):  # compare
        reg_value['111'] = 0
        if (reg_value[bin_list[i][10:13]] < reg_value[bin_list[i][13:16]]):
            reg_value['111'] = 4
        elif (reg_value[bin_list[i][10:13]] > reg_value[bin_list[i][13:16]]):
            reg_value['111'] = 2
        elif (reg_value[bin_list[i][10:13]] == reg_value[bin_list[i][13:16]]):
            reg_value['111'] = 1

        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        mem_plot.append(i)
        cycle_plot.append(k)
        i += 1
        k += 1



    elif (bin_list[i][:5] == '01111'):  # un_jump
        reg_value['111'] = 0
        output_str += f'{i:08b} '
        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '

        print(output_str)
        mem_plot.append(i)
        cycle_plot.append(k)
        i = int(bin_list[i][8:16], 2)
        k += 1

    elif (bin_list[i][:5] == '10000'):  # jlt
        output_str += f'{i:08b} '

        mem_plot.append(i)
        cycle_plot.append(k)
        if reg_value['111'] == 4:
            i = int(bin_list[i][8:16], 2)
        else:
            i += 1
        reg_value['111'] = 0

        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        k += 1


    elif (bin_list[i][:5] == '10001'):  # jgt
        output_str += f'{i:08b} '

        mem_plot.append(i)
        cycle_plot.append(k)
        if reg_value['111'] == 2:
            i = int(bin_list[i][8:16], 2)
        else:
            i += 1
        reg_value['111'] = 0

        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        k += 1


    elif (bin_list[i][:5] == '10010'):  # je
        output_str += f'{i:08b} '

        mem_plot.append(i)
        cycle_plot.append(k)
        if reg_value['111'] == 1:
            i = int(bin_list[i][8:16], 2)
        else:
            i += 1
        reg_value['111'] = 0

        for j in reg_value:
            output_str += f'{reg_value[j]:016b} '
        print(output_str)

        k += 1


if (bin_list[i][:5] == '10011'):  # hlt
    output_str = ''
    output_str += f'{i:08b} '
    for j in reg_value:
        output_str += f'{reg_value[j]:016b} '
    print(output_str)

    mem_plot.append(i)
    cycle_plot.append(k)
    i += 1
    k += 1


for l in bin_list:
    print(l)

plt.scatter(cycle_plot, mem_plot)
plt.show()

