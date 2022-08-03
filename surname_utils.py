import re

# http://gramma.ru/SPR/?id=2.6
okon_m = ['ОВ', 'ЕВ', 'ИН', 'ЫН', 'ОЙ', 'ИЙ',
          'СКОЙ', 'СКИЙ',
          'ЦКОЙ', 'ЦКИЙ']
okon_f = ['ОВА', 'ЕВА', 'ИНА', 'ЫНА', 'АЯ', 'ЯЯ',
          'СКАЯ',
          'ЦКАЯ']

turs_m = ('ОГЛЫ', 'ОГЛУ', 'УЛЫ', 'УУЛУ')
turs_f = ('КЫЗЫ', 'ГЫЗЫ')

# okon_m = r'(ОВ|ЕВ|ИН|ЫН|ОЙ|ИЙ|СКОЙ|СКИЙ|ЦКОЙ|ЦКИЙ)$'
# okon_f = r'(ОВА|ЕВА|ИНА|ЫНА|АЯ|ЯЯ|СКАЯ|ЦКАЯ)$'


def _check(word) -> (int, str, str):
    match = None
    for i, x in enumerate(okon_m):
        match = re.search('(' + x + ')$', word)
        if match:
            span = match.span()
            return i, word[:span[0]], 'MALE'
    if match is None:
        for i, x in enumerate(okon_f):
            match = re.search('(' + x + ')$', word)
            if match:
                span = match.span()
                return i, word[:span[0]], 'FEMALE'

    return None, None, None

    # match = re.search(okon_m, word)
    # if match:
    #     span = match.span()
    #     return word[:span[0]], 'MALE'
    # else:
    #     match = re.search(okon_f, word)
    #     if match:
    #         span = match.span()
    #         return word[:span[0]], 'FEMALE'
    #
    # return None, None


def ispars(w1: str, w2: str):
    w1_id, w1_s, w1_g = _check(w1)
    w2_id, w2_s, w2_g = _check(w2)
    if w1_s and w2_s and w1_s == w2_s:
        if w1_g == 'MALE' and ((w1_id == w2_id and w1_id <= 4)
                               or ((w2_id == 4 or w2_id == 5) and w1_id == 5)
                               or ((w1_id == 6 or w1_id == 7) and w2_id == 6)
                               or ((w1_id == 8 or w1_id == 8) and w2_id == 7)):
            return True
        elif w1_g == 'FEMALE' and ((w1_id == w2_id and w1_id <= 4)
                                   or ((w1_id == 4 or w1_id == 5) and w2_id == 5)
                                   or ((w2_id == 6 or w2_id == 7) and w1_id == 6)
                                   or ((w2_id == 8 or w2_id == 8) and w1_id == 7)):
            return True

    return False

print(ispars('БУРОВИЦКИЙ', 'БУРОВИЦКАЯ'))