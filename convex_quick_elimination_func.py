import math

def convex_hull_quickelimination(S):
    hull = []  # Create an empty list to store the convex hull points

    def quickHull(S):
        if len(S) < 3:
            hull.extend(S)
            return

        S = sorted(S, key=lambda x: x[0])
        hull.append(S[0])
        hull.append(S[-1])
        S1 = []
        S2 = []

        for x in S:
            z = sideOfLinePointIsOn([S[0], S[-1]], x)
            if z > 0.00:
                S2.append(x)
            elif z < 0.00:
                S1.append(x)

        findHull(S1, S[0], S[-1])
        findHull(S2, S[-1], S[0])

    def findHull(Sk, P, Q):
        if len(Sk) == 0:
            return

        furthestPoint = Sk[0]
        maxDist = 0

        for x in Sk:
            dist = findDistPointLine(x, [P, Q])
            if dist > maxDist:
                maxDist = dist
                furthestPoint = x

        Sk.remove(furthestPoint)

        hull.insert(1, furthestPoint)
        S1 = []
        S2 = []

        for p in Sk:
            if sideOfLinePointIsOn([P, furthestPoint], p) > 0.00:
                S2.append(p)
            elif sideOfLinePointIsOn([furthestPoint, Q], p) < 0.00:
                S1.append(p)

        findHull(S1, P, furthestPoint)
        findHull(S2, furthestPoint, Q)

    def findPointDistance(P1, P2):
        return math.hypot(P2[0] - P1[0], P2[1] - P1[1])

    def findNearestPoint(point, line):
        line = sorted(line, key=lambda x: x[0])
        # Calculate the slope of the line
        if line[0][0] != line[1][0]:
            slope = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
            yIntercept = line[0][1] - slope * line[0][0]
            # Calculate the perpendicular line's slope and y-intercept
            slopePerpendicular = -1 / slope
            yInterceptPerpendicular = point[1] - slopePerpendicular * point[0]
            # Find the intersection point of the two lines
            intersectionX = (yInterceptPerpendicular - yIntercept) / (slope - slopePerpendicular)
            intersectionY = slope * intersectionX + yIntercept
            return [intersectionX, intersectionY]
        else:
            # The line is vertical, so the nearest point is directly below the given point
            return [line[0][0], point[1]]

    def findDistPointLine(point, line):
        nearest_point = findNearestPoint(point, line)
        return findPointDistance(point, nearest_point)

    def sideOfLinePointIsOn(line, x):
        vectAB = (line[1][0] - line[0][0], line[1][1] - line[0][1])
        vectAX = (x[0] - line[0][0], x[1] - line[0][1])
        zCoord = vectAB[0] * vectAX[1] - vectAB[1] * vectAX[0]
        return zCoord

    def isInsideTriangle(A, B, C, p):
        z1 = sideOfLinePointIsOn((A, B), p)
        z2 = sideOfLinePointIsOn((B, C), p)
        z3 = sideOfLinePointIsOn((C, A), p)

        if (z1 >= 0.00 and z2 >= 0.00 and z3 >= 0.00) or (z1 <= 0.00 and z2 <= 0.00 and z3 <= 0.00):
            return True

    quickHull(S)
    return hull
