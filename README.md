# 环境

python 3.12+

# 依赖

# 调用方法

`import dependency`

`from dependency import *`

# 功能

请详细参阅每个包下的readme.md

其中foundation是此包的基础,默认导入

# 加载

使用load_module加载模块

其中传参为模块名

返回值等同于import

但只会加载modules目录下的模块

允许传入对照表

对照表为一个字典,键为模块的别名,值为模块真名

# 模块编写事项
在modules目录下新建一个文件夹

用sys返回基础路径并找到基础包_foundation

可以通过复制其他包内的get_package.py并from import直接获取

请手动测试是否正常导入

需要注意包名前面要加_

否则load_module函数会找不到此包并返回False
