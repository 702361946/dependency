#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

import unittest
from pathlib import Path

from src.dependency.modules._file_operations import *


class TestCSV(unittest.TestCase):
    """CSV的单元测试"""

    def setUp(self):
        self.path = Path("test/temp_files")
        self.path.mkdir(parents=True, exist_ok=True)
        self.csv = CSV(file_save_path=str(self.path))

    def tearDown(self):
        """

        """
        # 清理文件
        for p in self.path.iterdir():
            p.unlink(missing_ok=True)

    # ---------- 正常读写 ----------
    def test_round_trip_simple(self):
        data = [["id", "name"], ["1", "Alice"], ["2", "Bob"]]
        file = "test_simple"

        # 写
        ok = self.csv.dump(data, filename=file, add_file_ext=True)
        self.assertTrue(ok, "dump 应成功返回 True")

        # 读
        rv: ReturnValue = self.csv.load(filename=file, add_file_ext=True)
        self.assertTrue(rv.ok, "load 应成功")
        self.assertEqual(rv.v, data, "读出的数据应与写入一致")

    # ---------- 脏数据 ----------
    def test_quoted_comma_newline(self):
        data = [["header"], ['a,bc"d', "x\ny"], ["正常"]]
        file = "dirty"

        self.csv.dump(data, filename=file)
        rv = self.csv.load(filename=file)
        self.assertTrue(rv.ok)
        self.assertEqual(rv.v, data)

    # ---------- 空矩阵 ----------
    def test_empty_matrix(self):
        data = []
        file = "empty_matrix"

        self.csv.dump(data, filename=file)
        rv = self.csv.load(filename=file)
        self.assertTrue(rv.ok)
        self.assertEqual(rv.v, data)

    # ---------- 空文件 ----------
    def test_empty_file(self):
        # 让 CSV 自己写空文件
        self.csv.dump([], filename="empty")
        rv = self.csv.load(filename="empty")
        self.assertTrue(rv.ok)
        self.assertEqual(rv.v, [])

    # ---------- 异常：写入非 list ----------
    def test_dump_type_error(self):
        # noinspection PyTypeChecker
        ok = self.csv.dump("not_a_list", filename="bad")
        self.assertFalse(ok, "写入非 list 应返回 False")

    # ---------- 异常：文件不存在 ----------
    def test_load_not_exist(self):
        rv = self.csv.load(filename="no_such_file")
        self.assertFalse(rv.ok, "文件不存在时应返回 ok=False")

    # ---------- 编码：UTF-8 含中文 ----------
    def test_utf8_chinese(self):
        data = [["城市", "人口"], ["北京", "2189"], ["上海", "2487"]]
        file = "cn"

        self.csv.dump(data, filename=file, encoding="utf-8")
        rv = self.csv.load(filename=file, encoding="utf-8")
        self.assertTrue(rv.ok)
        self.assertEqual(rv.v, data)

    # ---------- Interpreter 直接调用 ----------
    def test_interface_r(self):
        raw = 'a,b\r\n"hello,world",123\r\n'
        rv = self.csv.interpreter(raw, mode="r")
        self.assertTrue(rv.ok)
        self.assertEqual(rv.v, [["a", "b"], ["hello,world", "123"]])

    def test_interface_w(self):
        data = [["x", "y"], ["1", "2"]]
        rv = self.csv.interpreter(data, mode="w")
        self.assertTrue(rv.ok)
        self.assertIsInstance(rv.v, str)
        # 二次读取验证
        rv2 = self.csv.interpreter(rv.v, mode="r")
        self.assertEqual(rv2.v, data)


if __name__ == "__main__":
    unittest.main()