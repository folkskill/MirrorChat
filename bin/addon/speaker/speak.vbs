' 开启静默错误处理
On Error Resume Next

' 创建 SpeechSynthesizer 对象
Set speaker = CreateObject("SAPI.SpVoice")

' 检查对象是否成功创建
If Err.Number <> 0 Then
    ' 对象创建失败，退出脚本
    WScript.Quit
End If

' 清除错误信息
Err.Clear

' 获取所有可用的语音
Set voices = speaker.GetVoices()

' 选择第一个可用的语音（索引从 0 开始）
' 你可以修改索引来选择不同的语音
If voices.Count > 0 Then
    speaker.Voice = voices.Item(0)
End If

' 遍历所有命令行参数
For Each arg In WScript.Arguments
    ' 朗读当前参数
    speaker.Speak arg
    ' 检查是否有错误发生
    If Err.Number <> 0 Then
        ' 发生错误，清除错误信息并继续下一个参数
        Err.Clear
    End If
Next

' 释放对象
Set speaker = Nothing
