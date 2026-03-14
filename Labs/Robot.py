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
                new_collected_m1 = tuple(collected_m1+ (new_position,))

            if new_position in self.parts_m2 and new_position not in collected_m2 and m1_fixed and not m2_fixed:
                new_collected_m2 = tuple(collected_m2 + (new_position,))

            successors["Right"] = (new_position, new_collected_m1, new_collected_m2, m1_fixed, m2_fixed, 0)

        # LEFT
        new_position = moveLeft(robot_pos, self.walls)
        if new_position:
            new_collected_m1 = collected_m1
            new_collected_m2 = collected_m2

            if new_position in self.parts_m1 and new_position not in collected_m1 and not m1_fixed:
                new_collected_m1 = tuple(collected_m1+ (new_position,))

            if new_position in self.parts_m2 and new_position not in collected_m2 and m1_fixed and not m2_fixed:
                new_collected_m2 = tuple(collected_m2 + (new_position,))

            successors["Left"] = (new_position, new_collected_m1, new_collected_m2, m1_fixed, m2_fixed, 0)

        # UP
        new_position = moveUp(robot_pos, self.walls)
        if new_position:
            new_collected_m1 = collected_m1
            new_collected_m2 = collected_m2

            if new_position in self.parts_m1 and new_position not in collected_m1 and not m1_fixed:
                new_collected_m1 = tuple(collected_m1 + (new_position,))

            if new_position in self.parts_m2 and new_position not in collected_m2 and m1_fixed and not m2_fixed:
                new_collected_m2 = tuple(collected_m2 + (new_position,))

            successors["Up"] = (new_position, new_collected_m1, new_collected_m2, m1_fixed, m2_fixed, 0)

        # DOWN
        new_position = moveDown(robot_pos, self.walls)
        if new_position:
            new_collected_m1 = collected_m1
            new_collected_m2 = collected_m2

            if new_position in self.parts_m1 and new_position not in collected_m1 and not m1_fixed:
                new_collected_m1 = tuple(collected_m1 + (new_position,))

            if new_position in self.parts_m2 and new_position not in collected_m2 and m1_fixed and not m2_fixed:
                new_collected_m2 = tuple(collected_m2 + (new_position,))

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
