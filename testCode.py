import time
import multiprocessing
from multiprocessing import Process, Manager
from functools import partial
from threading import Thread
from physicalEngine import *

#TEST`
if __name__ == "__main__":

    multiprocessing.freeze_support()

    FPS = 60 
    SCREEN_SIZE = (1920, 1080)

    a = AABB((4,40), (50,400), 1)
    b = AABB((2,3),(5,6), 1)
    c = Collision()
    print(c.AABBvsAABB(a,b))
    d = Circle((10,500), 40)
    e = Circle((2,4), 8)
    g = Triangle((2,3),(10,6), (15,3))
    print(c.CirclevsCircle(d,e))
    print(c.AABBvsCircle(a,d))
    print(c.AABBvsCircle(a,e))
    print(c.AABBvsCircle(b,d))
    print(c.AABBvsCircle(b,e))
    print(c.AABBvsTriangle(b,g))
    print("======init Finished=========")
    COUNT = 0
    m = 0
    startTime = time.time()
    for i in range(COUNT):
        if c.AABBvsTriangle(AABB1=AABB((i,i),(2*i+1,3*i+1), 0), Triangle1=Triangle((10, 10), (30,100),(50,10))):
            m += 1
    print(f"===========사각형,삼각형 충돌처리 걸린시간: {time.time()-startTime}=========")
    print(f"===========겹치는 사각형, 삼각형 개수: {m}=========================")

    p1 = Process(target=control, args=(0, COUNT//2,1))
    p2 = Process(target=control, args=(COUNT//2, COUNT, 2))
    print("===multiprocessingInit finished====")
    startTime = time.time()
    results = []
    
    p1.start()
    print("=====p1 started======")
    p2.start()
    p1.join()
    print("=====p1 joined======")
    p2.join()
    print(f"===========사각형 충돌처리-multi 걸린시간: {time.time()-startTime}=========")


    '''
    results = []
    m = 0
    startTime = time.time()
    for i in range(COUNT):
        if c.AABBvsAABB(AABB((i,i), (2*i+1, 5*i+1), 0), AABB((10, 100), (500, 600), 0)):
            m+= 1
    print(f"===========사각형 충돌처리-일반 걸린시간: {time.time()-startTime}=========")
    print(f"===========겹치는 사각형 개수: {m}=========================")

    startTime = time.time()
    th1 = Thread(target=control, args=(0, COUNT//2,1))
    th2 = Thread(target=control, args=(COUNT//2, COUNT, 2))
    th1.start()
    th2.start()
    th1.join()
    th2.join()
    procs = []

    for i in range(4):
        proc = Process(target=control, args=(COUNT,1))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    #pool = multiprocessing.Pool(processes=4)
    #argues = [(0, COUNT//4, 1), (COUNT//4, COUNT//2, 2), (COUNT//2, COUNT*3//2, 3), (COUNT*3//2, COUNT, 4)]
    #pool.map(control, argues)
    
    b = []
    startTime = time.time()
    for i in range(COUNT):
        b.append(c.CirclevsCircle(Circle1=Circle((i,i), 5), Circle2=Circle((10, 100), 600)))
    print(f"===========원 충돌처리-multi 걸린시간: {time.time()-startTime}=========")
    m = 0
    for i in range(len(b)):
        if b[i]:
            m += 1
    print(f"===========겹치는 원 개수: {m}=========================")
    '''
    
