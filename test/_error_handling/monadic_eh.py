#  Copyright (c) 2026.
#  @702361946
#  702361946@qq.com
#  https://github.com/702361946
import unittest
from collections.abc import Callable

from src.dependency.modules._error_handling import MEH


class TestMEH(unittest.TestCase):
    """MEH 单子错误处理类的单元测试"""

    # ========== 构造器测试 ==========

    def test_unit_ok_creates_success(self):
        """unit_ok 创建成功状态"""
        m = MEH.unit_ok(42)
        self.assertTrue(m.ok)
        self.assertEqual(m.v, 42)
        self.assertIsNone(m.e)

    def test_unit_ok_with_none_value(self):
        """unit_ok 允许 None 作为有效值"""
        m = MEH.unit_ok(None)
        self.assertTrue(m.ok)
        self.assertIsNone(m.v)

    def test_unit_err_creates_failure(self):
        """unit_err 创建失败状态"""
        err = ValueError("test error")
        m = MEH.unit_err(err)
        self.assertFalse(m.ok)
        self.assertEqual(m.e, err)
        self.assertIsNone(m.v)

    def test_direct_construction(self):
        """直接构造（不推荐但有效）"""
        m = MEH(v=42, ok=True, e=None)
        self.assertTrue(m.ok)
        self.assertEqual(m.v, 42)

    # ========== bind 测试 ==========

    def test_bind_success_chain(self):
        """bind 成功链式"""
        m = (
            MEH.unit_ok(5)
            .bind(lambda x: MEH.unit_ok(x * 2))
            .bind(lambda x: MEH.unit_ok(x + 1))
        )
        self.assertTrue(m.ok)
        self.assertEqual(m.v, 11)

    def test_bind_short_circuit_on_failure(self):
        """bind 失败时短路"""
        called = [False]

        def should_not_be_called(x):
            called[0] = True
            return MEH.unit_ok(x)

        m = (
            MEH.unit_err(ValueError("first error"))
            .bind(should_not_be_called)
            .bind(should_not_be_called)
        )

        self.assertFalse(m.ok)
        self.assertFalse(called[0])  # 后续函数未执行
        self.assertIsInstance(m.e, ValueError)

    def test_bind_propagates_error(self):
        """bind 传播错误信息"""
        original_err = RuntimeError("original")
        m = MEH.unit_err(original_err).bind(lambda x: MEH.unit_ok(1))
        self.assertFalse(m.ok)
        self.assertEqual(m.e, original_err)

    def test_bind_with_different_types(self):
        """bind 可以转换类型"""
        m = (
            MEH.unit_ok("123")
            .bind(lambda s: MEH.unit_ok(int(s)))
            .bind(lambda n: MEH.unit_ok(n > 0))
        )
        self.assertTrue(m.ok)
        self.assertTrue(m.v)

    def test_bind_func_returns_err(self):
        """bind 中 func 返回错误"""
        m = (
            MEH.unit_ok(5)
            .bind(lambda x: MEH.unit_ok(x * 2))
            .bind(lambda x: MEH.unit_err(ValueError("fail")))
            .bind(lambda x: MEH.unit_ok(x + 1))  # 不会执行
        )
        self.assertFalse(m.ok)
        self.assertIsInstance(m.e, ValueError)

    # ========== map 测试 ==========

    def test_map_success(self):
        """map 成功转换"""
        m = MEH.unit_ok(5).map(lambda x: x * 2)
        self.assertTrue(m.ok)
        self.assertEqual(m.v, 10)

    def test_map_short_circuit(self):
        """map 失败时短路"""
        called = [False]

        def should_not_be_called(x):
            called[0] = True
            return x * 2

        m = MEH.unit_err(ValueError("fail")).map(should_not_be_called)
        self.assertFalse(m.ok)
        self.assertFalse(called[0])

    def test_map_pure_function(self):
        """map 应用纯函数"""
        m = (
            MEH.unit_ok({"name": "Alice", "age": 30})
            .map(lambda d: d["name"])
            .map(str.upper)
            .map(len)
        )
        self.assertTrue(m.ok)
        self.assertEqual(m.v, 5)  # "ALICE" 长度

    def test_map_exception_to_error(self):
        """map 捕获异常转为错误"""
        m = MEH.unit_ok("abc").map(int)  # int("abc") 抛出 ValueError
        self.assertFalse(m.ok)
        self.assertIsInstance(m.e, ValueError)

    def test_map_attribute_error(self):
        """map 捕获 AttributeError"""
        m = MEH.unit_ok(None).map(lambda x: x.upper())
        self.assertFalse(m.ok)
        self.assertIsInstance(m.e, AttributeError)

    def test_map_type_error_for_meh_return(self):
        """map 禁止返回 MEH（强制用 bind）"""
        with self.assertRaises(TypeError) as ctx:
            MEH.unit_ok(5).map(lambda x: MEH.unit_ok(x * 2))

        self.assertIn("MEH", str(ctx.exception))

    def test_map_type_error_message(self):
        """map 类型错误提示信息"""
        with self.assertRaises(TypeError) as ctx:
            MEH.unit_ok(5).map(lambda x: MEH.unit_err(ValueError("test")))

        err_msg = str(ctx.exception)
        self.assertIn("func", err_msg.lower())
        self.assertIn("map", err_msg.lower())

    # ========== bind + map 混合测试 ==========

    def test_mixed_bind_and_map(self):
        """bind 和 map 混用"""

        def fetch_user(uid: str) -> MEH:
            if uid == "0":
                return MEH.unit_err(ValueError("not found"))
            return MEH.unit_ok({"id": uid, "name": "User" + uid})

        def get_email(user: dict) -> str:
            return user["id"] + "@example.com"

        def validate_email(email: str) -> MEH:
            if "@" not in email:
                return MEH.unit_err(ValueError("invalid email"))
            return MEH.unit_ok(email.lower())

        m = (
            fetch_user("123")
            .map(get_email)  # 纯提取
            .bind(validate_email)  # 验证（可能失败）
            .map(lambda e: e.split("@")[0])  # 纯转换
        )
        self.assertTrue(m.ok)
        self.assertEqual(m.v, "123")

    def test_mixed_chain_failure(self):
        """混合链式中途失败"""
        m = (
            MEH.unit_ok(10)
            .map(lambda x: x * 2)  # 20
            .bind(lambda x: MEH.unit_err(RuntimeError("fail")))
            .map(lambda x: x + 1)  # 不会执行
        )
        self.assertFalse(m.ok)
        self.assertIsInstance(m.e, RuntimeError)

    # ========== 复杂场景测试 ==========

    def test_nested_meh_not_created(self):
        """确保不会产生嵌套 MEH"""
        # 正确使用 bind 不会嵌套
        m1 = MEH.unit_ok(5).bind(lambda x: MEH.unit_ok(x * 2))
        self.assertTrue(m1.ok)
        self.assertEqual(m1.v, 10)
        self.assertNotIsInstance(m1.v, MEH)

    def test_error_recovery_not_allowed(self):
        """MEH 不允许错误恢复（单子的单向性）"""
        m = (
            MEH.unit_err(ValueError("fail"))
            .bind(lambda x: MEH.unit_ok("recovered"))  # 不会执行
        )
        self.assertFalse(m.ok)
        # 错误状态持续，没有"恢复"机制

    def test_zero_value_handling(self):
        """处理零值（0, False, "" 等）"""
        m1 = MEH.unit_ok(0).map(lambda x: x + 1)
        self.assertTrue(m1.ok)
        self.assertEqual(m1.v, 1)

        m2 = MEH.unit_ok(False).map(lambda x: not x)
        self.assertTrue(m2.ok)
        self.assertTrue(m2.v)

        m3 = MEH.unit_ok("").map(len)
        self.assertTrue(m3.ok)
        self.assertEqual(m3.v, 0)

    def test_exception_in_bind_not_caught(self):
        """bind 不捕获异常（由 func 自己处理）"""

        def bad_func(x):
            x += 1
            raise RuntimeError("unexpected")

        # bind 本身不捕获，异常会抛出
        with self.assertRaises(RuntimeError):
            MEH.unit_ok(5).bind(bad_func)

    # ========== 边界情况 ==========

    def test_empty_chain(self):
        """空链式（只有构造）"""
        m = MEH.unit_ok(42)
        self.assertTrue(m.ok)
        self.assertEqual(m.v, 42)

    def test_single_bind(self):
        """单步 bind"""
        m = MEH.unit_ok(5).bind(lambda x: MEH.unit_ok(str(x)))
        self.assertTrue(m.ok)
        self.assertEqual(m.v, "5")

    def test_single_map(self):
        """单步 map"""
        m = MEH.unit_ok(5).map(str)
        self.assertTrue(m.ok)
        self.assertEqual(m.v, "5")

    def test_chained_errors(self):
        """多次错误不会覆盖"""
        m = (
            MEH.unit_ok(1)
            .bind(lambda x: MEH.unit_err(ValueError("first")))
            .bind(lambda x: MEH.unit_err(RuntimeError("second")))
        )
        self.assertFalse(m.ok)
        self.assertIsInstance(m.e, ValueError)  # 保留第一个错误
        self.assertEqual(str(m.e), "first")


class TestMEHIntegration(unittest.TestCase):
    """集成测试：模拟真实业务场景"""

    def test_user_registration_flow(self):
        """用户注册流程"""

        def validate_username(name: str) -> MEH:
            if len(name) < 3:
                return MEH.unit_err(ValueError("用户名太短"))
            return MEH.unit_ok(name.lower())

        def check_duplicate(name: str) -> MEH:
            if name == "admin":
                return MEH.unit_err(ValueError("用户名已存在"))
            return MEH.unit_ok(name)

        def create_user(name: str) -> MEH:
            return MEH.unit_ok({"id": "123", "username": name})

        # 成功流程
        result = (
            MEH.unit_ok("Alice")
            .bind(validate_username)
            .bind(check_duplicate)
            .bind(create_user)
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.v["username"], "alice")

        # 验证失败
        fail1 = MEH.unit_ok("Al").bind(validate_username)
        self.assertFalse(fail1.ok)

        # 重复检查失败
        fail2 = MEH.unit_ok("Admin").bind(validate_username).bind(check_duplicate)
        self.assertFalse(fail2.ok)

    def test_calculator_with_error_handling(self):
        """带错误处理的计算器"""

        def safe_divide(divisor: float) -> Callable[[float], MEH]:
            """柯里化除法：先接收除数，返回接收被除数的函数"""

            def divide(dividend: float) -> MEH:
                if divisor == 0:
                    return MEH.unit_err(ZeroDivisionError("不能除以零"))
                return MEH.unit_ok(dividend / divisor)

            return divide

        def add_ten(x: float) -> float:
            return x + 10

        # 成功: 100 / 5 = 20, +10 = 30
        result = MEH.unit_ok(100).bind(safe_divide(5)).map(add_ten)
        self.assertTrue(result.ok)
        self.assertEqual(result.v, 30.0)  # 100 / 5 = 20, 20 + 10 = 30

        # 失败: 除以零
        fail = MEH.unit_ok(100).bind(safe_divide(0)).map(add_ten)
        self.assertFalse(fail.ok)
        self.assertIsInstance(fail.e, ZeroDivisionError)


if __name__ == "__main__":
    unittest.main()