# 概述

基于 Python 标准库 `tkinter` 的封装模块

提供了封装完的窗口管理方法

用于开发 tkinter 程序

但由于目前仍处于开发阶段

工具较少

如果有需要请联系702361946@qq.com更新

# 窗口

1. 创建窗口

   `Window()`

2. 窗口工具

   `.close()`

   `withdraw()`

   `deiconify()`

   `run()`

3. 组件工具

   `.button()`

   `.message()`

   `.entry()`

# 组件
所有组件实现均靠_component.py

以Frame为框架来管理

所以实际上你可以通过管理Frame大小来控制组件展示区域

可以通过deploy方法部署

# 注意事项
## 窗口获取
已创建完成的tk窗口可以从Window.window中获取

## log
log默认情况下在.\\log\\tkinter.txt中

同时如果要替换log控制器

可以在创建时传参log = xxx

xxx可以为带有.info, .error, .warning, .debug, .critical方法的对象


