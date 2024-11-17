import tkinter as tk
from tkinter import Tk, Label, PhotoImage
from pathlib import Path

def main():
    # 创建主窗口
    root = Tk()
    root.title("全屏图片显示")
    
    # 获取当前脚本所在的目录
    script_dir = Path(__file__).parent

    # 指定要显示的图片文件名
    image_filename = "your_image.png"  # 请将此处的 'your_image.png' 替换为你的图片文件名

    # 构建图片的完整路径
    image_path = script_dir / image_filename

    # 检查图片文件是否存在
    if not image_path.exists():
        print(f"图片文件未找到: {image_path}")
        return

    # 加载图片
    image = PhotoImage(file=str(image_path))

    # 创建标签并设置图片
    label = Label(root, image=image)
    label.pack(fill=tk.BOTH, expand=tk.YES)

    # 使窗口置顶
    root.attributes("-topmost", True)

    # 进入全屏模式
    root.attributes("-fullscreen", True)

    # 绑定按键事件以退出全屏
    def exit_fullscreen(event):
        root.destroy()

    root.bind("<Escape>", exit_fullscreen)  # 按下 Esc 键退出
    root.bind("q", exit_fullscreen)        # 按下 q 键退出

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()