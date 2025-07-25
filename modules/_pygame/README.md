# Modules
* [Window](#Window)
* [Music](#Music)
* [Sound](#Sound)
* [Image](#Image)
* [Font](#Font)

## Window
### key_mapping
可以通过set方法绑定某个Key类(name&mapping)

name是指此映射的命名

mapping是指Key类或Key子类

activate方法可以激活某个映射方案

_type可以传入"K"或"M"

### event_match
可以通过add方法添加事件绑定(具体代码请查表)

使用key_event_match方法并通过add绑定后可以直接调用映射函数

具体调用如下

```
cls.add_user_event_match(event_id, cls.key_event_match)
```

### update
update方法是在运行中更新的内容

比如画面

可以使用set方法更改update

## Music
可以通过play方法播放某个音乐

传入方法为基础保存路径.文件夹.文件名(带后缀)

所有路径分隔符应改为"."

stop用于停止

pause用于暂停

unpause用于恢复播放

set_volume用于调整音量

## Sound
使用init方法初始化音效后

可以通过play方法播放

可以通过stop方法终止某个音效播放(虽然貌似没必要)

set_volume方法可以调整单个音效音量

## Image
使用add_file(s)方法添加文件

可以使用scan_directory(_s)方法扫描所有符合后缀的文件

并通过add方法加入

add_exclusion_directory(_s)方法可以添加排除目录

通过init方法初始化图片后

可以通过blit方法绘制到窗口上(需要Window实例)

可以通过scale方法调整其大小

## Font
过于烂

基本用不了

## Key mapping
使用add方法添加按键映射

可通过按键名或id添加,但映射方法必须有名为event的可传参

使用remove方法移除

run可运行

MouseButton类为鼠标映射类

在运行中的更改貌似会与Key类同步

此外可以通过[事件对照表](event_compare.md)和[按键对照表](key_mapping.md)查表
