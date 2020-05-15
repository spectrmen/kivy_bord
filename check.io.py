from typing import List

def dfs(start, finish, mas, sum, summ):
    for t, c in mas.pop(start):
        if t == finish:
            summ.append(sum + c)
            continue
        else:
            if t not in mas.keys():
                s = sum + c #i hate the shit
                dfs(t,finish,mas,s, summ)
    return summ
def cheapest_flight(costs: List, a: str, b: str) -> int:
    v = {}
    summ = []
    for z,x,y in costs:
        try:
            v[z][0].append(x)
            v[z][1].append(y)

        except:
            v[z] = {0:[x], 1:[y]}
        try:
            v[x][0].append(z)
            v[x][1].append(y)
        except:
            v[x] = {0:[z],1:[y]}
    try:
        return min(dfs(a,b,v,0,summ))
    except:
        return 0


if __name__ == '__main__':
    print("Example:")
    print(cheapest_flight([['A', 'C', 100],
  ['A', 'B', 20],
  ['B', 'C', 50]],
 'A',
 'C'))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert cheapest_flight([['A', 'C', 100],
  ['A', 'B', 20],
  ['B', 'C', 50]],
 'A',
 'C') == 70
    assert cheapest_flight([['A', 'C', 100],
  ['A', 'B', 20],
  ['B', 'C', 50]],
 'C',
 'A') == 70
    assert cheapest_flight([['A', 'C', 40],
  ['A', 'B', 20],
  ['A', 'D', 20],
  ['B', 'C', 50],
  ['D', 'C', 70]],
 'D',
 'C') == 60
    assert cheapest_flight([['A', 'C', 100],
  ['A', 'B', 20],
  ['D', 'F', 900]],
 'A',
 'F') == 0
    assert cheapest_flight([['A', 'B', 10],
  ['A', 'C', 15],
  ['B', 'D', 15],
  ['C', 'D', 10]],
 'A',
 'D') == 25
    print("Coding complete? Click 'Check' to earn cool rewards!")
