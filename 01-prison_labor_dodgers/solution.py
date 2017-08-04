def answer(x,y):
    if len(x) > len(y):
        big = x
        small = y
    else:
        big = y
        small = x

    uniques = [i for i in big if i not in small]
    return uniques[0]
