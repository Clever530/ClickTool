# ClickTool/连点器
当想用连点器的时候发现没有，于是写了个连点器，写完了发现G502带鼠标宏可以调，我甚至还调过了，乐了

发上来帮助没有鼠标宏的人，现在不支持组合键（因为本质只是想连点鼠标右键），要改组合键可以自己下个代码让AI改一手

![image](https://github.com/Clever530/ClickTool/blob/main/gui.png)

可以进行窗口置顶 默认为置顶状态（按钮显示取消置顶）

设置毫秒数来设置连点时间间隔 默认为100ms

点击快捷键旁按钮设置快捷键 默认为`/~

点击目标按键旁按钮设置连点按键 默认为鼠标左键

重置按钮重置对应行按键

下崽儿连接：[ClickTool.exe](https://github.com/Clever530/ClickTool/releases/download/v1.0.0/ClickTool.exe)


如果有python环境建议直接clone
（不会压缩大小默默说到QAQ）
或者直接克隆项目
```
git clone https://github.com/Clever530/ClickTool.git
```
安装依赖
```python
pip install requirements.txt -r
```
连点器，启动！
```python
python ClickTool.py
```
