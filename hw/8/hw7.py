from sys import path
import os, random, math
path.append(os.path.abspath("..") + "/2")
from hw_2 import Num, Col, Tbl, cells, cols, rows, file

seed = random.seed


class Tree:
    def __init__(self):
        self.children = []
        self.leaves = []
        self.level = 0
        self.isRoot = False
        self.splitCount = 0


def print_tree(root):
    if not root.isRoot:
        for _ in range(root.level):
            print("|. ", end=" ")
    print(root.splitCount)
    if len(root.children) == 0:
        for _ in range(root.level - 1):
            print("|. ", end=" ")
        for col in root.leaves:
            print(col.column_name + " = ", end=" ")
            if (isinstance(col, Num)):
                print("{0} ({1})".format(col.mu, col.sd), end=" ")
            else:
                print("{0} ({1})".format(col.mode, col.entropy), end=" ")
        print("")
    else:
        for each in root.children:
            print_tree(each)
    if root.isRoot:
        for col in root.leaves:
            print(col.column_name + " = ", end=" ")
            if (isinstance(col, Num)):
                print("{0} ({1})".format(col.mu, col.sd), end=" ")
            else:
                print("{0} ({1})".format(col.mode, col.entropy), end=" ")


def distance(row1, row2, cols):
    d, n, p = 0, 0, 2
    for col in cols:
        n += 1
        d0 = col.dist(row1.cells[col.position], row2.cells[col.position])
        d += d0 ** p
    return d ** (1 / p) / n ** (1 / p)  # normalize distance


def cosine(x, y, z, dist, cols):
    return (distance(x, z, cols) ** 2 + dist ** 2 - distance(y, z, cols) ** 2) / (2 * dist)


class homework7:
    def __init__(self, file_name):
        seed(1)
        self.file_contents = cells(cols(rows(file(file_name))))
        self.tbl = Tbl()
        self.file_processing()
        self.tree = self.split(self.tbl, 0)
        print_tree(self.tree)

    def file_processing(self):
        for idx, row in enumerate(self.file_contents):
            if idx:
                self.tbl.add_row(row)
            else:
                self.tbl.add_column(row)

    def split(self, tbl, level):
        singlenode = Tree()
        if len(tbl.rows) < 2 * pow(len(self.tbl.rows), 1 / 2):
            for each in tbl.col_info['goals']:
                singlenode.leaves.append(tbl.cols[each])
            singlenode.level, singlenode.splitCount = level, len(tbl.rows)
        else:
            best_tuple, best_points = self.best_pivot_points(tbl)
            tbl_left, tbl_right = Tbl(), Tbl()
            self.getSingleNode(best_points, tbl_left, level, tbl_right, singlenode, tbl)
        return singlenode

    def getSingleNode(self, best_points, left_tbl, level, right_tbl, singlenode, tbl):
        left_tbl.add_column([col.column_name for col in tbl.cols])
        right_tbl.add_column([col.column_name for col in tbl.cols])
        for idx, each in enumerate(tbl.rows):
            if idx in best_points:
                right_tbl.add_row(each.cells)
            else:
                left_tbl.add_row(each.cells)
        splitCount = len(left_tbl.rows) + len(right_tbl.rows)
        singlenode.children.append(self.split(left_tbl, level + 1))
        singlenode.children.append(self.split(right_tbl, level + 1))
        singlenode.splitCount = splitCount
        singlenode.level = level

    def mapper(self, tbl):
        cols = [tbl.cols[col] for col in tbl.col_info['xs']]
        random_point = random.randint(0, len(tbl.rows) - 1)
        first_pivot_idx = self.get_first_pivot(cols, random_point, tbl)
        second_pivot_idx, second_pivot_pts = self.get_second_pivot(cols, first_pivot_idx, tbl)
        dist = second_pivot_pts[math.floor(len(second_pivot_pts) * 0.9)][1]
        return first_pivot_idx, second_pivot_idx, dist

    def get_second_pivot(self, cols, first_pivot_idx, tbl):
        second_pivot_pts = []
        for row in range(0, len(tbl.rows)):
            dist = distance(tbl.rows[first_pivot_idx], tbl.rows[row], cols)
            second_pivot_pts.append((row, dist))
        second_pivot_pts.sort(key=lambda x: x[1])
        second_pivot_idx = second_pivot_pts[math.floor(len(second_pivot_pts) * 0.9)][0]
        return second_pivot_idx, second_pivot_pts

    def get_first_pivot(self, cols, random_point, tbl):
        first_pivot_pts = []
        for row in range(0, len(tbl.rows)):
            dist = distance(tbl.rows[random_point], tbl.rows[row], cols)
            first_pivot_pts.append((row, dist))
        first_pivot_pts.sort(key=lambda x: x[1])
        first_pivot_idx = first_pivot_pts[math.floor(len(first_pivot_pts) * 0.9)][0]
        return first_pivot_idx

    def best_pivot_points(self, tbl):
        counter = 10
        initial = len(tbl.rows)
        best_tuple = None
        best_points = None
        while counter > 0:
            counter -= 1
            tuple = self.mapper(tbl)
            all_list = self.get_sorted_all_list(tuple, tbl)
            length = len(all_list)
            index = (length - 1) // 2
            median_distance = self.get_mean_distance(all_list, index, length)
            point_set = self.get_point_set(all_list, median_distance)
            right = abs(len(point_set) - (length - len(point_set)))
            if right < initial:
                initial, best_points, best_tuple = right, point_set, tuple
        return best_tuple, best_points

    def get_point_set(self, all_list, median_distance):
        pointset = set()
        for point in all_list:
            if point[1] < median_distance:
                pointset.add(point[0])
        return pointset

    def get_mean_distance(self, all_list, index, length):
        if (length % 2):
            median_distance = all_list[index][1]
        else:
            median_distance = (all_list[index][1] + all_list[index + 1][1]) / 2.0
        return median_distance

    def get_sorted_all_list(self, pivot_tuple, tbl):
        all_list = []
        cols = [tbl.cols[col] for col in tbl.col_info['xs']]
        for row in range(0, len(tbl.rows)):
            dist = cosine(tbl.rows[pivot_tuple[0]], tbl.rows[pivot_tuple[1]], tbl.rows[row], pivot_tuple[2], cols)
            all_list.append((row, dist))
        all_list.sort(key=lambda x: x[1])
        return all_list

    def callme(self,filename):
        print("---showing output for this file ----")
        print(filename.split('.')[0])
        hw7 = homework7(filename)


# homework7.callme('xomo10000.csv')
# homework7.callme('xomo10000.csv')
