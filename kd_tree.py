## 本代码为手写kd树和树搜索来实现KNN算法

import json
import numpy as np

# 首先定义节点，构建树结构的基础
class Node:
    """节点类"""

    def __init__(self, value, index, left_child, right_child):
        self.value = value.tolist()
        self.index = index
        self.left_child = left_child
        self.right_child = right_child

    def __repr__(self):
        return json.dumps(self, indent=3, default=lambda obj: obj.__dict__, ensure_ascii=False)
        # json.dumps函数是用来把传入的对象（这里是Node本身）转化成json的数据格式输出，indent规定缩进字符数，default为一个处理对象的函数，
        # ensure_ascii这里设置表示允许显示中文，obj.__dict__表示以字典的形式返回类属性


class KDTree:
    """kd tree类"""

    def __init__(self, data):
        # 数据集
        self.data = np.asarray(data)
        # kd树
        self.kd_tree = None
        # 创建平衡kd树
        self._create_kd_tree(data)

    def _split_sub_tree(self, data, depth=0):
        # 算法3.2第3步：直到子区域没有实例存在时停止
        if len(data) == 0:
            return None
        # 算法3.2第2步：选择切分坐标轴, 从0开始（书中是从1开始）
        l = depth % data.shape[1]       # 这一步代码很巧妙，随着深度的加深，可以自动选定切分轴
        # 对数据进行排序
        data = data[data[:, l].argsort()]   # 对第0列的值进行排序，然后根据index按行重排data
        # 算法3.2第1步：将所有实例坐标的中位数作为切分点
        median_index = data.shape[0] // 2
        # 获取结点在原数据集中的位置
        node_index = [i for i, v in enumerate(self.data) if list(v) == list(data[median_index])]
        return Node(
            # 本结点
            value=data[median_index],
            # 本结点在数据集中的位置
            index=node_index[0],
            # 左子结点
            left_child=self._split_sub_tree(data[:median_index], depth + 1),
            # 右子结点
            right_child=self._split_sub_tree(data[median_index + 1:], depth + 1)
        )

    def _create_kd_tree(self, X):
        self.kd_tree = self._split_sub_tree(X)

    def query(self, data, k=1):
        data = np.asarray(data)
        hits = self._search(data, self.kd_tree, k=k, k_neighbor_sets=list())
        dd = np.array([hit[0] for hit in hits])
        ii = np.array([hit[1] for hit in hits])
        return dd, ii

    def __repr__(self):
        return str(self.kd_tree)

    @staticmethod
    def _cal_node_distance(node1, node2):
        """计算两个结点之间的距离"""
        return np.sqrt(np.sum(np.square(node1 - node2)))    # 欧式距离

    ## kd-tree搜索算法，很关键！！！！
    def _search(self, point, tree=None, k=1, k_neighbor_sets=None, depth=0):
        if k_neighbor_sets is None:
            k_neighbor_sets = []     # 创建一个空列表存储邻接点坐标
        if tree is None:
            return k_neighbor_sets

        # (1)找到包含目标点x的叶结点
        if tree.left_child is None and tree.right_child is None:
            # 更新当前k近邻点集
            return self._update_k_neighbor_sets(k_neighbor_sets, k, tree, point)

        # 递归地向下访问kd树
        # 这里实际上设置要查找的point点的维度是2
        if point[0][depth % k] < tree.value[depth % k]:
            direct = 'left'
            next_branch = tree.left_child
        else:
            direct = 'right'
            next_branch = tree.right_child
        if next_branch is not None:
            # (3)(a) 判断当前结点，并更新当前k近邻点集
            k_neighbor_sets = self._update_k_neighbor_sets(k_neighbor_sets, k, next_branch, point)
            # (3)(b)检查另一子结点对应的区域是否相交
            if direct == 'left':
                node_distance = self._cal_node_distance(point, tree.right_child.value)
                if k_neighbor_sets[0][0] > node_distance:
                    # 如果相交，递归地进行近邻搜索
                    return self._search(point, tree=tree.right_child, k=k, depth=depth + 1,
                                        k_neighbor_sets=k_neighbor_sets)
            else:
                node_distance = self._cal_node_distance(point, tree.left_child.value)
                if k_neighbor_sets[0][0] > node_distance:
                    return self._search(point, tree=tree.left_child, k=k, depth=depth + 1,
                                        k_neighbor_sets=k_neighbor_sets)

        return self._search(point, tree=next_branch, k=k, depth=depth + 1, k_neighbor_sets=k_neighbor_sets)

    def _update_k_neighbor_sets(self, best, k, tree, point):
        # 计算目标点与当前结点的距离
        node_distance = self._cal_node_distance(point, tree.value)
        if len(best) == 0:   # 如果邻接点集合里面是空的则添加当前节点进去
            best.append((node_distance, tree.index, tree.value))
        elif len(best) < k:
            # 如果“当前k近邻点集”元素数量小于k
            self._insert_k_neighbor_sets(best, tree, node_distance)
        else:
            # 叶节点距离小于“当前 𝑘 近邻点集”中最远点距离
            if best[0][0] > node_distance:
                best = best[1:]
                self._insert_k_neighbor_sets(best, tree, node_distance)
        return best

    @staticmethod
    def _insert_k_neighbor_sets(best, tree, node_distance):
        """将距离最远的结点排在前面"""
        n = len(best)
        for i, item in enumerate(best):
            if item[0] < node_distance:
                # 将距离最远的结点插入到前面
                best.insert(i, (node_distance, tree.index, tree.value))
                break
        if len(best) == n:
            best.append((node_distance, tree.index, tree.value))


def print_k_neighbor_sets(k, ii, dd):
    if k == 1:
        text = "x点的最近邻点是"
    else:
        text = "x点的%d个近邻点是" % k

    for i, index in enumerate(ii):
        res = X_train[index]
        if i == 0:
            text += str(tuple(res))
        else:
            text += ", " + str(tuple(res))

    if k == 1:
        text += "，距离是"
    else:
        text += "，距离分别是"
    for i, dist in enumerate(dd):
        if i == 0:
            text += "%.4f" % dist
        else:
            text += ", %.4f" % dist

    print(text)


if __name__ == '__main__':
    import numpy as np

    X_train = np.array([[2, 3],
                        [5, 4],
                        [9, 6],
                        [4, 7],
                        [8, 1],
                        [7, 2]])
    kd_tree = KDTree(X_train)
    k = 3
    dists, indices = kd_tree.query(np.array([[3, 4.5]]), k=k)
    print_k_neighbor_sets(k, indices, dists)
    print(kd_tree)

    