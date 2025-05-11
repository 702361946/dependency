import os
import importlib

from ._foundation import *

__varsion__ = "0.2.0"
__author__ = "702361946@qq.com"
__license__ = "MIT"

log = Log(
    "dependency",
    log_output_to_file_path=f"{log_path}dependency.log",
)


def load_module(name: str, name_compare: dict[str, str] | None = None):
    """
    加载模块
    :param name: 模块名
    :param name_compare: 可选模块名对照表
    :return: import对象
    """
    if name_compare is None:
        name_compare = {}

    if name in name_compare.keys():
        name = name_compare[name]

    try:
        log.info(f"load {name}")
        return importlib.import_module(
            f'._{name}',
            package=f"{__package__}.modules"
        )
    except Exception as e:
        log.error(e)
        print(f"load {name} error:{e}")
        return False


def list_modules(out_md_file: bool = False) -> list[str]:
    """
    列出所有modules下模块
    此函数仅用于提示该如何from import或import
    同时只有以_为前缀的python包才会列出
    :param out_md_file: 是否在当前运行目录下输出md文件并列出所有带README.md的模块下README.md文件的路径[name](path)
    :return:
    """
    log.info("list modules")

    def out_md_file_all(all_modules: list[str], modules_path: str):
        """

        :param all_modules:
        :param modules_path:
        :return:
        """
        log.info("out md file all")
        readme_files = []
        # 遍历所有模块
        for module in all_modules:
            # 构建模块的完整路径
            module_path = os.path.join(modules_path, f"_{module}")
            # 检查是否存在README.md文件
            readme_path = os.path.join(module_path, "README.md")
            if os.path.exists(readme_path):
                # 将路径转换为绝对路径并统一为 /
                abs_readme_path = os.path.relpath(readme_path).replace("\\", "/")
                # 输出模块名和README.md文件的路径
                readme_files.append(f"[{module}](./{abs_readme_path})")

        with open("_modules.md", "w", encoding="utf-8") as f:
            for readme_file in readme_files:
                f.write(readme_file + "\n")


    modules_dir = os.path.join(
        os.path.dirname(__file__),
        "modules"
    )
    valid_modules = []
    # 获取所有以_开头的文件夹
    for item in os.listdir(modules_dir):
        if item.startswith("_") and os.path.isdir(os.path.join(modules_dir, item)):
            # 检查是否存在__init__.py
            init_file = os.path.join(modules_dir, item, "__init__.py")
            if os.path.isfile(init_file):
                # 去除前缀_并添加到返回列表
                valid_modules.append(item[1:])

    if out_md_file:
        out_md_file_all(valid_modules, modules_dir)

    log.info(f"valid modules:\n{valid_modules}")
    return valid_modules
