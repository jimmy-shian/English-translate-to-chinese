import tkinter as tk
from tkinter import Tk, Entry
import pyautogui
import time
import clipboard

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder=None, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_color = self['fg']
        self.bind("<FocusIn>", self.on_entry_click)
        self.bind("<FocusOut>", self.on_focus_out)
        self.on_focus_out(None)
        
    def on_entry_click(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END) 
            self.insert(0, '')
            self.config(fg=self.default_color)
            
    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)

def convert_input(text):
    pyautogui.hotkey('ctrl', ' ') #輸入法切換位置
    # 将输入的文字逐一输入
    for c in text:
        pyautogui.press(c)
    time.sleep(0.3)

def convert_input_from_inputbox(event):
    # 获取输入框的内容
    text = input_box.get()
    if not text:
        return text_output.insert(tk.END, f"\n請輸入內容\n")
    # 输出"开始转换"
    text_output.insert(tk.END, f"\n開始轉換..")
    time.sleep(1)
    # 如果输入框为空，直接返回
    text_output.insert(tk.END, f"...輸入法轉為中文\n")
    # 清空第二个输入框的内容
    input_box2.delete(0, tk.END)
    # 将焦点设置为第二个输入框
    input_box2.focus()
    # 执行转换
    convert_input(text)

def copy_to_clipboard(event):
    # 获取输入框2的内容
    text2 = input_box2.get()
    # 如果输入框为空，直接返回
    if not text2:
        return text_output.insert(tk.END, f"\n轉換失敗請重新嘗試\n")
    time.sleep(0.5)
    text_output.insert(tk.END, f"\n複製「{text2}」到剪貼簿\n")
    time.sleep(0.5)
    # 将内容复制到剪贴板
    clipboard.copy(text2)

# 创建窗口
window = tk.Tk()
window.geometry("600x700")
# 设置窗口标题
window.title("輸入法轉換工具")

# 创建第一个输入框
input_box = PlaceholderEntry(window, font=("Helvetica", 15), placeholder="文字輸入位置")
input_box.pack(padx=20, pady=10, fill=tk.X)
# 绑定 Enter 键的事件处理函数
input_box.bind("<Return>", lambda event: convert_input_from_inputbox(event))
# 创建第二个输入框
input_box2 = PlaceholderEntry(window, font=("Helvetica", 15), placeholder="結果顯示&文字選擇")
input_box2.pack(padx=20, pady=10, fill=tk.X)
# 绑定 Enter 键的事件处理函数
input_box2.bind("<Return>", lambda event: copy_to_clipboard(event))

button_frame = tk.Frame(window)
text_frame = tk.Frame(window)
# 创建转换按钮
convert_button = tk.Button(button_frame, text="開始轉換",height=1, command=lambda event=None: convert_input_from_inputbox(event))
convert_button.pack(side=tk.LEFT, pady=10, padx=0)
# 创建复制按钮
copy_button = tk.Button(button_frame, text="複製結果",height=1, command=lambda event=None: copy_to_clipboard(event))
copy_button.pack(side=tk.LEFT, padx=30)
# 创建 Scrollbar
scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# 创建 Text 组件，并允许编辑
text_output = tk.Text(text_frame, height=25, state=tk.NORMAL, yscrollcommand=scrollbar.set)
text_output.pack(side=tk.TOP, padx=10, pady=20, fill=tk.BOTH)
text_output.insert(tk.END, f"""(輸入法為英文時, 才可轉換文中文)\n
在文字輸入位置按"enter"即可開始轉換\n
在結果顯示位置按"enter"即可複製文字\n
                   """)
# 配置 Scrollbar
scrollbar.config(command=text_output.yview)
# 将按钮Frame和文本框Frame放入主窗口中
button_frame.pack(expand=0, side=tk.TOP)
text_frame.pack(side=tk.TOP)

# 运行窗口
window.mainloop()
