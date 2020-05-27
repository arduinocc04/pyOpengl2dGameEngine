#include <iostream>
#include <math.h>
#include <vector>

struct dot {
    float x;
    float y;
};

struct AABB {
    dot dotList[4];

    float minX;
    float minY;
    float maxX;
    float maxY;
};

struct Circle {

    dot centerDot;
    float radius;
    AABB AABB;
    bool type = false;
};

struct Polygon {
    dot* dotList;
    AABB AABB;
    bool type = true;
};

struct Line {
    float slope;
    float xIntercept;
    float yIntercept;
    dot dotList[2];
    
};

class Helper
{
    public:
        void delPolyDotList(Polygon poly1) {
            delete poly1.dotList;
        }

        AABB makeAABB(float dotList[][2]) {
            float* xList = new float[sizeof(dotList)/sizeof(float)];
            float* yList = new float[sizeof(dotList)/sizeof(float)];

            for(int i = 0; i < sizeof(dotList)/sizeof(float); i++) {
                xList[i] = dotList[i][0];
                yList[i] = dotList[i][1];
            }

            float minX = xList[0];
            float maxX = xList[0];
            float minY = yList[0];
            float maxY = yList[0];
            for(int i = 0; i< sizeof(dotList)/sizeof(float); i++) {
                if(xList[i] < minX) {
                    minX = xList[i];
                }
                else if(xList[i] > maxX) {
                    maxX = xList[i];
                }

                if(yList[i] < minY) {
                    minY = yList[i];
                }
                else if(yList[i] > maxY) {
                    maxY = yList[i];
                }
            }
            //return process..    
            AABB toReturn;
            toReturn.dotList[0] = {minX, minY};
            toReturn.dotList[1] = {maxX, minY};
            toReturn.dotList[2] = {maxX, maxY};
            toReturn.dotList[3] = {minX, maxY};
            toReturn.minX = minX;
            toReturn.maxX = maxX;
            toReturn.minY = minY;
            toReturn.maxY = maxY;
            return toReturn;
        }

        Polygon makePolygon(float dotList[][2]) {
            Polygon toReturn;
            toReturn.dotList = new dot[sizeof(dotList)/sizeof(dot)];
            dot dot1;
            int dotListLen = sizeof(dotList)/sizeof(dot);
            for(int i = 0; i < dotListLen; i++) {
                dot1 = {dotList[i][0], dotList[i][1]};
                toReturn.dotList[i] = dot1;
            }
            toReturn.AABB = makeAABB(dotList);
            
            return toReturn;
        }   

        Circle makeCircle(float centerDot[2], float radius) {
            Circle toReturn;
            toReturn.centerDot.x = centerDot[0];
            toReturn.centerDot.y = centerDot[1];
            toReturn.radius = radius;
            float dots[4][2];
            dots[0][0] = centerDot[0] - radius;
            dots[0][1] = centerDot[1] - radius;
            dots[1][0] = centerDot[0] + radius;
            dots[1][1] = centerDot[1] - radius;
            dots[2][0] = centerDot[0] + radius;
            dots[2][1] = centerDot[1] + radius;
            dots[3][0] = centerDot[0] - radius;
            dots[3][1] = centerDot[1] + radius;
            toReturn.AABB = makeAABB(dots);
        }
};

class Collision
{
    private:
        Line makeLineByDot(dot dot1, dot dot2) {
            float a = dot1.x - dot2.x;
            float slope, xIntercept, yIntercept;
            dot dotList[2] = {dot1, dot2};
            if(a == 0) {
                slope = NULL;
            }
            else {
                slope = (dot1.y - dot2.y)/a;
            }

            if(slope == NULL) {
                xIntercept = dot1.x;
                yIntercept = NULL;
            }
            else {
                yIntercept = dot1.y - slope*dot1.x;
                xIntercept = NULL;
            }

            Line toReturn;
            toReturn.slope = slope;
            toReturn.xIntercept = xIntercept;
            toReturn.yIntercept = yIntercept;
            toReturn.dotList[0] = dotList[0];
            toReturn.dotList[1] = dotList[1];
            return toReturn;
        }

        bool rightTurn(dot dot1, dot dot2, dot dot3) {
            return (dot3.y - dot1.y)*(dot2.x - dot1.x) < (dot2.y - dot1.y)*(dot3.x - dot1.x);
        }

        std::vector<dot> grahamScan(std::vector<dot> dotList) {
            std::vector<dot> upper;
            std::vector<dot> lower;
            upper.push_back(dotList[0]);
            upper.push_back(dotList[1]);
            lower.push_back(dotList[sizeof(dotList)/sizeof(dot)-1]);
            lower.push_back(dotList[sizeof(dotList)/sizeof(dot)-2]);
            for(int i = 2; i < sizeof(dotList)/sizeof(dot); i++) {
                upper.push_back(dotList[i]);
                while(upper.size() > 2 && !(rightTurn(upper[upper.size()-1], upper[upper.size()-2], upper[upper.size()-3]))) {
                    upper.erase(upper.end() - 1);
                }
            }
            for(int i = sizeof(dotList)/sizeof(dot) - 3; i > -1; i--) {
                lower.push_back(dotList[i]);
                while(lower.size() > 2 && !(rightTurn(lower[lower.size()-1], lower[lower.size()-2], lower[lower.size()-3]))) {
                    lower.erase(lower.end() - 1);
                }
            }

            lower.erase(lower.begin());
            lower.erase(lower.end() - 1);
            for(int i = 0; i < lower.size(); i++) {
                upper.push_back(lower[i]);
            }

            return upper;
        }

    public:
        float getDotvsDotDistanceSquared(dot dot1, dot dot2) {
            return pow(dot1.x-dot2.x, 2) + pow(dot1.y-dot2.y, 2);
        }
        
        float getLinevsDotDistance(Line line1, dot dot1) {
            float a = line1.dotList[0].x - line1.dotList[1].x;
            float b = line1.dotList[0].y - line1.dotList[1].y;
            return abs(a*(dot1.y - line1.dotList[1].y) - b*(dot1.x - line1.dotList[1].x))/sqrt(pow(a, 2) + pow(b, 2));
        }

        bool lineSegvsLineseg(Line line1, Line line2) {
            dot meet;
            if(line1.slope == line2.slope) {
                return false;
            }
            if(line1.slope == NULL) {
                meet = {line1.xIntercept, line2.slope*line1.xIntercept + line2.yIntercept};
                line1.slope = 99999999;
            }
            else if(line2.slope == NULL) {
                meet = {line2.xIntercept, line1.slope*line2.xIntercept + line1.yIntercept};
                line2.slope = 99999999;
            }
            else {
                meet = {(line2.yIntercept - line1.yIntercept)/(line1.slope - line2.slope), line1.slope*(line2.yIntercept - line1.yIntercept)/(line1.slope - line2.slope) + line1.yIntercept};
            }

            if(abs(line1.slope) < abs(line2.slope)) {
                if((line1.dotList[1].x - meet.x)*(line1.dotList[0].x - meet.x) > 0 || (line2.dotList[0].y - meet.y)*(line2.dotList[1].y - meet.y) > 0) {
                    return false;
                }
            }
            else {
                if((line2.dotList[1].x - meet.x)*(line2.dotList[0].x - meet.x) > 0 || (line1.dotList[0].y - meet.y)*(line1.dotList[1].y - meet.y) > 0) {
                    return false;
                }
            }
            return true;
        }
        bool isDotInPolygon(dot dot1, Polygon polygon1) {
            dot dot2 = {dot1.x + 10000, dot1.y};
            Line dotLine = makeLineByDot(dot1, dot2);
            Line polygonLine;
            int meetCount = 0;

            for(int i = 0; i < sizeof(polygon1.dotList)/sizeof(dot)-1; i++) {
                polygonLine = makeLineByDot(polygon1.dotList[i], polygon1.dotList[i+1]);
                if(lineSegvsLineseg(dotLine, polygonLine)) {
                    meetCount += 1;
                }
            }
            polygonLine = makeLineByDot(polygon1.dotList[0], polygon1.dotList[sizeof(polygon1.dotList)/sizeof(dot)-1]);
            if(lineSegvsLineseg(dotLine, polygonLine)) {
                meetCount += 1;
            }

            if(meetCount%2) {
                return true;
            }
            return false;

        }
        bool isDotInAABB(dot dot1, AABB AABB1) {
            dot dot2 = {dot1.x + 10000, dot1.y};
            Line dotLine = makeLineByDot(dot1, dot2);
            Line polygonLine;
            int meetCount = 0;

            for(int i = 0; i < sizeof(AABB1.dotList)/sizeof(dot)-1; i++) {
                polygonLine = makeLineByDot(AABB1.dotList[i], AABB1.dotList[i+1]);
                if(lineSegvsLineseg(dotLine, polygonLine)) {
                    meetCount += 1;
                }
            }
            polygonLine = makeLineByDot(AABB1.dotList[0], AABB1.dotList[sizeof(AABB1.dotList)/sizeof(dot)-1]);
            if(lineSegvsLineseg(dotLine, polygonLine)) {
                meetCount += 1;
            }

            if(meetCount%2) {
                return true;
            }
            return false;

        }
        int* getPolyDotInOtherPoly(Polygon sourcePoly, Polygon backgroundPoly) {
            std::vector<int> polyIndexs;
            for(int i = 0; i < sizeof(sourcePoly.dotList)/sizeof(dot); i ++) {
                if(isDotInPolygon(sourcePoly.dotList[i], backgroundPoly)) {
                    polyIndexs.push_back(i);
                }
            }
            int *toReturn = new int[polyIndexs.size()];
            for(int i = 0; i < sizeof(toReturn)/sizeof(int); i++) {
                toReturn[i] = polyIndexs[i];
            }

            return toReturn;
        }

        int* getPolyDotInOtherAABB(Polygon sourcePoly, AABB backgroundAABB) {
            std::vector<int> polyIndexs;
            for(int i = 0; i < sizeof(sourcePoly.dotList)/sizeof(dot); i ++) {
                if(isDotInAABB(sourcePoly.dotList[i], backgroundAABB)) {
                    polyIndexs.push_back(i);
                }
            }
            int *toReturn = new int[polyIndexs.size()];
            for(int i = 0; i < sizeof(toReturn)/sizeof(int); i++) {
                toReturn[i] = polyIndexs[i];
            }

            return toReturn;
        }
        
        bool AABBvsAABB(AABB AABB1, AABB AABB2) {
            if(AABB1.minX > AABB2.maxX || AABB2.minX > AABB1.maxX) {
                return false;
            }
            if(AABB1.minY > AABB2.maxY || AABB2.minY > AABB1.maxY) {
                return false;
            }
            return true;
        }

        bool CirclevsCircle(Circle circle1, Circle circle2) {
            float centerDotDistanceSquared = getDotvsDotDistanceSquared(circle1.centerDot, circle2.centerDot);
            return pow(circle1.radius + circle2.radius, 2) > centerDotDistanceSquared;
        }

        bool PolyvsCircle(Polygon polygon1, Circle circle1) {
            for(int i = 0; i < sizeof(polygon1.dotList)/sizeof(dot); i++) {
                if (getDotvsDotDistanceSquared(polygon1.dotList[i], circle1.centerDot) < pow(circle1.radius, 2)) {
                    return true;
                }
            }
            return false;
        }

        bool PolyvsPoly(Polygon polygon1, Polygon polygon2, bool reversed=false) {
            if(!reversed) {
                if(PolyvsPoly(polygon2, polygon1, reversed=true)) {
                    return true;
                }
            }
            int* polygon2DotIndexInPolygon1AABB = getPolyDotInOtherAABB(polygon2, polygon1.AABB);
            if(sizeof(polygon2DotIndexInPolygon1AABB) == 0) {
                return false;
            }
            std::vector<dot> points;
            for(int i = 0; i < sizeof(polygon1.dotList)/sizeof(dot); i++) {
                points.push_back(polygon1.dotList[i]);
            }
            for(int i = 0; i < sizeof(polygon2DotIndexInPolygon1AABB)/sizeof(dot); i++) {
                points.push_back(polygon2.dotList[polygon2DotIndexInPolygon1AABB[i]]);
            }

            points = grahamScan(points);
            if(points.size() != sizeof(polygon1.dotList)/sizeof(dot)) {
                return false;
            }
            return true;
        }
};