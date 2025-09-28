| 事件名称                | 事件代码  | 描述           | 主要属性                                                                                                                                 |
|---------------------|-------|--------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `KeyDown`           | 768   | 按键按下事件       | `unicode`: 按键对应的 Unicode 字符<br>`key`: 按键键值<br>`mod`: 修饰键状态<br>`scancode`: 扫描码<br>`window`: 窗口对象                                      |
| `KeyUp`             | 769   | 按键释放事件       | `unicode`: 按键对应的 Unicode 字符<br>`key`: 按键键值<br>`mod`: 修饰键状态<br>`scancode`: 扫描码<br>`window`: 窗口对象                                      |
| `TextInput`         | 771   | 文本输入事件       | `text`: 输入的文本内容<br>`window`: 窗口对象                                                                                                    |
| `MouseMotion`       | 1024  | 鼠标移动事件       | `pos`: 鼠标当前位置 `(x, y)`<br>`rel`: 鼠标相对移动 `(dx, dy)`<br>`buttons`: 鼠标按键状态 `(left, middle, right)`<br>`touch`: 是否触摸事件<br>`window`: 窗口对象 |
| `MouseButtonDown`   | 1025  | 鼠标按键按下事件     | `pos`: 鼠标当前位置 `(x, y)`<br>`button`: 按下的鼠标按钮编号<br>`touch`: 是否触摸事件<br>`window`: 窗口对象                                                   |
| `MouseButtonUp`     | 1026  | 鼠标按键释放事件     | `pos`: 鼠标当前位置 `(x, y)`<br>`button`: 释放的鼠标按钮编号<br>`touch`: 是否触摸事件<br>`window`: 窗口对象                                                   |
| `WindowShown`       | 32774 | 窗口显示事件       | `window`: 窗口对象                                                                                                                       |
| `WindowFocusGained` | 32785 | 窗口获得焦点事件     | `window`: 窗口对象                                                                                                                       |
| `WindowFocusLost`   | 32786 | 窗口失去焦点事件     | `window`: 窗口对象                                                                                                                       |
| `WindowMoved`       | 32777 | 窗口移动事件       | `x`: 窗口新位置的 x 坐标<br>`y`: 窗口新位置的 y 坐标<br>`window`: 窗口对象                                                                               |
| `WindowExposed`     | 32776 | 窗口内容需要重新绘制事件 | `window`: 窗口对象                                                                                                                       |
| `WindowLeave`       | 32784 | 鼠标离开窗口事件     | `window`: 窗口对象                                                                                                                       |
| `WindowEnter`       | 32783 | 鼠标进入窗口事件     | `window`: 窗口对象                                                                                                                       |
| `ActiveEvent`       | 32768 | 窗口活动状态变化事件   | `gain`: 状态变化类型（`1` 表示获得焦点，`0` 表示失去焦点）<br>`state`: 状态详细信息（`1` 表示获得焦点，`2` 表示失去焦点）<br>`window`: 窗口对象                                    |
