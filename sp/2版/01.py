import tkinter as tk
from tkinter import Tk
from PIL import Image, ImageTk  # 注意：这里使用了 PIL 库
import sys

def main(image_path):
    root = Tk()
    root.attributes("-fullscreen", True)  # 设置全屏
    root.configure(background='black')  # 设置背景颜色

    # 加载图片
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"无法打开图片: {e}")
        sys.exit(1)

    photo = ImageTk.PhotoImage(image)

    # 创建标签并显示图片
    label = tk.Label(root, image=photo, bg='black')
    label.pack(fill=tk.BOTH, expand=True)

    # 保持对图片的引用，否则图片可能不会显示
    label.image = photo

    # 退出全屏的快捷键（例如，按下 Esc 键）
    def exit_fullscreen(event):
        root.destroy()

    root.bind("<Escape>", exit_fullscreen)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = '1.png'  # 默认图片路径

    main(image_path)