def answer(xs):
    def mul(arr):
        if not arr:
            return 0
        return reduce(lambda x,y: x*y, arr)

    if len(xs) < 1 and len(xs) > 50:
        return 0

    original = len(xs)

    # remove values out of range and 0
    xs = filter(lambda x: abs(x) <= 1000 and x != 0, xs)

    p = []
    n = []
    for x in xs:
        if x > 0:
            p.append(x)
        else:
            n.append(x)

    p.sort(reverse=True)
    n.sort()

    # if the list of negative numbers is greater than 1 but odd, get rid of the last one
    if len(n) > 1 and len(n) % 2 == 1:
        n = n[:-1]

    if original > 1 and len(p)+len(n) == original:
        #print 'have to drop something'
        if mul(p) > mul(n):
            #print 'should drop from n'
            if len(n) < 1:
                #print 'nothing to drop on n'
                #print 'drop 1 from positive'
                p = p[:-1]
            else:
                #print 'drop 2 from negative'
                n = n[:-2]
        else:
            #print 'should drop from p'
            if len(p) < 1:
                #print 'nothing to drop on p'
                #print 'drop 2 from negative'
                n = n[:-2]
            else:
                #print 'drop 1 from positive'
                p = p[:-1]


    res = mul(p+n)
    if original > 1 and res < 0:
        res = 0

    return str(res)


assert answer([2, -3, 1, 0, -5]) == '30'
assert answer([2, 0, 2, 2, 0]) == '8'
assert answer([-2, -3, 4, -5]) == '60'

assert answer([1, 2, -1, -5]) == '10'
assert answer([]) == '0'
assert answer([1]) == '1'
assert answer([1, 1]) == '1'
assert answer([-1, -2, 3]) == '3'
assert answer([-2, -2, 3]) == '4'

assert answer([10, -50]) == '10'

assert answer([-2, -2, -2, -2]) == '4'
assert answer([2, 2, 2]) == '4'

assert answer([-10]) == '-10' # test 3
assert answer([0, 0, -43, 0]) == '0' # test 4
