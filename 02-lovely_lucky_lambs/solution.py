def answer(total_lambs):
    if total_lambs < 10 or total_lambs > 10**9:
        return 0

    stingy = [1]
    generous = [1]
    total_lambs -= 1

    l = total_lambs
    while l > 0:
        new = sum(stingy[-2:])
        stingy.append(new)
        l -= new
    if l < 0:
        stingy.pop()
    print(stingy)

    l = total_lambs
    while l > 0:
        new = generous[-1]*2
        generous.append(new)
        l -= new
    if l < 0:
        l += generous.pop()
        if l >= sum(generous[-2:]):
            generous.append(sum(generous[-2:]))

    return len(stingy)-len(generous)
