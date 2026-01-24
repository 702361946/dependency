#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

# test_f_ini.py
"""INI 模块单元测试"""
import unittest
import tempfile
import os

from src.dependency.modules._file_operations import *


class TestIni(unittest.TestCase):
    """测试 Ini 类的读写功能"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.ini = Ini(file_save_path=self.temp_dir)

    def tearDown(self):
        # 清理临时文件
        for f in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, f))
        os.rmdir(self.temp_dir)

    def test_load_valid_ini(self):
        """测试加载有效的 INI 文件"""
        # 准备测试文件
        content = """[section1]
key1 = value1
key2 = value2

[section2]
key3 = value3
"""
        file_path = os.path.join(self.temp_dir, "test.ini")
        with open(file_path, "w", encoding="UTF-8") as f:
            f.write(content)

        # 加载并验证 - 使用正确的参数名 file_path（下划线）
        result = self.ini.load("test", file_path=self.temp_dir)
        self.assertTrue(result.ok, f"加载失败: {result.v}")
        self.assertEqual(result.v["section1"]["key1"], "value1")
        self.assertEqual(result.v["section2"]["key3"], "value3")

    def test_load_nonexistent_file(self):
        """测试加载不存在的文件返回失败"""
        result = self.ini.load("nonexistent", file_path=self.temp_dir)
        self.assertFalse(result.ok)

    def test_dump_valid_dict(self):
        """测试写入有效的嵌套字典"""
        data = {
            "section1": {"key1": "value1", "key2": "value2"},
            "section2": {"key3": "value3"}
        }
        result = self.ini.dump(data, file_name="output", file_path=self.temp_dir)
        self.assertTrue(result.ok, f"写入失败: {result.v}")

        # 验证文件内容
        file_path = os.path.join(self.temp_dir, "output.ini")
        self.assertTrue(os.path.exists(file_path), "文件未创建")

        # 读回验证
        loaded = self.ini.load("output", file_path=self.temp_dir)
        self.assertTrue(loaded.ok)
        self.assertEqual(loaded.v["section1"]["key1"], "value1")

    def test_dump_invalid_type(self):
        """测试写入非字典类型返回失败"""
        # noinspection PyTypeChecker
        result = self.ini.dump("not_a_dict", file_name="bad", file_path=self.temp_dir)
        self.assertFalse(result.ok)
        self.assertIsInstance(result.v, TypeError)

    def test_dump_empty_dict(self):
        """测试写入空字典"""
        result = self.ini.dump({}, file_name="empty", file_path=self.temp_dir)
        self.assertTrue(result.ok, f"写入失败: {result.v}")

        file_path = os.path.join(self.temp_dir, "empty.ini")
        self.assertTrue(os.path.exists(file_path), "文件未创建")

    def test_round_trip(self):
        """测试读写往返一致性"""
        original = {
            "database": {"host": "localhost", "port": "3306"},
            "app": {"debug": "true", "name": "myapp"}
        }

        # 写入
        dump_result = self.ini.dump(original, file_name="roundtrip", file_path=self.temp_dir, add_file_ext=False)
        self.assertTrue(dump_result.ok)

        # 读取
        load_result = self.ini.load("roundtrip", file_path=self.temp_dir, add_file_ext=False)
        self.assertTrue(load_result.ok)

        # 验证（注意：INI值都是字符串）
        self.assertEqual(load_result.v["database"]["host"], "localhost")
        self.assertEqual(load_result.v["database"]["port"], "3306")


if __name__ == "__main__":
    unittest.main()