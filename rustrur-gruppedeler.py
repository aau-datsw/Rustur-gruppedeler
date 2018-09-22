from math import exp
from random import random, randrange
import csv
import sys

csv_file_datalogi = "Datalogi.csv"
csv_file_software = "Software.csv"
csv_new_file_datalogi = "GroupsDatalogi.csv"
csv_new_file_software = "GroupsSoftware.csv"
sys.setrecursionlimit(10000)
max_iterations = 10000
max_temperature = 10000
group_size_dat = 11
group_size_sw = 17


class Student:
    def __init__(self, name, p0group):
        self.name = name
        self.p0group = p0group

    def __str__(self):
        return "({}, {})".format(self.name, self.p0group)


def csv_reader(csv_file):
    """
    Read the CSV file. The CSV file is expected to have the first column as the P0-groups, followed by the students name
    :param csv_file: Path to the csv file
    :return: return a list of students.
    """
    csv_students = []

    with open(csv_file, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            group_name = row[0]
            for student in row[1:]:
                if student == "":
                    break
                csv_students.append(Student(student, group_name))

    return csv_students


def csv_writer(csv_new_file, groups):
    """
    Writes the new groups to an csv file
    :param csv_new_file: Path to the new csv file
    :param groups: the list of groups
    """
    with open(csv_new_file, "a+") as file:
        writer = csv.writer(file, delimiter=";")
        for group in groups:
            writer.writerow(["New group"])
            for student in group:
                if student.name is None:
                    break
                writer.writerow([student.name, student.p0group])


def simulated_annealing(students, **params):
    """
    Used as an attempt for randomizing the groups
    :param students: The list of students
    :param params:
    :return: the best groups
    """
    current = divide_into_groups(students, **params)
    best = current
    cost_best = similarity(best, **params)

    for i in range(1, max_iterations - 1):
        next_state = permute_groups(current, **params)
        temperature = calculate_temperature(i, max_temperature, **params)

        cost_cur = similarity(current, **params)
        cost_next = similarity(next_state, **params)

        if cost_next <= cost_cur:
            current = next_state

            if cost_next <= cost_best:
                print("New best found. Cost: {}".format(cost_best))
                best = next_state
                cost_best = cost_next

        elif exp((cost_cur - cost_next) / temperature) > random():
            current = next_state

    return best


def divide_into_groups(students, num_groups, **kwargs):
    """
    Initial groups
    :param students: list of students
    :param num_groups: Total amount of groups
    :param kwargs:
    :return: non-random groups with no duplicates
    """
    groups = [[] for _ in range(0, num_groups)]

    for idx, student in enumerate(students):
        groups[idx % num_groups].append(student)

    return groups


def permute_groups(groups, **kwargs):
    """
    Get two random group members, swap them around, and checks if there's any duplicates
    :param groups: Initial groups
    :param kwargs:
    :return: Return a new group
    """
    groups_cpy = groups[:]

    group1 = randrange(0, len(groups_cpy))
    group2 = randrange(0, len(groups_cpy))

    while group1 == group2:
        group2 = randrange(0, len(groups_cpy))

    group1_member = randrange(0, len(groups_cpy[group1]))
    group2_member = randrange(0, len(groups_cpy[group2]))

    # Swap
    temp = groups_cpy[group1][group1_member]
    groups_cpy[group1][group1_member] = groups_cpy[group2][group2_member]
    groups_cpy[group2][group2_member] = temp

    if contains_duplicates(groups_cpy[group1]) or contains_duplicates(groups_cpy[group2]):
        return permute_groups(groups_cpy, **kwargs)
    else:
        return groups_cpy


def contains_duplicates(group):
    """
    Checks for duplicates in the groups
    (Two duplicates are allowed, software was 24 P0 groups, and we needed 17 rustur groups)
    :param group: a list of groups
    :return: True if more then 1 duplicate pr. team, else False
    """
    for idx, student in enumerate(group):
        for i in range(idx + 1, len(group)):
            duplicates = 0
            if student.p0group == group[i].p0group:
                duplicates += 1
                if duplicates >= 2:
                    return True

    return False


def calculate_temperature(iteration, max_temperature, **kwargs):
    """
    Linear cooling functions
    :param iteration: current iterations
    :param max_temperature:
    :param kwargs:
    :return: new temperature
    """
    return max_temperature - iteration


def similarity(groups, **kwargs):
    """
    How similar are the groups?
    :param groups: a list of groups
    :param kwargs:
    :return: their similarity sum
    """
    similarity_sum = 0

    for idx, group in enumerate(groups):
        for i in range(idx + 1, len(groups)):
            similarity_sum += pairwise_similarity(group, groups[i])

    return similarity_sum


def pairwise_similarity(group1, group2):
    """
    Used to calculate the similarity
    :param group1: First group
    :param group2: Second group
    :return: the pairwise similarity between the two groups
    """
    equal_students = 0

    for student1 in group1:
        for student2 in group2:
            if student1.p0group == student2.p0group:
                equal_students += 1

    return equal_students / min(len(group1), len(group2))


def calculate(students, grp_size):
    """
    Runs the simulated annealing process, when done there's a check for duplicates
    :param students: list of students
    :param grp_size: the size of the groups
    :return: the new groups
    """
    groups = simulated_annealing(students, num_groups=grp_size)
    for group in groups:
        if contains_duplicates(group):
            print("Duplicates! Rerunning")
            calculate(students, grp_size)
        else:
            print("No duplicates")
    return groups


def run(students, new_csv_file, group_size):
    print("Creating " + new_csv_file)
    groups = calculate(students, group_size)
    csv_writer(new_csv_file, groups)


sw_students = csv_reader(csv_file_software)
dat_students = csv_reader(csv_file_datalogi)

run(sw_students, csv_new_file_software, group_size_sw)
run(dat_students, csv_new_file_datalogi, group_size_dat)
