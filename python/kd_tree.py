class Node(object):

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent


class KDTree(object):

    def __init__(self, points, k):
        self.n_dim = len(points[0])
        self.k = k
        self.root = self.build(points, 0)

    def build(self, points, depth):
        if len(points) <= self.k:
            return Node(None, left=points)

        axis = depth % self.n_dim

        median = self.median([p[axis] for p in points])
        node = Node(median)

        points_left, points_right = [p for p in points if p[axis] < median], [p for p in points if p[axis] >= median]

        node.left = self.build(points_left, depth + 1)
        node.left.parent = node

        node.right = self.build(points_right, depth + 1)
        node.right.parent = node

        return node

    def median(self, values):
        return values[len(values) // 2]

    def knn(self, point):
        node = self.root

        depth = 0
        while type(node.left) != list:
            axis = depth % self.n_dim
            if point[axis] < node.key:
                node = node.left
            else:
                node = node.right
            depth += 1

        return node.left


if __name__ == '__main__':
    kdtree = KDTree([(2, 3), (3, 1), (6, 2), (6, 4), (3, 9)], k=2)
    print(kdtree.knn((7, 2)))
