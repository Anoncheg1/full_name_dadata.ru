import csv
import re
# READ

se = set()
li = []
popularity = dict()


def setto(w, g, n):
    if w in popularity.keys():
        if popularity[w] < n:
            popularity[w] = n
            se.add((w, g))
    else:
        popularity[w] = n
        se.add((w, g))


p = '/home/u2/Desktop/FIO_NER/И.csv'
# p = '/home/u2/Desktop/FIO_NER/О.csv'
# p = '/home/u2/Desktop/FIO_NER/Ф.csv'
with open(p, 'r') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in reader:
        setto(w=row[0].upper().strip(),
              g=row[1],
              n=round(int(row[2])*321.59 - 961.777))  # по уравнению прямой x1= 3 y1= 3 x2= 2027 y2= 650906


p = '/home/u2/Desktop/result/I.csv'
# p = '/home/u2/Desktop/result/O.csv'
# p = '/home/u2/Desktop/result/F.csv'
with open(p, 'r') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for i, row in enumerate(reader):
        if i == 0:
            continue  # skip first line
        setto(w=row[1].upper().strip(),
              g=row[2],
              n=int(row[3]))

li = sorted(list(se), key=lambda x: x[0])

# save conflicts
conflict = [x for i, x in enumerate(li) if i >= 1 and (li[i - 1][0] == li[i][0])]
# print(conflict)
# filter
reo = re.compile(r'^[А-Я\- ]*$')
li = [x for i, x in enumerate(li) if i >= 1 and (li[i - 1][0] != li[i][0])
      and reo.fullmatch(li[i][0]) and len(li[i][0]) > 1 and li[i][0] != '--' and li[i][0] != '---']
# conflict2 = [x for i, x in enumerate(li) if i >= 1 and (li[i - 1][0] == li[i][0])]
# print(conflict2)
li = [(x[0], x[1], popularity[x[0]]) for x in li]
li = sorted(li, key=lambda x: x[2], reverse=True)
print("result", len(li), li)



# # SAVE
# p = '/home/u2/Desktop/names.csv'
# with open(p, 'w') as f:
#     writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
#     for x in li:
#         writer.writerow(x)
#
# # SAVE
# p = '/home/u2/Desktop/conflicts.csv'
# with open(p, 'w') as f:
#     writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
#     for x in conflict:
#         writer.writerow(x)





# print("wtf")
# p = sorted(list(popularity.items()), key=lambda x: x[1], reverse=True)
# print("popularity", popularity['ЕЛЕНА'])