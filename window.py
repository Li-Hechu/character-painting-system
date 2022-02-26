"""设计GUI界面"""
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import *

from PIL import Image, ImageTk

from conversion import convert


class GUI:
    """定义GUI界面的设置方法"""

    def __init__(self):
        """初始化方法"""
        # 定义各种参数
        self.img_name = ""
        self.export_filename = ""
        self.is_convert = False  # 判断是否调用转换函数
        # 初始化窗口
        self.win = Tk()
        # 设置窗口属性
        self.win.title("字符画生成系统")
        self.win.geometry("930x460+300+250")
        self.win.resizable(False, False)
        self.win.iconbitmap("ico/dirty snowman.ico")
        # 设置菜单
        menu = Menu(self.win, borderwidth=5, bg="#e4a0c3", tearoff=False, cursor="shuttle")
        menu.add_command(label="说明", command=self.instruction)
        menu.add_command(label="退出", command=self.quit)
        # 设置整体布局,分为上下两个部分
        win_top = Frame(self.win, width=930, height=400)
        win_top.pack(pady=10, side="top")
        win_bottom = Frame(self.win, width=930, height=80)
        win_bottom.pack(pady=(10, 5), side="top")
        # 设置窗体左边布局，用于显示原来的图片
        left = LabelFrame(win_top, text="源", width=350, height=300, relief="groove", borderwidth=5)
        left.pack(padx=15, pady=10, side="left")
        self.left_text = Text(left, width=50, height=20, state="disabled")  # 请主注意，这里的长宽单位与Frame组件不一样
        self.left_text.pack()
        # 设置窗体中间布局，用来放置功能按键
        center = Frame(win_top, width=90, height=300, relief="groove", borderwidth=5)
        center.pack(padx=15, pady=10, side="left")
        Button(center, text="导入", command=self.import_file).pack(pady=10, side="top")
        Button(center, text="转换", command=self.conversion).pack(pady=10, side="top")
        Button(center, text="导出", command=self.export_file).pack(pady=10, side="top")
        Button(center, text="清除全部", command=self.again).pack(pady=10, side="top")
        # 设置窗体右边的布局，用来显示转换后的字符画
        right = LabelFrame(win_top, text="预览窗格", width=350, height=300, relief="groove", borderwidth=5)
        right.pack(padx=15, pady=10, side="left")
        self.right_text = Text(right, width=50, height=20, state="disabled")
        self.right_text.pack()
        # 设置下方功能区
        bottom = LabelFrame(win_bottom, text="通用设置", width=900, height=80, relief="groove", borderwidth=5)
        bottom.pack(side="bottom")
        Label(bottom, text="组成字符画的字符串:", font="宋体 10 bold").pack(padx=5, pady=5, side="left")
        self.str = StringVar()
        Entry(bottom, width=70, textvariable=self.str).pack(padx=5, pady=5, side="left")
        self.str.set("(默认)")
        Label(bottom, text="清晰度:", font="宋体 10 bold").pack(padx=5, pady=10, side="left")
        self.degree = StringVar()
        Combobox(bottom, textvariable=self.degree, values=("清晰", "一般", "字符")).pack(padx=5, pady=10, side="left")
        self.degree.set("一般")
        # 显示菜单
        self.win.config(menu=menu)
        # 显示窗口
        self.win.mainloop()

    def import_file(self):
        """导入图片"""
        self.l_clear()
        self.r_clear()
        self.left_text.config(state="normal")
        self.img_name = askopenfilename(title="导入", filetypes=[("JPG格式图片", "*.jpg"), ("PNG格式图片", "*.jpg"),
                                                                ("ICON格式图片", "*.ico")])
        if self.img_name != "":
            img = Image.open(self.img_name)
            img.thumbnail((350, 300))
            self.photo = ImageTk.PhotoImage(img)
            self.left_text.image_create(END, image=self.photo)  # 要使用全局性的变量来存储图片，否则无法显示
            self.left_text.config(state="disabled")

    def conversion(self):
        """转换图片"""
        if self.img_name == "":
            showerror("错误", "请导入需要转换的图片。")
        else:
            self.r_clear()
            self.img = convert(self.img_name, self.str.get(), self.degree.get())
            temp_img = self.img  # 创建原图片的副本
            self.right_text.config(state="normal")
            temp_img.thumbnail((350, 300))
            self.temp_img = ImageTk.PhotoImage(temp_img)
            self.right_text.image_create(END, image=self.temp_img)
            self.right_text.config(state="disabled")
            self.is_convert = True
            showinfo("提示", "图片转换成功。")

    def export_file(self):
        """导出图片"""
        if self.is_convert == False:
            showerror("错误", "您没有转换图片，请先转换再导出。")
        else:
            if self.img_name == "":
                showerror("错误", "未导入图片。")
            else:
                self.export_filename = asksaveasfilename(title="导出", filetypes=[("JPG格式图片", "*.jpg"),
                                                                                ("PNG格式图片", "*.png")])
                if self.export_filename != "":
                    self.img.save(self.export_filename)
                    showinfo("提示", "图片保存成功！")
                    self.again()

    def l_clear(self):
        """清除左边Text组件里的内容"""
        self.left_text.config(state="normal")
        self.left_text.delete(0.0, END)
        self.left_text.config(state="disabled")

    def r_clear(self):
        """清除右边Text组件里的内容"""
        self.right_text.config(state="normal")
        self.right_text.delete(0.0, END)
        self.right_text.config(state="disabled")

    def again(self):
        """重置"""
        self.img_name = ""
        self.export_filename = ""
        self.is_convert = False
        self.l_clear()
        self.r_clear()

    def instruction(self):
        """该系统的说明内容"""
        top = Toplevel()
        # 窗体基本设置
        top.title("使用说明")
        top.iconbitmap("ico/Freda.ico")
        top.geometry("400x200+600+300")
        top.resizable(False, False)
        # 添加文本框
        introduction = Text(top, width=380, height=180, borderwidth=5, relief="groove", )
        introduction.pack(side="top")
        try:
            with open("introduction/read_me.ini", "r", encoding="utf-8") as fp:
                string = fp.read()
                introduction.insert(0.0, string)
        except FileNotFoundError:
            showerror("错误", "文件不存在")
        introduction.config(state="disabled")
        # 显示窗口
        top.mainloop()

    def quit(self):
        """退出程序"""
        if askyesno("提示", "您确定退出系统？"):
            exit(0)
