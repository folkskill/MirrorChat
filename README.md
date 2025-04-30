<p align="center">
  <img width="18%" align="center" src="https://github.com/user-attachments/assets/3b1f2665-5f26-4170-8563-9529df52c552" alt="logo">
</p>
  <h1 align="center">
  MirrorChat
</h1>

<p align="center">
  基于 Wcferry 的微信拓展工具
</p>

<div align="center">

</div>

<p align="center">
<a href="../README.md">English</a> | 简体中文 | <a href="https://qfluentwidgets.com/">官方网站</a>
</p>

<div align="center">

![version](https://img.shields.io/badge/version-0.2.1.20250425_beta-blue)
![Interface](https://raw.githubusercontent.com/zhiyiYo/PyQt-Fluent-Widgets/master/docs/source/_static/Interface.jpg)

</div>

## 使用📥

使用 pip3 下载：

1. `PyQt-Fluent-Widgets`
2. `wcferry`
3. `colorama`

shell 使用 pip 下载示例：

```shell
pip install "PyQt-Fluent-Widgets[full]" -i https://pypi.org/simple/
pip install wcferry
pip install colorama
```

在 GitHub 中点击下载 ZIP。
将项目解压并开始您的拓展使用！

## 运行示例▶️

使用 pip 安装好以上的包之后，就可以运行本项目。

```shell
cd bin
python MirrorChatMain.py
```

如果遇到 `ImportError: cannot import name 'XXX' from 'qfluentwidgets'`，这表明安装的 `PyQt-Fluent-Widgets` 版本过低。可以按照上面的安装指令将 pypi 源替换为 https://pypi.org/simple 并重新安装.

## 许可证📄

本项目的开发以提升用户对原版微信的使用体验为目标，本人不支持，不同意其他人利用本项目进行包括但不限于如下的行为：

1. 窃取微信隐私敏感信息。
2. 恶意制作病毒插件。
3. 利用本项目进行违反网络安全法的行为。

另外的，本人不允许他人在本项目的原版基础上进行源码修改并发布。
（除非经过本人的允许）

## 关于 Wcferry🚀️

[wcferry](https://github.com/lich0821/WeChatFerry) 是一个优秀的微信集成开发工具。
其提供了很多与微信交互的方法和功能。
没有这个模块，本项目绝对无法持续的开发！

## 关于作者 😄

本项目由 [folkskill](https://github.com/folkskill) 独立制作。

# 版本更新 🎉️

## V0.2.1.20250425_beta 🚀️

### 新增 🆕

- 加入 `encoder` 插件，用于实现对消息的加密和解密。(用 C++ 实现，位于 `bin/addon/encoder/file.exe`, 主要贡献人是 `@blbl-SheepSoup`)
- 在 `bin/module/chatTools.py` 中添加了对于插件的 `tool.mirc` 脚本的注入。
- 在 `bin/module/chatTools.py` 中添加了发送文件的内置小工具。

<details><summary>点击查看更多历史版本</summary>

## V0.2.0.20250410_beta 🚀️

### 新增 🆕

- 为 GUI 界面加入了设置界面。(位于 `bin/gui/settings/settings.py`)
- 为 GUI 界面加入了小工具按钮。(位于 `bin/module/chatTools.py`)
- 在 `bin/` 目录下加入了 `addon` 目录, 用于实现插件功能。
- 在 `bin/addon/` 目录下加入了 `example` 插件, 作为插件功能的示例。

## V0.1.1.20250405_beta 🚀️

### 新增 🆕

- 对 `fluent-widgets` 的 GUI 界面进行更新。实现了消息气泡，以及对于消息的发送和接收的功能。(使用 `bin/module/wechatWapper.py`)
- 基于 `V0.1.0.20250331_beta` 中对于 `.mirc` 脚本载入的支持，采用了将样式设置相关的代码写入了 `.mirc` 脚本中。目的是为了让用户可以自定义样式。
- 在 `bin/` 目录下加入了 `imports` 目录，用于实现所用库的集中管理。

### 修复 ✅

- 修复了 `.mirc` 脚本的注入器在注入 `.mirc` 脚本时因为换行写入函数，类，而导致的 EOF 读取错误。

## V0.1.0.20250331_beta 🚀️

### 新增 🆕

- 确认项目的文件架构。
- 加入对于本项目的脚本文件 `.mirc`，本质上是一个 `.py` 文件。以及对 `.mirc` 的注入器。(位于 `bin/module/moduleLoader.py`)
- 实现了对于 `fluent-widgets` 的基本交互界面的开发。
- 制作微信交互器模块。(位于 `bin/module/wechatWapper.py`)

</details>

