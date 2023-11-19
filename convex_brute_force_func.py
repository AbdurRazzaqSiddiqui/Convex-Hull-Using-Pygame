from itertools import combinations

def orientation(p, q, r):
    """
    Function to determine the orientation of triplet (p, q, r).
    Returns:
    0 : Collinear points
    1 : Clockwise points
    2 : Counterclockwise
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

def on_segment(p, q, r):
    """
    Given three collinear points p, q, r, the function checks if 
    point q lies on line segment 'pr'.
    """
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def convex_hull_bruteforce(points):
    n = len(points)
    result = []

    for combo in combinations(points, 3):
        p, q, r = combo
        o = orientation(p, q, r)
        if o == 0:  # Collinear points
            if on_segment(p, q, r):
                result.append(p)
                result.append(q)
                result.append(r)
        elif o == 1:  # Clockwise
            result.append(p)
            result.append(q)
            result.append(r)
        else:  # Counterclockwise
            result.append(p)
            result.append(r)
            result.append(q)

    return list(set(result))