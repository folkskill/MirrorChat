from cx_Freeze import setup, Executable

# 配置要打包的脚本
executables = [
    Executable(
        script="bin/MirrorChatMain.py",  # 要打包的 Python 脚本
        base="Win32GUI",  # 对于控制台应用程序，设置为 None；对于 GUI 应用程序，Windows 下可设置为 "Win32GUI"
        target_name="MirrorChatMain.exe",  # 生成的可执行文件的名称
        icon="icon.ico"  # 可执行文件的图标文件路径
    )
]

# 配置打包选项
build_options = {
    "packages": ["loguru","qfluentwidgets","wcferry","bin.gui","bin.addon","bin.config","bin.imports","bin.module"],  # 需要包含的 Python 包
    "excludes": [],  # 需要排除的 Python 包
    "include_files": [],  # 需要包含的额外文件或目录，
}

# 调用 setup 函数进行打包
setup(
    name="MirrorChat",  # 项目名称
    version="0.3.1.20250518",  # 项目版本
    description="MirrorChat",  # 项目描述
    options={"build_exe": build_options},  # 打包选项
    executables=executables  # 可执行文件配置
)