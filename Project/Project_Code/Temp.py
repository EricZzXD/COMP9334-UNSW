temp_output_sub_job_departure = [['1.0', '2.8'],
                                 ['6.0', '8.1'],
                                 ['5.0', '8.9'],
                                 ['3.0', '9.1'],
                                 ['7.0', '10.0'],
                                 ['3.0', '11.0'],
                                 ['6.0', '12.0'],
                                 ['9.0', '12.9'],
                                 ['8.0', '15.0'],
                                 ['8.0', '15.1']]

# temp_list = []
#
# for i in range(0, len(temp_output_sub_job_departure) - 1):
#     bigest = temp_output_sub_job_departure[i][2]
#     count_true = True
#     for j in range(0, len(temp_output_sub_job_departure)):
#         if (temp_output_sub_job_departure[i][0][0] ==
#             temp_output_sub_job_departure[len(temp_output_sub_job_departure) - j - 1][0][0]) and count_true:
#             temp_list.append(float(temp_output_sub_job_departure[j][2]) - float(temp_output_sub_job_departure[j][1]))
#             print(temp_output_sub_job_departure[i][0])
#             count_true = False
#
# print(temp_list)

list = [[1, 2], [1, 3], [2, 1], [2, 2], [3, 5]]
myDic = {}
output_response_time = 0

for i in temp_output_sub_job_departure:
    if i[0] not in myDic:
        myDic[i[0]] = i
    else:
        if float(myDic[i[0]][1]) < float(i[1]):
            myDic[i[0]] = i

for i in myDic:
    output_response_time = round(output_response_time + round(float(myDic[i][1]) - float(myDic[i][0]), 4), 4)

print(output_response_time)
# output = []
# for i in myDic:
#     output.append(myDic[i])
# print(output)
#
# final = 0
# for i in output:
#     final = final + round(float(i[1]) - float(i[0]), 4)

# print(final)
