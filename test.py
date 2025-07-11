def speak():
    from os import getcwd
    from subprocess import Popen
    msg:str = "测试"
    cwd = getcwd()
    print(cwd + f"bin\\addon\\speaker\\speak.vbs")
    Popen([cwd + f"bin\\addon\\speaker\\speak.vbs", msg], shell=True)

speak()