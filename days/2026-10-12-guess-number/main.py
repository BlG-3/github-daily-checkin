"""第 1 天：一个只使用 Python 标准库的命令行猜数字游戏。"""

import random


def play_round():
    """玩一轮；猜中返回 True，主动退出返回 False。"""
    answer = random.randint(1, 100)
    attempts = 0
    print("\n我想好了一个 1～100 的整数。输入 q 可以随时退出。")

    while True:
        text = input("你的猜测：").strip()
        if text.lower() == "q":
            print(f"本轮答案是 {answer}。下次再来！")
            return False

        try:
            guess = int(text)
        except ValueError:
            print("请输入整数，例如 42。")
            continue

        if not 1 <= guess <= 100:
            print("数字要在 1～100 之间。")
            continue

        attempts += 1
        if guess < answer:
            print("猜小了，再大一点！")
        elif guess > answer:
            print("猜大了，再小一点！")
        else:
            print(f"猜对了！答案是 {answer}，你用了 {attempts} 次有效猜测。")
            return True


def main():
    print("🎯 猜数字 · GitHub每日打卡 / 第 1 天")
    try:
        while play_round():
            if input("再玩一轮？输入 y 继续，其他输入退出：").strip().lower() != "y":
                break
    except (EOFError, KeyboardInterrupt):
        print("\n游戏已结束。")


if __name__ == "__main__":
    main()
