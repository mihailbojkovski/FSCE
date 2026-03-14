from searching_framework import *


def moveRight(robot_pos, walls):
    if robot_pos[0] < 9 and (robot_pos[0] + 1, robot_pos[1]) not in walls:
        return (robot_pos[0] + 1, robot_pos[1])


def moveLeft(robot_pos, walls):
    if robot_pos[0] > 0 and (robot_pos[0] - 1, robot_pos[1]) not in walls:
        return (robot_pos[0] - 1, robot_pos[1])


def moveUp(robot_pos, walls):
    if robot_pos[1] < 9 and (robot_pos[0], robot_pos[1] + 1) not in walls:
        return (robot_pos[0], robot_pos[1] + 1)


def moveDown(robot_pos, walls):
    if robot_pos[1] > 0 and (robot_pos[0], robot_pos[1] - 1) not in walls:
        return (robot_pos[0], robot_pos[1] - 1)


class Robot(Problem):

    def __init__(self, initial, m1_pos, m2_pos, s1, s2, parts_m1, parts_m2, walls):
        super().__init__(initial)
        self.m1_pos = m1_pos
        self.m2_pos = m2_pos
        self.s1 = s1
        self.s2 = s2
        self.parts_m1 = parts_m1
        self.parts_m2 = parts_m2
        self.walls = walls

    def actions(self, state):
        return list(self.successor(state).keys())

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        robot_pos, collected_m1, collected_m2, m1_fixed, m2_fixed, repair_count = state
        return m1_fixed and m2_fixed

    def successor(self, state):
        robot_pos, collected_m1, collected_m2, m1_fixed, m2_fixed, repair_count = state

        successors = {}

        # RIGHT
        new_position = moveRight(robot_pos, self.walls)
        if new_position:
            new_collected_m1 = collected_m1
            new_collected_m2 = collected_m2

            if new_position in self.parts_m1 and new_position not in collected_m1 and not m1_fixed:
                new_collected_m1 = tuple(sorted(collected_m1 + (new_position,)))

            if new_position in self.parts_m2 and new_position not in collected_m2 and m1_fixed and not m2_fixed:
                new_collected_m2 = tuple(sorted(collected_m2 + (new_position,)))

            successors["Right"] = (new_position, new_collected_m1, new_collected_m2, m1_fixed, m2_fixed, 0)

        # LEFT
        new_position = moveLeft(robot_pos, self.walls)
        if new_position:
            new_collected_m1 = collected_m1
            new_collected_m2 = collected_m2

            if new_position in self.parts_m1 and new_position not in collected_m1 and not m1_fixed:
                new_collected_m1 = tuple(sorted(collected_m1 + (new_position,)))

            if new_position in self.parts_m2 and new_position not in collected_m2 and m1_fixed and not m2_fixed:
                new_collected_m2 = tuple(sorted(collected_m2 + (new_position,)))

            successors["Left"] = (new_position, new_collected_m1, new_collected_m2, m1_fixed, m2_fixed, 0)

        # UP
        new_position = moveUp(robot_pos, self.walls)
        if new_position:
            new_collected_m1 = collected_m1
            new_collected_m2 = collected_m2

            if new_position in self.parts_m1 and new_position not in collected_m1 and not m1_fixed:
                new_collected_m1 = tuple(sorted(collected_m1 + (new_position,)))

            if new_position in self.parts_m2 and new_position not in collected_m2 and m1_fixed and not m2_fixed:
                new_collected_m2 = tuple(sorted(collected_m2 + (new_position,)))

            successors["Up"] = (new_position, new_collected_m1, new_collected_m2, m1_fixed, m2_fixed, 0)

        # DOWN
        new_position = moveDown(robot_pos, self.walls)
        if new_position:
            new_collected_m1 = collected_m1
            new_collected_m2 = collected_m2

            if new_position in self.parts_m1 and new_position not in collected_m1 and not m1_fixed:
                new_collected_m1 = tuple(sorted(collected_m1 + (new_position,)))

            if new_position in self.parts_m2 and new_position not in collected_m2 and m1_fixed and not m2_fixed:
                new_collected_m2 = tuple(sorted(collected_m2 + (new_position,)))

            successors["Down"] = (new_position, new_collected_m1, new_collected_m2, m1_fixed, m2_fixed, 0)

        # REPAIR M1
        if robot_pos == self.m1_pos and not m1_fixed and len(collected_m1) == len(self.parts_m1):

            new_count = repair_count + 1
            new_m1_fixed = m1_fixed

            if new_count == self.s1:
                new_m1_fixed = True
                new_count = 0

            successors["Repair"] = (robot_pos, collected_m1, collected_m2, new_m1_fixed, m2_fixed, new_count)

        # REPAIR M2
        if robot_pos == self.m2_pos and m1_fixed and not m2_fixed and len(collected_m2) == len(self.parts_m2):

            new_count = repair_count + 1
            new_m2_fixed = m2_fixed

            if new_count == self.s2:
                new_m2_fixed = True
                new_count = 0

            successors["Repair"] = (robot_pos, collected_m1, collected_m2, m1_fixed, new_m2_fixed, new_count)

        return successors
if __name__ == '__main__':
    robot_start_pos = tuple(map(int, input().split(',')))
    M1_pos = tuple(map(int, input().split(',')))
    M1_steps = int(input())
    M2_pos = tuple(map(int, input().split(',')))
    M2_steps = int(input())

    parts_M1 = int(input())
    to_collect_M1 = tuple(tuple(map(int, input().split(','))) for _ in range(parts_M1))

    parts_M2 = int(input())
    to_collect_M2 = tuple(tuple(map(int, input().split(','))) for _ in range(parts_M2))

    walls = [(4,0),(5,0),(7,5),(8,5),(9,5),(1,6),(1,7),(0,6),(0,8),(0,9),(1,9),(2,9),(3,9)]

    initial_state = (robot_start_pos, tuple(), tuple(), False, False, 0)

    problem = Robot(initial_state, M1_pos, M2_pos, M1_steps, M2_steps, to_collect_M1, to_collect_M2, walls)

    result = breadth_first_graph_search(problem)

    if result is not None:
        print(result.solution())
    else:
        print("No Solution!")

