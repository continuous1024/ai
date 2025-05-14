def backtrack_no_repeat(state: list[int], choices: list[int], selected: list[bool], res: list[list[int]]):
    """回溯"""
    if len(state) == len(choices):
        res.append(list(state))
        return
    for i, choice in enumerate(choices):
        if selected[i]:
            continue
        selected[i] = True
        state.append(choice)
        backtrack_no_repeat(state, choices, selected, res)
        selected[i] = False
        state.pop()

def permutations_no_repeat(nums: list[int]) -> list[list[int]]:
    """生成排列"""
    res = list[list[int]]()
    backtrack_no_repeat(state=[], choices=nums, selected=[False] * len(nums), res=res)
    return res

def backtrack(state: list[int], choices: list[int], selected: list[bool], res: list[list[int]]):
    """回溯"""
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

def permutations(nums: list[int]) -> list[list[int]]:
    """生成排列"""
    res = list[list[int]]()
    backtrack(state=[], choices=nums, selected=[False] * len(nums), res=res)
    return res


if __name__ == "__main__":
    # 初始化列表
    nums = [1, 2, 3]
    # 调用函数
    res = permutations_no_repeat(nums)
    print(res)
    
    # 初始化列表
    nums = [1, 1, 2]
    # 调用函数
    res = permutations(nums)
    print(res)