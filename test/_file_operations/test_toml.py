#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
"""TOML 模块单元测试"""
import unittest
import tempfile
import os

from src.dependency.modules._file_operations import *


class TestToml(unittest.TestCase):
    """测试 Toml 类的读写功能"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.toml = Toml(file_save_path=self.temp_dir)

    def tearDown(self):
        for f in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, f))
        os.rmdir(self.temp_dir)

    def test_load_valid_toml(self):
        """测试加载有效的 TOML 文件"""
        content = """
[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
server = "192.168.1.1"
ports = [8001, 8001, 8002]
"""
        file_path = os.path.join(self.temp_dir, "test.toml")
        with open(file_path, "w", encoding="UTF-8") as f:
            f.write(content)

        result = self.toml.load("test", filepath=self.temp_dir)
        self.assertTrue(result.ok)
        self.assertEqual(result.v["owner"]["name"], "Tom Preston-Werner")
        self.assertEqual(result.v["database"]["server"], "192.168.1.1")

    def test_load_nonexistent_file(self):
        """测试加载不存在的文件返回失败"""
        result = self.toml.load("nonexistent", filepath=self.temp_dir)
        self.assertFalse(result.ok)

    def test_dump_valid_dict(self):
        """测试写入有效的字典"""
        data = {
            "title": "TOML Example",
            "owner": {"name": "John", "age": 30},
            "items": ["a", "b", "c"]
        }
        result = self.toml.dump(data, filename="output", filepath=self.temp_dir)
        self.assertTrue(result.ok)

        file_path = os.path.join(self.temp_dir, "output.toml")
        self.assertTrue(os.path.exists(file_path))

    def test_dump_invalid_type(self):
        """测试写入非字典/列表类型返回失败"""
        # noinspection PyTypeChecker
        result = self.toml.dump("not_a_dict", filename="bad", filepath=self.temp_dir)
        self.assertFalse(result.ok)
        self.assertIsInstance(result.v, TypeError)

    def test_dump_list_in_table(self):
        """测试在表格内写入数组（TOML支持数组作为值）"""
        data = {
            "items": [{"name": "item1"}, {"name": "item2"}]
        }
        result = self.toml.dump(data, filename="list", filepath=self.temp_dir)
        self.assertTrue(result.ok, f"写入失败: {result.v}")

        # 读回验证
        loaded = self.toml.load("list", filepath=self.temp_dir)
        self.assertTrue(loaded.ok)
        self.assertEqual(len(loaded.v["items"]), 2)
        self.assertEqual(loaded.v["items"][0]["name"], "item1")

    def test_dump_array_value(self):
        """测试数组作为值写入"""
        data = {
            "numbers": [1, 2, 3, 4, 5],
            "strings": ["a", "b", "c"],
            "mixed": [{"key": "val1"}, {"key": "val2"}]
        }
        result = self.toml.dump(data, filename="array", filepath=self.temp_dir)
        self.assertTrue(result.ok)

        loaded = self.toml.load("array", filepath=self.temp_dir)
        self.assertTrue(loaded.ok)
        self.assertEqual(loaded.v["numbers"], [1, 2, 3, 4, 5])

    def test_round_trip(self):
        """测试读写往返一致性"""
        original = {
            "package": {"name": "example", "version": "0.1.0"},
            "dependencies": {"python": ">=3.8", "tomlkit": ">=0.12"}
        }

        dump_result = self.toml.dump(original, filename="roundtrip", filepath=self.temp_dir)
        self.assertTrue(dump_result.ok)

        load_result = self.toml.load("roundtrip", filepath=self.temp_dir)
        self.assertTrue(load_result.ok)
        self.assertEqual(load_result.v["package"]["name"], "example")
        self.assertEqual(load_result.v["dependencies"]["python"], ">=3.8")

    def test_preserve_format(self):
        """测试 tomlkit 保留格式特性"""
        content = """# This is a comment
[section]
key = "value"  # inline comment
"""
        file_path = os.path.join(self.temp_dir, "formatted.toml")
        with open(file_path, "w", encoding="UTF-8") as f:
            f.write(content)

        result = self.toml.load("formatted", filepath=self.temp_dir)
        self.assertTrue(result.ok)

        # 重新写入
        dump_result = self.toml.dump(result.v, filename="formatted_out", filepath=self.temp_dir)
        self.assertTrue(dump_result.ok)


if __name__ == "__main__":
    unittest.main()