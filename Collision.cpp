#include <iostream>
#include <math.h>
#include <vector>

struct dot
{
    float x;
    float y;
};

struct AABB
{
    dot dotList[4];

    float minX;
    float minY;
    float maxX;
    float maxY;
};

struct Circle
{
    dot centerDot;
    float radius;
    AABB AABB;
    bool type = false;
};

struct Polygon
{
    int arrayLen;
    dot* dotList = new dot[arrayLen];
    AABB AABB;
    bool type = true;
};

struct Line
{
    float slope;
    float xIntercept;
    float yIntercept;
    dot dotList[2];
    
};

class Collision
{
    private:
        Line makeLineByDot(dot dot1, dot dot2)
        {
            float a = dot1.x - dot2.x;
            float slope, xIntercept, yIntercept;
            dot dotList[2] = {dot1, dot2};
            if(a == 0)
            {
                slope = NULL;
            }
            else
            {
                slope = (dot1.y - dot2.y)/a;
            }

            if(slope == NULL)
            {
                xIntercept = dot1.x;
                yIntercept = NULL;
            }
            else
            {
                yIntercept = dot1.y - slope*dot1.x;
                xIntercept = NULL;
            }

            Line toReturn = {slope, xIntercept, yIntercept, dotList};
            return toReturn;
        }

    public:
        float getDotvsDotDistanceSquared(dot dot1, dot dot2)
        {
            return pow(dot1.x-dot2.x, 2) + pow(dot1.y-dot2.y, 2);
        }
        
        float getLinevsDotDistance(Line line1, dot dot1)
        {
            float a = line1.dotList[0].x - line1.dotList[1].x;
            float b = line1.dotList[0].y - line1.dotList[1].y;
            return abs(a*(dot1.y - line1.dotList[1].y) - b*(dot1.x - line1.dotList[1].x))/sqrt(pow(a, 2) + pow(b, 2));
        }

        bool lineSegvsLineseg(Line line1, Line line2)
        {
            dot meet;
            if(line1.slope == line2.slope)
            {
                return false;
            }
            if(line1.slope == NULL)
            {
                meet = {line1.xIntercept, line2.slope*line1.xIntercept + line2.yIntercept};
                line1.slope = 99999999;
            }
            else if(line2.slope == NULL)
            {
                meet = {line2.xIntercept, line1.slope*line2.xIntercept + line1.yIntercept};
                line2.slope = 99999999;
            }
            else
            {
                meet = {(line2.yIntercept - line1.yIntercept)/(line1.slope - line2.slope), line1.slope*(line2.yIntercept - line1.yIntercept)/(line1.slope - line2.slope) + line1.yIntercept};
            }

            if(abs(line1.slope) < abs(line2.slope))
            {
                if((line1.dotList[1].x - meet.x)*(line1.dotList[0].x - meet.x) > 0 || (line2.dotList[0].y - meet.y)*(line2.dotList[1].y - meet.y) > 0)
                {
                    return false;
                }
            }
            else
            {
                if((line2.dotList[1].x - meet.x)*(line2.dotList[0].x - meet.x) > 0 || (line1.dotList[0].y - meet.y)*(line1.dotList[1].y - meet.y) > 0)
                {
                    return false;
                }
            }
            return true;
        }
        bool isDotInPolygon(dot dot1, Polygon polygon1)
        {
            dot dot2 = {dot1.x + 10000, dot1.y};
            Line dotLine = makeLineByDot(dot1, dot2);
            Line polygonLine;
            int meetCount = 0;

            for(int i = 0; i < sizeof(polygon1.dotList)/sizeof(dot)-1; i++)
            {
                polygonLine = makeLineByDot(polygon1.dotList[i], polygon1.dotList[i+1]);
                if(lineSegvsLineseg(dotLine, polygonLine))
                {
                    meetCount += 1;
                }
            }
            polygonLine = makeLineByDot(polygon1.dotList[0], polygon1.dotList[sizeof(polygon1.dotList)/sizeof(dot)-1]);
            if(lineSegvsLineseg(dotLine, polygonLine))
            {
                meetCount += 1;
            }

            if(meetCount%2)
            {
                return true;
            }
            return false;

        }
        int* getPolydotInOtherPoly(Polygon sourcePoly, Polygon backGroundPoly)
        {
            std::vector<int> polyIndexs;
            for(int i = 0; i < sizeof(sourcePoly.dotList)/sizeof(dot); i ++)
            {
                if(isDotInPolygon(sourcePoly.dotList[i], backGroundPoly))
                {
                    polyIndexs.push_back(i);
                }
            }
            int *toReturn = new int[polyIndexs.size()];
            for(int i = 0; i < sizeof(toReturn)/sizeof(int); i++)
            {
                toReturn[i] = polyIndexs[i];
            }

            return toReturn;
        }
        
        bool AABBvsAABB(AABB AABB1, AABB AABB2)
        {
            if(AABB1.minX > AABB2.maxX || AABB2.minX > AABB1.maxX)
            {
                return false;
            }
            if(AABB1.minY > AABB2.maxY || AABB2.minY > AABB1.maxY)
            {
                return false;
            }
            return true;
        }

        bool CirclevsCircle(Circle circle1, Circle circle2)
        {
            float centerDotDistanceSquared = getDotvsDotDistanceSquared(circle1.centerDot, circle2.centerDot);
            return pow(circle1.radius + circle2.radius, 2) > centerDotDistanceSquared;
        }
};