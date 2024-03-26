Win+Z ：打开窗口布局

Win+N ：打开通知中心/四指轻触

Win+A ：打开快速设置

Win+W ：打开小组件

Win+E ：打开文件资源管理器

Win+ S  == Win + Q ：打开搜索/三指轻触

Win+ Shift+S ：打开截图

Win+V ：打开剪贴板

Win+H ：打开语音识别文字

Win+ . ：打开表情库

Win+D ：清理打开的窗口及最小化，显示桌面

Win+L ：锁屏

Win+Tab ：切换任务窗口

Win+B快速跳转系统托盘

Win+B是系统托盘的快捷键。按下时，焦点会移到托盘上，点击回车后可以直接看到托盘图标

Win+C 开放微软团队 ，微软团队也是Windows 11中新增的一个组件。

Win+空格 切换输入法，在装有多款输入法的系统之中，Win+空格可以快速完成输入法切换

Win+光标键 窗口排版，借助Win键+→/↑/←/↓，可以实现左/右/左上/左下/右上/右下/全屏/最小化/上半屏九种组合

Win + 小数字， 窗口切换

Win+Home 最小化非活动窗口，打开窗口过多，会严重影响前端的工作效率，这时Win+Home就能派上用场了。





切换无线网

netsh wlan show networks

连接无线网

netsh wlan connect name=iBOSHKFCS

netsh wlan connect name=cl

断开连接

netsh wlan disconnect  [[interface=]<string>]





### win11右键菜单样式改变

管理员运行命令：

reg.exe add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve 

不需要重启电脑，重启资源管理器即可，用命令：

taskkill /f /im explorer.exe ; start explorer.exe

这个是恢复win11右键

reg.exe delete "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /va /f













