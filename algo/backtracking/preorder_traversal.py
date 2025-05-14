class TreeNode:
    """二叉树节点类"""

    def __init__(self, val: int = 0):
        self.val: int = val  # 节点值
        self.left: TreeNode | None = None  # 左子节点引用
        self.right: TreeNode | None = None  # 右子节点引用

def list_to_tree_dfs(arr: list[int], i: int) -> TreeNode | None:
    """将列表反序列化为二叉树：递归"""
    # 如果索引超出数组长度，或者对应的元素为 None ，则返回 None
    if i < 0 or i >= len(arr) or arr[i] is None:
        return None
    # 构建当前节点
    root = TreeNode(arr[i])
    # 递归构建左右子树
    root.left = list_to_tree_dfs(arr, 2 * i + 1)
    root.right = list_to_tree_dfs(arr, 2 * i + 2)
    return root

def list_to_tree(arr: list[int]) -> TreeNode | None:
    """将列表反序列化为二叉树"""
    return list_to_tree_dfs(arr, 0)


def pre_order(root: TreeNode):
    if root is None:
        return
    if root.val == 7:
        # 记录解
        res.append(root)
    pre_order(root.left)
    pre_order(root.right)


def pre_order_path(root: TreeNode):
    # 剪枝
    if root is None:
        return
    # 尝试
    path.append(root)
    if root.val == 7:
        # 记录解
        pathRes.append(list(path))
    pre_order_path(root.left)
    pre_order_path(root.right)
    # 回退
    path.pop()

"""Driver Code"""
if __name__ == "__main__":
    root = list_to_tree([1, 7, 3, 4, 5, 6, 7])

    # 前序遍历
    res = list[TreeNode]()
    pre_order(root)
    print("\n输出所有值为 7 的节点")
    print([node.val for node in res])

    path = list[TreeNode]()
    pathRes = list[list[TreeNode]]()
    pre_order_path(root)
    print("\n输出所有根节点到节点 7 的路径")
    for path in pathRes:
        print([node.val for node in path])
