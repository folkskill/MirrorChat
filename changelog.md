# 版本更新 🎉️

## V0.2.1.20250425_beta 🚀️ 

### 新增

- 加入 `encoder` 插件，用于实现对消息的加密和解密。(用 C++ 实现，位于 `bin/addon/encoder/file.exe`, 主要贡献人是 `@blbl-SheepSoup`)
- 在 `bin/module/chatTools.py` 中添加了对于插件的 `tool.mirc` 脚本的注入。
- 在 `bin/module/chatTools.py` 中添加了发送文件的内置小工具。

## V0.2.0.20250410_beta 🚀️ 

### 新增

- 为 GUI 界面加入了设置界面。(位于 `bin/gui/settings/settings.py`)
- 为 GUI 界面加入了小工具按钮。(位于 `bin/module/chatTools.py`)
- 在 `bin/` 目录下加入了 `addon` 目录, 用于实现插件功能。
- 在 `bin/addon/` 目录下加入了 `example` 插件, 作为插件功能的示例。

## V0.1.1.20250405_beta 🚀️ 

### 新增

- 对 `fluent-widgets` 的 GUI 界面进行更新。实现了消息气泡，以及对于消息的发送和接收的功能。(使用 `bin/module/wechatWapper.py`)
- 基于 `V0.1.0.20250331_beta` 中对于 `.mirc` 脚本载入的支持，采用了将样式设置相关的代码写入了 `.mirc` 脚本中。目的是为了让用户可以自定义样式。
- 在 `bin/` 目录下加入了 `imports` 目录，用于实现所用库的集中管理。

### 修复

- 修复了 `.mirc` 脚本的注入器在注入 `.mirc` 脚本时因为换行写入函数，类，而导致的 EOF 读取错误。

## V0.1.0.20250331_beta 🚀️ 

### 新增

- 确认项目的文件架构。
- 加入对于本项目的脚本文件 `.mirc`，本质上是一个 `.py` 文件。以及对 `.mirc` 的注入器。(位于 `bin/module/moduleLoader.py`)
- 实现了对于 `fluent-widgets` 的基本交互界面的开发。
- 制作微信交互器模块。(位于 `bin/module/wechatWapper.py`)