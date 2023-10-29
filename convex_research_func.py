import random
import math

def convex_hull_research(points):
    def ccw(p1, p2, p3):
        return (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])

    def graham(points):
        points = sorted(points, key=lambda x: (x[1], x[0]))
        upper = []
        for p in points:
            while len(upper) >= 2 and ccw(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        return upper

    def divide_groups(points, k):
        n = len(points)
        groups = [points[i:i + k] for i in range(0, n, k)]
        return groups

    def chan(points, k):
        if len(points) <= k:
            return graham(points)

        groups = divide_groups(points, k)
        hulls = [chan(group, k) for group in groups]
        merged_hull = merge_hulls(hulls)
        return graham(merged_hull)

    def merge_hulls(hulls):
        if len(hulls) == 1:
            return hulls[0]
        if len(hulls) == 2:
            return merge_two_hulls(hulls[0], hulls[1])
        if len(hulls) % 2 != 0:
            extra_hull = hulls.pop()
        half = len(hulls) // 2
        left_half = merge_hulls(hulls[:half])
        right_half = merge_hulls(hulls[half:])
        return merge_two_hulls(left_half, right_half)

    def merge_two_hulls(left_hull, right_hull):
        left_tangent = (0, 0)
        right_tangent = (0, 0)
        left_index = 0
        right_index = 0

        for i in range(len(left_hull)):
            if left_hull[i][0] < left_tangent[0]:
                left_tangent = left_hull[i]
                left_index = i

        for i in range(len(right_hull)):
            if right_hull[i][0] > right_tangent[0]:
                right_tangent = right_hull[i]
                right_index = i

        while True:
            no_turn = True

            while ccw(left_hull[left_index], right_hull[right_index], right_hull[(right_index + 1) % len(right_hull)]) <= 0:
                right_index = (right_index + 1) % len(right_hull)
                no_turn = False

            while ccw(left_hull[(left_index - 1 + len(left_hull)) % len(left_hull)], left_hull[left_index], right_hull[right_index]) >= 0:
                left_index = (left_index - 1 + len(left_hull)) % len(left_hull)
                no_turn = False

            if no_turn:
                break

        upper_hull = left_hull[:left_index + 1] + right_hull[right_index:]
        lower_hull = right_hull[:right_index + 1] + left_hull[left_index:]

        return upper_hull + lower_hull

    return chan(points, 2)
