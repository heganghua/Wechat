# -*- coding: utf-8 -*-

from pywinauto.application import Application

class WeChatGet:

    def __init__(self):
        # app = Application().connect(handle=0x3070c)
        # app = Application().start('notepad.exe')
        # 连接程序， 微信Process
        app = Application('uia').connect(process=5344)
        # 拿到微信主窗口
        win_main_Dialog = app.window(class_name="WeChatMainWndForPC")
        # 判断是否为dialog，
        print(win_main_Dialog.is_dialog)
        # 给控件画个共色框便于看出
        win_main_Dialog.draw_outline(colour='red')
        # 打印当前窗口的所有controller（控件和属性）
        win_main_Dialog.print_control_identifiers(depth=None, filename=None)

    def main(self):
        pass


if __name__ == '__main__':
    wc = WeChatGet()
