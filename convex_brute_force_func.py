def convex_hull_bruteforce(points):
    n = len(points)
    if n < 3:
        return points
    hull = []
    for i in range(n):
        for j in range(n):
            if i != j:
                valid = True
                for k in range(n):
                    if k != i and k != j:
                        if orientation(points[i], points[j], points[k]) == 1:
                            valid = False
                            break
                if valid:
                    if points[i] not in hull:
                        hull.append(points[i])
                    if points[j] not in hull:
                        hull.append(points[j])
    return hull

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

