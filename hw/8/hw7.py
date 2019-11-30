from sys import path
import os, random, math
from collections import defaultdict
path.append(os.path.abspath("..") + "/2")
from hw_2 import Num, Sym,Col, cells, cols, rows, file
from hw6 import Tbl
seed=random.seed

class Tree:
    def __init__(i):
        i.children = []
        i.leaves = []
        i.tbl = None
        i.level = 0
        i.isRoot = False
        i.splitCount = 0    



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

class hw7:
    def __init__(i, file_name=None):
        seed(1)
        i.leaf_nodes = []
        i.file_contents = cells(cols(rows(file(file_name))))
        i.tbl = Tbl()
        i.file_processing()
        i.tree = i.split(i.tbl,0)
        
    def file_processing(i):
        for idx, row in enumerate(i.file_contents):
            if not idx:
                i.tbl.addCol(row)
            else:
                i.tbl.addRow(row)
    
    def split(i, tbl,level):
        n = Tree()
        if (len(tbl.rows) < 2* pow(len(i.tbl.rows),1/2)):
            for each in tbl.col_info['goals']:
                n.leaves.append(tbl.cols[each])
            n.level = level
            n.tbl = tbl
            n.splitCount = len(tbl.rows)
            i.leaf_nodes.append(n)
        else:
            best_tuple, best_points = i.best_pivot_points(tbl)
            left_tbl = Tbl()
            right_tbl = Tbl()
            left_tbl.addCol([col.column_name for col in tbl.cols])
            right_tbl.addCol([col.column_name for col in tbl.cols])
            for idx, each in enumerate(tbl.rows):
                if idx in best_points:
                    right_tbl.addRow(each.cells)
                else:
                    left_tbl.addRow(each.cells)
            splitCount = len(left_tbl.rows) + len(right_tbl.rows)
            n.children.append(i.split(left_tbl,level + 1))
            n.children.append(i.split(right_tbl, level + 1))
            n.splitCount = splitCount
            n.level = level
        return n

    def fast_map(i, tbl):
        cols = [tbl.cols[col] for col in tbl.col_info['xs']]
        random_point = random.randint(0,len(tbl.rows)-1)
        first_pivot_pts = []
        for row in range(0,len(tbl.rows)):
            dist = distance(tbl.rows[random_point],tbl.rows[row], cols)
            first_pivot_pts.append((row, dist))
        first_pivot_pts.sort(key = lambda x: x[1])
        first_pivot_idx = first_pivot_pts[math.floor(len(first_pivot_pts)*0.9)][0]    
        second_pivot_pts = []
        for row in range(0,len(tbl.rows)):
            dist = distance(tbl.rows[first_pivot_idx],tbl.rows[row], cols)
            second_pivot_pts.append((row, dist))
        second_pivot_pts.sort(key = lambda x: x[1])
        second_pivot_idx = second_pivot_pts[math.floor(len(second_pivot_pts)*0.9)][0]
        dist = second_pivot_pts[math.floor(len(second_pivot_pts)*0.9)][1]
        return (first_pivot_idx, second_pivot_idx, dist)
    
    def get_mean_distance(i, all_list, index, length):
        if (length % 2):
            median_distance = all_list[index][1]
        else:
            median_distance = (all_list[index][1] + all_list[index + 1][1]) / 2.0
        return median_distance

    def get_point_set(i, all_list, median_distance):
        pointset = set()
        for point in all_list:
            if point[1] < median_distance:
                pointset.add(point[0])
        return pointset

    def get_second_pivot(i, cols, first_pivot_idx, tbl):
        second_pivot_pts = []
        for row in range(0, len(tbl.rows)):
            dist = distance(tbl.rows[first_pivot_idx], tbl.rows[row], cols)
            second_pivot_pts.append((row, dist))
        second_pivot_pts.sort(key=lambda x: x[1])
        second_pivot_idx = second_pivot_pts[math.floor(len(second_pivot_pts) * 0.9)][0]
        return second_pivot_idx, second_pivot_pts

    def get_first_pivot(i, cols, random_point, tbl):
        first_pivot_pts = []
        for row in range(0, len(tbl.rows)):
            dist = distance(tbl.rows[random_point], tbl.rows[row], cols)
            first_pivot_pts.append((row, dist))
        first_pivot_pts.sort(key=lambda x: x[1])
        first_pivot_idx = first_pivot_pts[math.floor(len(first_pivot_pts) * 0.9)][0]
        return first_pivot_idx

    def mapper(i, tbl):
        cols = [tbl.cols[col] for col in tbl.col_info['xs']]
        random_point = random.randint(0, len(tbl.rows) - 1)
        first_pivot_idx = i.get_first_pivot(cols, random_point, tbl)
        second_pivot_idx, second_pivot_pts = i.get_second_pivot(cols, first_pivot_idx, tbl)
        dist = second_pivot_pts[math.floor(len(second_pivot_pts) * 0.9)][1]
        return first_pivot_idx, second_pivot_idx, dist
        
    def get_sorted_all_list(i, pivot_tuple, tbl):
        all_list = []
        cols = [tbl.cols[col] for col in tbl.col_info['xs']]
        for row in range(0, len(tbl.rows)):
            dist = cosine(tbl.rows[pivot_tuple[0]], tbl.rows[pivot_tuple[1]], tbl.rows[row], pivot_tuple[2], cols)
            all_list.append((row, dist))
        all_list.sort(key=lambda x: x[1])
        return all_list

    def best_pivot_points(i,tbl):
        counter = 10
        initial = len(tbl.rows)
        best_tuple = None
        best_points = None
        while counter > 0:
            counter -= 1
            tuple = i.mapper(tbl)
            all_list = i.get_sorted_all_list(tuple, tbl)
            length = len(all_list)
            index = (length - 1) // 2
            median_distance = i.get_mean_distance(all_list, index, length)
            pointset = i.get_point_set(all_list, median_distance)
            right = abs(len(pointset) - (length - len(pointset)))
            if right < initial:
                initial, best_points, best_tuple = right, pointset, tuple
        return best_tuple, best_points


if __name__ == '__main__':
    # hw7 = Hw7('pom310000.csv')
    hw7 = Hw7('xomo10000.csv')
    print_tree(hw7.tree)