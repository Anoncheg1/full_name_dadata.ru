import urllib.request
from urllib.error import URLError
import json
import csv
import time
from time import sleep
import socks
import socket
# own
from surname_utils import ispars, _check

SURNAME = True

API_KEY = ['f670813c14f672c1e197101fd767cbe675933d86',
           '5ac89f480b95a0b3106c198b4f69b2ec3ba97a41',
           '56a28ea26d7875662ea2f9734ca9c9ac9b32e709',
           'dc0133a4f244838588d1861e6f54ef1ec47daef7',
           'afe000cb6cc57f29ae9b24ff0fc844027bf1d4ce',  # sivtsev_si@bel-rusnarbank.ru masha123
           '9958b2293c6deb9b46a9577886f7592ebe2530f2']  # bozhko_mp@bel-rusnarbank.ru
headers = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5',
           'Content-Type': 'application/json',
           'Accept': 'application/json',
           'Authorization': None
           }

saved_socket = socket.socket

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 8888)
replace_socket = [saved_socket, socks.socksocket]


def que(word, idx: int):
    """
    https://dadata.ru/api/suggest/name/
    https://dadata.ru/api/clean/
    """

    socket.socket = replace_socket[idx % 2]  # change proxy by socket

    # NAME PATRONYMIC SURNAME
    data = '{ "query": "' + word + '", "count": 3, "parts": ["SURNAME"] }'
    headers['Authorization'] = 'Token ' + API_KEY[idx % 6]  # change APIKEY 1 2 1 2 1 2 1 2
    req = urllib.request.Request(url='https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/fio',
                                 headers=headers, data=data.encode())

    with urllib.request.urlopen(req) as f:
        r = f.read().decode('utf-8')
        print(r)
        j = json.loads(r)
        # j2 = json.dumps(j, ensure_ascii=False, indent=4)
        # print(j2)
        sug = None
        if len(j['suggestions']) > 0:
            for s in j['suggestions']:
                if s["unrestricted_value"].upper() == word:
                    sug = s
        elif len(j['suggestions']) == 1:
            sug = j['suggestions'][0]

        if sug is not None:
            ret_word = sug["unrestricted_value"].upper()
            gender = sug["data"]["gender"]  # UNKNOWN / MALE / FEMALE
            qc = sug["data"]["qc"]  # 0, 1
            return ret_word, gender, qc

    return None, None, None


def que_a(w, ii):
    try:
        res = que(w, ii)  # request to DADATA!!
        return res
    except URLError as e:
        print(e)
        return None

# print(que('ВАСЯ'))

p_w = '/home/u2/Desktop/surnames_dadata_qc.csv'
p_r = '/home/u2/Desktop/surnames_sorted.csv'

readed = []
with open(p_r, 'r') as fr:
    reader = csv.reader(fr, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in reader:
        readed.append(tuple(row))

res = None
with open(p_w, 'a') as fw:
    writer = csv.writer(fw, delimiter=',', quoting=csv.QUOTE_NONE)
    for i, row in enumerate(readed):
        if i < 253135:  # ФАХРИУЛЛИНА
            continue
        if SURNAME and ((i >= 1 and ispars(readed[i - 1][0], readed[i][0]))
                        or (i < len(readed)-1 and ispars(readed[i][0], readed[i+1][0]))) and res:
            # do not query dadata
            g = _check(readed[i][0])[2]
            res = (readed[i][0], g, g, 'pair')  # g g - ?
        else:
            for _ in range(99999):
                for x in range(len(API_KEY)):
                    res = que_a(row[0], i+x)  # retry
                    if res:
                        break
                    # else:
                    #     sleep(1)
                if res:
                    break
                else:
                    sleep(10)
            time.sleep(0.5)  # between requests

        if res is not None:
            writer = csv.writer(fw, delimiter=',', quoting=csv.QUOTE_NONE)
            respon = row + res
            print(i, respon)
            writer.writerow(respon)

