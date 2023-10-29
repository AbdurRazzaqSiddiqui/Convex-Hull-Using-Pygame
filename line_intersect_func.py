# Function to find the intersection point of two lines
def line_intersection_checker_algebra(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if den == 0:
        return None  # Lines are parallel

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

    if 0 <= t <= 1 and 0 <= u <= 1:
        return True  # Lines intersect
    return False  # Lines do not intersect

# Find intersection using CCW
def line_intersection_checker_CCW(line1, line2):
    p1, p2 = line1
    p3, p4 = line2

    def ccw(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    if ccw(p1, p3, p4) * ccw(p2, p3, p4) <= 0 and ccw(p1, p2, p3) * ccw(p1, p2, p4) <= 0:
        return True  # Lines intersect
    return False  # Lines do not intersect

# Find intersection using Research