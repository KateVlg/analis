import csv
with open('/home/student/tomita-parser/build/bin/input.txt', "w") as my_output_file:
    with open('news_docs.csv', "r") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            [my_output_file.write(''.join(line[4])+'\n') for line in csv.reader(f)]
    f.close()