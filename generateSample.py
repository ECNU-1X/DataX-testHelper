import random

with open("100M.txt", "w", encoding="utf-8") as fw:
    for i in range(1,100000001):
        str_list = [chr(i) for i in range(97,123)]   #a-z
        string = ''.join(random.sample(str_list, 15))
        fw.write(",".join([str(i), string, str(i*0.1)]) + "\n")



