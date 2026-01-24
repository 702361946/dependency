#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946

"""JSON 模块单元测试"""
import unittest
import tempfile
import os
import json

from src.dependency.modules._file_operations import *


class TestJson(unittest.TestCase):
    """测试 Json 类的读写功能"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.json = Json(file_save_path=self.temp_dir)

    def tearDown(self):
        for f in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, f))
        os.rmdir(self.temp_dir)

    def test_load_valid_json_dict(self):
        """测试加载有效的 JSON 对象（字典）"""
        data = {"name": "test", "value": 123, "active": True}
        file_path = os.path.join(self.temp_dir, "test.json")
        with open(file_path, "w", encoding="UTF-8") as f:
            json.dump(data, f)

        result = self.json.load("test", filepath=self.temp_dir)
        self.assertTrue(result.ok)
        self.assertEqual(result.v["name"], "test")
        self.assertEqual(result.v["value"], 123)

    def test_load_valid_json_list(self):
        """测试加载有效的 JSON 数组"""
        data = [1, 2, 3, {"nested": "value"}]
        file_path = os.path.join(self.temp_dir, "list.json")
        with open(file_path, "w", encoding="UTF-8") as f:
            json.dump(data, f)

        result = self.json.load("list", filepath=self.temp_dir)
        self.assertTrue(result.ok)
        self.assertEqual(len(result.v), 4)
        self.assertEqual(result.v[3]["nested"], "value")

    def test_load_nonexistent_file(self):
        """测试加载不存在的文件返回失败"""
        result = self.json.load("nonexistent", filepath=self.temp_dir)
        self.assertFalse(result.ok)

    def test_load_invalid_json(self):
        """测试加载无效的 JSON 返回失败"""
        file_path = os.path.join(self.temp_dir, "invalid.json")
        with open(file_path, "w", encoding="UTF-8") as f:
            f.write("{invalid json")

        result = self.json.load("invalid", filepath=self.temp_dir)
        self.assertFalse(result.ok)

    def test_dump_valid_dict(self):
        """测试写入有效的字典"""
        data = {"key": "value", "number": 42}
        result = self.json.dump(data, filename="output", filepath=self.temp_dir)
        self.assertTrue(result.ok)

        file_path = os.path.join(self.temp_dir, "output.json")
        self.assertTrue(os.path.exists(file_path))

        # 验证内容
        with open(file_path, "r", encoding="UTF-8") as f:
            loaded = json.load(f)
        self.assertEqual(loaded["key"], "value")

    def test_dump_valid_list(self):
        """测试写入有效的列表"""
        data = [{"id": 1}, {"id": 2}]
        result = self.json.dump(data, filename="list", filepath=self.temp_dir)
        self.assertTrue(result.ok)

    def test_dump_invalid_type(self):
        """测试写入非字典/列表类型返回失败"""
        # noinspection PyTypeChecker
        result = self.json.dump("not_a_dict_or_list", filename="bad", filepath=self.temp_dir)
        self.assertFalse(result.ok)
        self.assertIsInstance(result.v, TypeError)

    def test_dump_with_indent(self):
        """测试自定义缩进参数"""
        data = {"level1": {"level2": "value"}}
        result = self.json.dump(data, filename="indented", filepath=self.temp_dir, indent=2)
        self.assertTrue(result.ok)

        # 验证文件有缩进
        file_path = os.path.join(self.temp_dir, "indented.json")
        with open(file_path, "r", encoding="UTF-8") as f:
            content = f.read()
        self.assertIn("  ", content)  # 检查缩进空格

    def test_dump_ensure_ascii(self):
        """测试 ensure_ascii 参数处理非 ASCII 字符"""
        data = {"name": "中文测试", "emoji": "🎉"}

        # ensure_ascii=False（默认）
        result = self.json.dump(
            data,
            filename="unicode",
            filepath=self.temp_dir,
            ensure_ascii=False
        )
        self.assertTrue(result.ok)

        file_path = os.path.join(self.temp_dir, "unicode.json")
        with open(file_path, "r", encoding="UTF-8") as f:
            content = f.read()
        self.assertIn("中文测试", content)  # 直接包含中文

        # ensure_ascii=True
        result = self.json.dump(
            data,
            filename="ascii",
            filepath=self.temp_dir,
            ensure_ascii=True
        )
        self.assertTrue(result.ok)

        file_path = os.path.join(self.temp_dir, "ascii.json")
        with open(file_path, "r", encoding="UTF-8") as f:
            content = f.read()
        self.assertIn("\\u4e2d\\u6587", content)  # Unicode 转义

    def test_round_trip(self):
        """测试读写往返一致性"""
        original = {
            "string": "value",
            "number": 3.14,
            "boolean": False,
            "null": None,
            "array": [1, 2, 3],
            "object": {"nested": "data"}
        }

        dump_result = self.json.dump(original, filename="roundtrip",
                                     filepath=self.temp_dir)
        self.assertTrue(dump_result.ok)

        load_result = self.json.load("roundtrip", filepath=self.temp_dir)
        self.assertTrue(load_result.ok)
        self.assertEqual(load_result.v, original)

    def test_add_file_ext_parameter(self):
        """测试 add_file_ext 参数控制后缀添加"""
        data = {"test": "data"}

        # add_file_ext=True（默认）
        result = self.json.dump(data, filename="with_ext", filepath=self.temp_dir)
        self.assertTrue(result.ok)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "with_ext.json")))

        # add_file_ext=False，手动添加后缀
        result = self.json.dump(data, filename="manual.json", filepath=self.temp_dir,
                                add_file_ext=False)
        self.assertTrue(result.ok)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "manual.json")))


if __name__ == "__main__":
    unittest.main()