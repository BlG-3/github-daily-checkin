"""使用标准库 unittest 验证游戏规则和交互流程。"""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main as game


class GameTests(unittest.TestCase):
    def run_game(self, inputs, computers=()):
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs), patch.object(
            game.random, "choice", side_effect=computers
        ) as choose, redirect_stdout(output):
            game.main()
        return output.getvalue(), choose.call_count

    def test_all_nine_matchups(self):
        expected = (
            ("平局", "胜", "负"),
            ("负", "平局", "胜"),
            ("胜", "负", "平局"),
        )
        for i, player in enumerate(game.CHOICES):
            for j, computer in enumerate(game.CHOICES):
                with self.subTest(player=player, computer=computer):
                    self.assertEqual(game.judge(player, computer), expected[i][j])

    def test_numeric_and_chinese_inputs(self):
        for text, name in (("1", "石头"), ("2", "剪刀"), ("3", "布"),
                           ("石头", "石头"), ("剪刀", "剪刀"), ("布", "布")):
            with self.subTest(text=text):
                output, calls = self.run_game([f" {text} ", "q"], [name])
                self.assertIn(f"你出了{name}，电脑出了{name}。平局！", output)
                self.assertIn("共完成 1 轮：0 胜 / 0 负 / 1 平局", output)
                self.assertEqual(calls, 1)

    def test_multiple_rounds_and_statistics(self):
        output, calls = self.run_game(["1", "2", "布", "q"], ["剪刀", "石头", "布"])
        self.assertIn("你赢了！", output)
        self.assertIn("电脑赢了！", output)
        self.assertIn("共完成 3 轮：1 胜 / 1 负 / 1 平局", output)
        self.assertEqual(calls, 3)

    def test_invalid_inputs_do_not_count(self):
        output, calls = self.run_game(["", "   ", "0", "4", "abc", "1.0", "q"])
        self.assertEqual(output.count("输入无效"), 6)
        self.assertIn("共完成 0 轮", output)
        self.assertEqual(calls, 0)

    def test_immediate_quit(self):
        output, calls = self.run_game([" Q "])
        self.assertIn("共完成 0 轮", output)
        self.assertEqual(calls, 0)

    def test_eof_and_ctrl_c_preserve_statistics(self):
        for error in (EOFError(), KeyboardInterrupt()):
            with self.subTest(error=type(error).__name__):
                output, calls = self.run_game(["1", error], ["剪刀"])
                self.assertIn("输入已结束", output)
                self.assertIn("共完成 1 轮：1 胜 / 0 负 / 0 平局", output)
                self.assertEqual(calls, 1)


if __name__ == "__main__":
    unittest.main()
