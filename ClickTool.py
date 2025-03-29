import tkinter as tk
from tkinter import messagebox
import threading
import time
import pyautogui
import keyboard  # 用于监听键盘事件
import mouse  # 用于监听鼠标事件

class MouseClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("连点器")
        self.running = False
        self.hotkey = '`'  # 默认快捷键
        self.target_button = "left"  # 默认点击鼠标左键

        # 禁止调整窗口大小
        self.root.resizable(False, False)

        # 默认窗口置顶
        self.root.attributes("-topmost", True)

        # 创建置顶按钮
        self.top_button = tk.Button(root, text="取消置顶", command=self.toggle_topmost)
        self.top_button.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # 时间间隔、输入框、开始/停止按钮在一行
        tk.Label(root, text="时间间隔 (毫秒):").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # 添加验证规则
        validate_cmd = root.register(self.validate_numeric_input)  # 注册验证函数
        self.interval_entry = tk.Entry(root, width=10, validate="key", validatecommand=(validate_cmd, "%P"))
        self.interval_entry.grid(row=1, column=1, padx=5, pady=5)
        self.interval_entry.insert(0, "100")  # 默认值为 100 毫秒

        self.start_stop_button = tk.Button(root, text="开始", command=self.toggle_clicking)
        self.start_stop_button.grid(row=1, column=2, padx=5, pady=5)

        # 快捷键、按钮
        tk.Label(root, text="快捷键:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.hotkey_button = tk.Button(root, text=self.hotkey, width=10, command=self.start_hotkey_listening)
        self.hotkey_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.reset_hotkey_button = tk.Button(root, text="重置", command=self.reset_hotkey)
        self.reset_hotkey_button.grid(row=2, column=2, padx=5, pady=5)

        # 自定义按键、按钮
        tk.Label(root, text="目标按键:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.target_button_button = tk.Button(root, text=self.target_button, width=10, command=self.start_listening)
        self.target_button_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.reset_button = tk.Button(root, text="重置", command=self.reset_target_button)
        self.reset_button.grid(row=3, column=2, padx=5, pady=5)

        # 启动快捷键监听线程
        self.listen_hotkeys()

    def validate_numeric_input(self, new_value):
        """
        验证输入框的值是否为数字。
        :param new_value: 输入框的新值
        :return: 如果是数字或为空，则返回 True；否则返回 False
        """
        if new_value.isdigit() or new_value == "":
            return True
        return False

    def start_clicking(self):
        try:
            interval_ms = int(self.interval_entry.get())  # 获取毫秒值
            if interval_ms <= 0:
                raise ValueError("时间间隔必须大于 0")
            interval = interval_ms / 1000.0  # 转换为秒
        except ValueError as e:
            messagebox.showerror("错误", f"无效的时间间隔: {e}")
            return

        self.running = True
        self.start_stop_button.config(text="停止")  # 按钮变为“停止”

        # 禁用输入框和按钮
        self.interval_entry.config(state="disabled")
        self.hotkey_button.config(state="disabled")
        self.reset_hotkey_button.config(state="disabled")
        self.target_button_button.config(state="disabled")
        self.reset_button.config(state="disabled")

        # 取消输入框的焦点
        self.start_stop_button.focus_set()

        # 启动线程以避免阻塞 GUI
        threading.Thread(target=self.click_loop, args=(interval,), daemon=True).start()

    def stop_clicking(self):
        self.running = False
        self.start_stop_button.config(text="开始")  # 按钮变为“开始”

        # 恢复输入框和按钮
        self.interval_entry.config(state="normal")
        self.hotkey_button.config(state="normal")
        self.reset_hotkey_button.config(state="normal")
        self.target_button_button.config(state="normal")
        self.reset_button.config(state="normal")

    def toggle_clicking(self):
        if self.running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def click_loop(self, interval):
        while self.running:
            if self.target_button in ["left", "right", "middle"]:
                pyautogui.click(button=self.target_button)
            else:
                keyboard.press_and_release(self.target_button)
            time.sleep(interval)

    def listen_hotkeys(self):
        # 监听快捷键
        keyboard.add_hotkey(self.hotkey, self.toggle_clicking)  # 使用当前设置的快捷键

    def toggle_topmost(self):
        # 切换窗口置顶状态
        current_state = self.root.attributes("-topmost")
        self.root.attributes("-topmost", not current_state)
        self.top_button.config(text="取消置顶" if not current_state else "置顶")

    def start_hotkey_listening(self):
        # 避免重复监听
        if hasattr(self, "listening_hotkey") and self.listening_hotkey:
            return

        self.listening_hotkey = True  # 标记正在监听
        self.hotkey_button.config(text="_", state="disabled")  # 按钮显示为下划线并禁用

        def on_key_event(event):
            try:
                new_hotkey = event.name
                # 移除旧的快捷键绑定
                if self.hotkey:
                    keyboard.remove_hotkey(self.hotkey)
                # 绑定新的快捷键
                keyboard.add_hotkey(new_hotkey, self.toggle_clicking)
                self.hotkey = new_hotkey
                self.hotkey_button.config(text=self.hotkey, state="normal")  # 更新按钮文本并启用
            except Exception as e:
                messagebox.showerror("错误", f"无法设置快捷键: {e}")
                self.reset_hotkey()  # 恢复默认快捷键
            finally:
                # 仅移除当前监听的事件，而不是所有事件
                keyboard.unhook(on_key_event)
                self.listening_hotkey = False  # 监听结束

        # 监听键盘事件
        keyboard.hook(on_key_event)

    def reset_hotkey(self):
        # 重置快捷键为默认值
        if self.hotkey:
            keyboard.remove_hotkey(self.hotkey)  # 移除旧的快捷键绑定
        self.hotkey = '`'
        self.hotkey_button.config(text=self.hotkey, state="normal")  # 恢复按钮文本和状态
        try:
            keyboard.add_hotkey(self.hotkey, self.toggle_clicking)  # 重新绑定默认快捷键
        except Exception as e:
            messagebox.showerror("错误", f"无法恢复默认快捷键: {e}")

    def set_hotkey(self):
        if not self.hotkey:
            messagebox.showerror("错误", "快捷键不能为空！")
            return
        try:
            # 移除旧的快捷键绑定
            keyboard.remove_hotkey(self.hotkey)
            # 绑定新的快捷键
            keyboard.add_hotkey(self.hotkey, self.toggle_clicking)
        except Exception as e:
            messagebox.showerror("错误", f"无法设置快捷键: {e}")

    def start_listening(self):
        # 避免重复监听
        if hasattr(self, "listening") and self.listening:
            return

        self.listening = True  # 标记正在监听
        self.target_button_button.config(text="_", state="disabled")  # 按钮显示为下划线并禁用

        def stop_listening():
            """停止键盘和鼠标的监听"""
            self.listening = False
            self.target_button_button.config(state="normal")  # 恢复按钮状态
            keyboard.unhook(on_key_event)
            mouse.unhook(on_mouse_event)

        def on_key_event(event):
            try:
                self.target_button = event.name
                self.target_button_button.config(text=self.target_button, state="normal")  # 更新按钮文本并启用
            except Exception as e:
                messagebox.showerror("错误", f"无法设置目标按键: {e}")
            finally:
                stop_listening()  # 停止监听

        def on_mouse_event(event):
            try:
                if hasattr(event, "button"):  # 仅处理鼠标按键事件
                    self.target_button = event.button
                    self.target_button_button.config(text=self.target_button, state="normal")  # 更新按钮文本并启用
            except Exception as e:
                messagebox.showerror("错误", f"无法设置目标按键: {e}")
            finally:
                stop_listening()  # 停止监听

        # 同时监听键盘和鼠标事件
        keyboard.hook(on_key_event)
        mouse.hook(on_mouse_event)

    def reset_target_button(self):
        # 重置目标按键为默认值
        self.target_button = "left"
        self.target_button_button.config(text=self.target_button, state="normal")  # 恢复按钮文本和状态

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseClicker(root)
    root.mainloop()