#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import sys
import os

# 导包
if True:
    # 获取dependency根路径
    package_path = os.path.dirname( # .\
        os.path.dirname( #.\modules\
            os.path.dirname( # .\modules\.\
                os.path.abspath(__file__) # .\modules\.\_get_package.py
            )
        )
    )

    # 将包路径添加到sys.path
    if package_path not in sys.path:
        sys.path.append(package_path)

    # 导入
    try:
        from _foundation import *
    except ImportError:
        print("无法导入_foundation模块")
        input(f"检查是否被删除或路径错误:{package_path}")