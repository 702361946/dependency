#  Copyright (c) 2024-2025.
#  702361946@qq.com(https://github.com/702361946)

import os
import platform

# 检查操作系统,以及处理路径
os_name = (os.name, platform.system())
"""
0: os.name
1: platform.system()
"""

if os_name[1] == "":
    print(f"ERROR:无法识别的操作系统:{os_name}")
    input("请向702361946@qq.com提交控制台输出")
    exit(1)
