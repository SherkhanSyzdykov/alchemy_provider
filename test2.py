from typing import List
from collections import deque


def max_area(height: List[int]) -> int:
    height_length = len(height)
    if height_length < 2:
        return 0

    S = 0
    first = 0
    second = height_length - 1

    while first < second:
        lower = height[first]
        if lower > height[second]:
            lower = height[second]

        s = lower * (second - first)

        print({'lower': lower, 's': s, 'S': S, 'weight': second - first})
        if s > S:
            S = s

        # [1,8,6,2,5,4,8,3,7]
        if height[first] < height[second]:
            first += 1
            continue

        second -= 1

    return S


max_area(
[1,8,6,2,5,4,8,3,7]
)