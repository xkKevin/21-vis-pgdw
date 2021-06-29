with open("1624862452.880091_exec.txt", "r") as fp1, open("1624862452.880091_exec copy.txt", "r") as fp2:
    fp1_lines = fp1.readlines()
    fp2_lines = fp2.readlines()
    print(fp1_lines[0])
    print(len(fp1_lines), len(fp2_lines))
    for i in range(len(fp1_lines)):
        if fp1_lines[i] != fp2_lines[i]:
            print(fp1_lines[i])
            print(fp2_lines[i])