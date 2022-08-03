import csv
import re
from surname_utils import _check

what = 'surname'
# what = 'patronymic'
# what = 'name'

# READ
p = '/mnt/hit4/hit4user/FIOsuggest/'+what+'/'+what+'_dadata_qc.csv'

li = []  # result
words = []  # used in loop

# dadata - 1) empty answer, 2) in answer another word 3) correct word but not equal gender
# 1) if dadata gender != our gender - we take dadata gender
# 2) if dadata gender == 'UNKNOWN' and qc = 0 - we take our gender
# 3) if dadata gender == 'UNKNOWN' and qc = 1 - we take our gender with caution
# 4) if dadata gender_our != gender_ddata and qc = 0 - we take dadata gender
# never happen 5) if dadata gender_our != gender_ddata and qc = 1 - we take dadata gender with caution
# 6) NAME - if dadata did not answer - we skip it
# 6) PATRONYMIC - if dadata did not answer and one word - we skip it else add origin ОГЛЫ/ОГЛУ/УЛЫ - М КЫЗЫ/ГЫЗЫ - Ж
# 6) SURNAME - if dadata did not answer - we add original 23) we take 'UNKNOWN' if not in 'pair'
PATRONYMIC = False
SURNAME = True

readed = []
with open(p, 'r') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in reader:
        readed.append(row)

readed = sorted(readed, key=lambda x: int(x[2]), reverse=True)  # sord by popularity

lumbering1 = []
# with open(p, 'r') as f:
#     reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
for i, row in enumerate(readed):
    w1 = row[0].upper()
    w2 = row[3].upper()
    gend1 = row[1]
    gend2 = row[4]
    qc = row[5]
    pop = row[2]
    if gend1 == 'Ж':
        gend1 = 'FEMALE'
    else:
        gend1 = 'MALE'

    # if not gend2:
    #     print(w1, w2)
    if w1 == w2:
        if gend1 == gend2:
            li.append((pop, w1, gend1))
            words.append(w1)
        elif gend2 == 'UNKNOWN' and qc == '0':  # 2)
            if SURNAME and (i < len(readed)-1 and len(readed[i+1]) == 7) or len(readed[i]) == 7:
                li.append((pop, w1, gend2))
                words.append(w1)
            else:
                li.append((pop, w1, gend2, gend2))
                words.append(w1)
        elif gend2 == 'UNKNOWN' and qc == '1':  # 3)
            if SURNAME and (i < len(readed)-1 and len(readed[i+1]) == 7) or len(readed[i]) == 7:
                _, _, gend2 = _check(w1)
                li.append((pop, w1, gend2))
                words.append(w1)
            else:
                li.append((pop, w1, gend1, 'achtung!'))
                words.append(w1)
        elif gend2 != '' and qc == '0':
            li.append((pop, w1, gend2))
            words.append(w1)
        # elif gend2 != '' and qc == '1': # never happen
        #     li.append((w1, gend2, ' ', 'wtf'))
        #     words.append(w1)
        else:  # w2 exist but empty gend2 and qc: ( never happen)
            print(pop,w1)
            if SURNAME:
                if qc == 1:
                    _, _, gend1 = _check(w1)
                if gend1 is None:
                    gend1 = 'UNKNOWN'
                li.append((pop, w1, gend1))
                words.append(w1)
            else:
                lumbering1.append((w1, gend1, 'BAD'))  # if in pair first was unknewn
    elif PATRONYMIC and w2 == '' and re.search("(ОГЛЫ|ОГЛУ|УЛЫ|УУЛУ)$", w1):  # Имя_отца + Сын/Дочь
        li.append((pop, w1, 'MALE'))  # save fixed word
        words.append(w1)
    elif PATRONYMIC and w2 == '' and re.search("(КЫЗЫ|ГЫЗЫ)$", w1):
        li.append((pop, w1, 'FEMALE'))  # save fixed word
        words.append(w1)
    elif w2 == '':
        li.append((pop, w1, gend1, 'BAD'))  # save fixed word
        words.append(w1)
    else: # lost
        print(row)

lumbering = [x for x in li if len(x) == 4 and x[3] == 'achtung!'] + lumbering1
lumbering2 = [x for x in li if len(x) == 4 and x[3] == 'BAD']

# SAVE without lumbering
p = '/mnt/hit4/hit4user/FIOsuggest/'+what+'/'+what+'_ddata.csv'
with open(p, 'w') as f:
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for x in li:
        if len(x) == 4 and x[3] == 'BAD':
            continue
        writer.writerow((x[1], x[2], x[0]))

p = '/mnt/hit4/hit4user/FIOsuggest/'+what+'/lumbering_ddata.csv'
with open(p, 'w') as f:
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for x in lumbering:
        writer.writerow(x)

p = '/mnt/hit4/hit4user/FIOsuggest/'+what+'/lumbering2_ddata.csv'
with open(p, 'w') as f:
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for x in lumbering2:
        writer.writerow(x)