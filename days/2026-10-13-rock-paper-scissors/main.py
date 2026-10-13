"""第 2 天：只使用 Python 标准库的命令行石头剪刀布。"""

import random


CHOICES = ("石头", "剪刀", "布")
INPUTS = {"1": "石头", "2": "剪刀", "3": "布", **{name: name for name in CHOICES}}
WINNING_PAIRS = {("石头", "剪刀"), ("剪刀", "布"), ("布", "石头")}


def judge(player, computer):
    """判断一轮结果，双方出拳需为 CHOICES 中的值。"""
    if player == computer:
        return "平局"
    if (player, computer) in WINNING_PAIRS:
        return "胜"
    return "负"


def main():
    stats = {"胜": 0, "负": 0, "平局": 0}
    print("石头剪刀布 · GitHub每日打卡 / 第 2 天")
    print("输入 1（石头）、2（剪刀）、3（布），也可以直接输入中文。输入 q 退出。")

    try:
        while True:
            text = input("\n请出拳：").strip()
            if text.lower() == "q":
                break
            if text not in INPUTS:
                print("输入无效，请输入 1、2、3、石头、剪刀、布或 q。")
                continue

            player = INPUTS[text]
            computer = random.choice(CHOICES)
            result = judge(player, computer)
            stats[result] += 1
            message = {"胜": "你赢了！", "负": "电脑赢了！", "平局": "平局！"}[result]
            print(f"你出了{player}，电脑出了{computer}。{message}")
            print(f"当前战绩：{stats['胜']} 胜 / {stats['负']} 负 / {stats['平局']} 平局")
    except (EOFError, KeyboardInterrupt):
        print("\n输入已结束。")

    rounds = sum(stats.values())
    print(f"\n共完成 {rounds} 轮：{stats['胜']} 胜 / {stats['负']} 负 / {stats['平局']} 平局。下次再来！")


if __name__ == "__main__":
    main()
