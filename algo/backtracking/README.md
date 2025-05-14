# 回溯算法

回溯算法（backtracking algorithm）是一种通过穷举来解决问题的方法，它的核心思想是从一个初始状态出发，暴力搜索所有可能的解决方案，当遇到正确的解则将其记录，直到找到解或者尝试了所有可能的选择都无法找到解为止。
回溯算法通常采用“深度优先搜索”来遍历解空间。

https://www.hello-algo.com/chapter_backtracking/backtracking_algorithm/

回溯算法本质上是一种深度优先搜索算法，它尝试所有可能的解决方案直到找到满足条件的解。这种方法的优点在于能够找到所有可能的解决方案，而且在合理的剪枝操作下，具有很高的效率。

然而，在处理大规模或者复杂问题时，回溯算法的运行效率可能难以接受。

时间：回溯算法通常需要遍历状态空间的所有可能，时间复杂度可以达到指数阶或阶乘阶。
空间：在递归调用中需要保存当前的状态（例如路径、用于剪枝的辅助变量等），当深度很大时，空间需求可能会变得很大。
即便如此，回溯算法仍然是某些搜索问题和约束满足问题的最佳解决方案。对于这些问题，由于无法预测哪些选择可生成有效的解，因此我们必须对所有可能的选择进行遍历。在这种情况下，关键是如何优化效率，常见的效率优化方法有两种。

剪枝：避免搜索那些肯定不会产生解的路径，从而节省时间和空间。
启发式搜索：在搜索过程中引入一些策略或者估计值，从而优先搜索最有可能产生有效解的路径。

回溯算法可用于解决许多搜索问题、约束满足问题和组合优化问题。

搜索问题：这类问题的目标是找到满足特定条件的解决方案。

- 全排列问题：给定一个集合，求出其所有可能的排列组合。
- 子集和问题：给定一个集合和一个目标和，找到集合中所有和为目标和的子集。
- 汉诺塔问题：给定三根柱子和一系列大小不同的圆盘，要求将所有圆盘从一根柱子移动到另一根柱子，每次只能移动一个圆盘，且不能将大圆盘放在小圆盘上。

约束满足问题：这类问题的目标是找到满足所有约束条件的解。

- n 皇后：在 n * n 的棋盘上放置 n 个皇后，使得它们互不攻击。
- 数独：在 9 * 9 的网格中填入数字 1 ~ 9，使得每行、每列和每个 3 * 3 子网格中的数字不重复。
- 图着色问题：给定一个无向图，用最少的颜色给图的每个顶点着色，使得相邻顶点颜色不同。

组合优化问题：这类问题的目标是在一个组合空间中找到满足某些条件的最优解。

- 0-1 背包问题：给定一组物品和一个背包，每个物品有一定的价值和重量，要求在背包容量限制内，选择物品使得总价值最大。
- 旅行商问题：在一个图中，从一个点出发，访问所有其他点恰好一次后返回起点，求最短路径。
- 最大团问题：给定一个无向图，找到最大的完全子图，即子图中的任意两个顶点之间都有边相连。

请注意，对于许多组合优化问题，回溯不是最优解决方案。

0-1 背包问题通常使用动态规划解决，以达到更高的时间效率。
旅行商是一个著名的 NP-Hard 问题，常用解法有遗传算法和蚁群算法等。
最大团问题是图论中的一个经典问题，可用贪心算法等启发式算法来解决。

## 尝试与回退

在二叉树中搜索所有值为 7 的节点，请返回根节点到这些节点的路径。

```sh
python preorder_traversal.py
```

```py
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
```

## 剪枝

在二叉树中搜索所有值为 7 的节点，请返回根节点到这些节点的路径，并要求路径中不包含值为 3 的节点。

使用模板代码实现

```sh
python preorder_backtrack.py
```

```py
def is_solution(state: list[TreeNode]) -> bool:
    """判断当前状态是否为解"""
    return state and state[-1].val == 7

def record_solution(state: list[TreeNode], res: list[list[TreeNode]]):
    """记录解"""
    res.append(list(state))

def is_valid(state: list[TreeNode], choice: TreeNode) -> bool:
    """判断在当前状态下，该选择是否合法"""
    return choice is not None and choice.val != 3

def make_choice(state: list[TreeNode], choice: TreeNode):
    """更新状态"""
    state.append(choice)

def undo_choice(state: list[TreeNode], choice: TreeNode):
    """恢复状态"""
    state.pop()

def backtrack(
    state: list[TreeNode], choices: list[TreeNode], res: list[list[TreeNode]]
):
    # 检查是否为解
    if is_solution(state):
        # 记录解
        record_solution(state, res)
    # 遍历所有选择，这里循环相当于走树的不同分支
    for choice in choices:             
        # 剪枝：检查选择是否合法
        if is_valid(state, choice):
            # 尝试：做出选择，更新状态
            make_choice(state, choice)
            # 进行下一轮选择
            backtrack(state, [choice.left, choice.right], res)
            # 回退：撤销选择，恢复到之前的状态
            undo_choice(state, choice)
```

## 全排列问题

全排列问题是回溯算法的一个典型应用。它的定义是在给定一个集合（如一个数组或字符串）的情况下，找出其中元素的所有可能的排列。

### 无相等元素的情况

输入一个整数数组，其中不包含重复元素，返回所有可能的排列。

从回溯算法的角度看，我们可以把生成排列的过程想象成一系列选择的结果。
假设输入数组为 [1,2,3]，如果我们先选择 1，再选择 3，最后选择 2，则获得排列 [1,3,2]。回退表示撤销一个选择，之后继续尝试其他选择。

从回溯代码的角度看，候选集合 choices 是输入数组中的所有元素，状态 state 是直至目前已被选择的元素。
请注意，每个元素只允许被选择一次，因此 state 中的所有元素都应该是唯一的。

为了实现每个元素只被选择一次，我们考虑引入一个布尔型数组 selected ，其中 selected[i] 表示 choices[i] 是否已被选择，并基于它实现以下剪枝操作。

- 在做出选择 choice[i] 后，我们就将 selected[i] 赋值为 True，代表它已被选择。
- 遍历选择列表 choices 时，跳过所有已被选择的节点，即剪枝。

### 考虑相等元素的情况

输入一个整数数组，数组中可能包含重复元素，返回所有不重复的排列。

假设输入数组为 [1,1,2]，在第一轮中，选择 1 或选择 1` 是等价的，在这两个选择之下生成的所有排列都是重复的。因此应该把 1` 剪枝。
同理，在第一轮选择 2 之后，第二轮选择中的 1 和 1` 也会产生重复分支，因此也应将第二轮的 1` 剪枝。
从本质上看，我们的目标是在某一轮选择中，保证多个相等的元素仅被选择一次。

```sh
python3 permutations.py     
```

```py
def backtrack(state: list[int], choices: list[int], selected: list[bool], res: list[list[int]]):
    if len(state) == len(choices):
        res.append(list(state))
        return
    duplicated = set[int]()
    for i, choice in enumerate(choices):
        if selected[i]:
            continue
        if choice in duplicated:
            continue
        duplicated.add(choice)
        selected[i] = True
        state.append(choice)
        backtrack(state, choices, selected, res)
        selected[i] = False
        state.pop()
```