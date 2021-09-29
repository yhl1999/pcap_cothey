import time
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread

sleep_time = [1,2,1,1]
def aADDb(a,b,cnt):
    print(current_thread().getName())
    res = a[cnt]+b[cnt]
    a[cnt] = res
    return res

futureList = []

A = [[11,2,35,53]]
B = [[5,4,66,21]]
C = []

pool = ThreadPoolExecutor(10)

for i in range(0,4):
    futureList.append(pool.submit(aADDb,A[0],B[0],i))

for i in futureList:
    C.append(i.result())
print(A)
print(C)