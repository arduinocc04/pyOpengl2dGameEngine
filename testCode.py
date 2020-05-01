import time
import physicalEngine

def collision(p, moveableObj, possibleStaticObjList):
    startTime = time.time()
    for staticObj in possibleStaticObjList:
        if type(moveableObj) is physicalEngine.Group:
            p.GroupvsObj(moveableObj, staticObj)
        else:
            if type(staticObj) is physicalEngine.Circle:
                if type(moveableObj) is physicalEngine.Circle:
                    p.CirclevsCircle(staticObj, moveableObj)
                else:
                    p.PolyvsCircle(moveableObj, staticObj)
            else:
                if type(moveableObj) is physicalEngine.Circle:
                    p.PolyvsCircle(staticObj, moveableObj)
                else:
                    p.PolyvsPoly(moveableObj, staticObj)
    print('collision Finished, ',len(possibleStaticObjList), 'takeTime: ', time.time()-startTime)

if __name__ == "__main__":
    import time,threading,multiprocessing
    FPS = 60
    SCREEN_SIZE = (1920, 1080)
    line1 = physicalEngine.Line((0,0), (1,2))
    line2 = physicalEngine.Line((3,4), (5, 10))
    p = physicalEngine.Collision()
    print("lineseg vs lineseg: ", p.LineSegmentvsLineSegment(line1, line2))

    polygon1 = physicalEngine.Polygon([(4,7), (3,4), (7,1), (14,4), (11,8), (6,9)], mass=0)
    polygon2 = physicalEngine.Polygon([(4,7), (5,7), (4,9), (5,9)], 0)
    circle1 = physicalEngine.Circle((13,8),4, 0)
    circle2 = physicalEngine.Circle((18,7), 2, 0)
    square = physicalEngine.Polygon([(2,8), (2,6), (6,6), (6,8)],0)
    group = physicalEngine.Group((polygon1, polygon2, circle1, circle2),0)
    print('polygonvspoly: ', p.PolyvsPoly(polygon1, polygon2))
    staticObjList = []

    #for i in range(100000):
       # staticObjList.append(physicalEngine.Polygon([(0,0), (0,i), (i,i), (i,0)], 0))

    for _ in range(100000):
        staticObjList.append(square)

    moveableObjList = [polygon1]
    

    for moveableObj in moveableObjList:
        possibleStaticObjList = []
        aabbStartTime = time.time()
        for staticObj in staticObjList:
            if p.AABBvsAABB(moveableObj.AABBForCollision, staticObj.AABBForCollision):
                possibleStaticObjList.append(staticObj)
        print(f'aabb collision finished. it takes: {time.time()-aabbStartTime}sec')
        print(f'len of possibleStaticObjList is {len(possibleStaticObjList)}')
        a = len(possibleStaticObjList)
        pr1 = multiprocessing.Process(target=collision, args=(p,moveableObj,possibleStaticObjList[:a//4]))
        pr2 = multiprocessing.Process(target=collision, args=(p,moveableObj,possibleStaticObjList[a//4:a//2]))
        #pr3 = multiprocessing.Process(target=collision, args=(p,moveableObj,possibleStaticObjList[a//2:(a//4)*3]))
        #pr4 = multiprocessing.Process(target=collision, args=(p,moveableObj,possibleStaticObjList[(a//4)*3:]))
        pr1 = multiprocessing.Process(target=collision, args=(p,moveableObj,possibleStaticObjList[:a//2]))
        pr2 = multiprocessing.Process(target=collision, args=(p,moveableObj,possibleStaticObjList[a//2:]))

        startTime = time.time()
        pr1.start()
        pr2.start()
        #pr3.start()
        #pr4.start()

        pr1.join()
        pr2.join()
        #pr3.join()
        #pr4.join()
        print(f'========================collision finished with multiprocessing. it takes {time.time()-startTime}===============')