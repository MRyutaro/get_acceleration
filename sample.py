a = ['0.01,-0.00,1.07,3.16,1.01,-1.08', '0.00,0.00,1.07,2.99,0.96,-1.14']
float_line = list()

for i in range(len(a)):
    line_disp = a[i].split(',')
    print(f"l={line_disp}")
    # print(type(l[0]))

    tmp_float_l = list()
    for j in range(6):
        tmp_float_l.append(float(line_disp[j]))

    print(f"tmp_float_l={tmp_float_l}\n")
    float_line.append(tmp_float_l)
