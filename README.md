# 环境

python 3.12+

# 依赖

# 调用方法

`import dependency`

`from dependency import *`

# 功能

请详细参阅每个包下的readme.md

其中foundation是此包的基础,默认导入

# json配置

```json
{
    "自定义包名": {
        "load": "是否导入'True/False',一定要是bool类型",
        "name": "原包名(不必带_)"
    }
}
```
如
```json
{
    "tkinter": {
        "load": false,
        "name": "tkinter"
    }
}
```

# 输出

在modules字典中

```json
{
    "自定义包名": "导入成功的包或False"
}
```

需要注意变量要以.访问,而非key

如`modules["xxx"].xxx`

# 模块编写事项
在modules目录下新建一个文件夹

用sys返回基础路径并找到基础包_foundation

基于_foundation(或其他包)基础进行拓展

请手动测试是否正常导入

需要注意包名前面要加_
