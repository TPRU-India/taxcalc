import decimal


def curr_ind(n):
    """ Convert a number (int / float) into indian formatting style """
    d = decimal.Decimal(str(n))

    if d.as_tuple().exponent < -2:
        s = str(n)
    else:
        s = '{0:.2f}'.format(n)

    i = len(s) - 1

    res, flag, k = '', 0, 0
    while i >= 0:
        if flag == 0:
            res += s[i]
            if s[i] == '.':
                flag = 1
        elif flag == 1:
            k += 1
            res += s[i]
            if k == 3 and i - 1 >= 0:
                res += ','
                flag = 2
                k = 0
        else:
            k += 1
            res += s[i]
            if k == 2 and i - 1 >= 0:
                res += ','
                flag = 2
                k = 0
        i -= 1

    return res[::-1]
