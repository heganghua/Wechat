# -*- coding: utf-8 -*-
import sys, io
from pywinauto.application import Application
import time

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='GB2312')


class WeChatGet:

    def __init__(self):
        self.init_window()
        # app = Application().connect(handle=0x3070c)
        # app = Application().start('notepad.exe')
        # 连接程序， 微信Process
        # app = Application('uia').connect(process=7020)
        # 拿到微信主窗口
        # win_main_Dialog = app.window(class_name="WeChatMainWndForPC")
        # 判断是否为dialog，
        # print(win_main_Dialog.is_dialog)
        # 给控件画个共色框便于看出
        # win_main_Dialog.draw_outline(colour='red')
        # 打印当前窗口的所有controller（控件和属性）
        # win_main_Dialog.print_control_identifiers(depth=None, filename=None)
        # session_listBox = win_main_Dialog.child_window(title="会话", control_type="List")
        # while(True):
        #     # session_listBox.print_control_identifiers()
        #     # 好友列表
        #     for item in session_listBox.items():
        #         print(item)
        #     session_listBox = session_listBox.scroll(direction='down', amount='page')
        #     print("===============================================")
        # details_page = win_main_Dialog.child_window(class_name='ContactProfileWnd')
        # details_page.draw_outline(colour='red')
        # we_id = win_main_Dialog.child_window(title="微信号：", control_type="Text")
        # print(we_id.window_text())

    def init_window(self, exe_path=r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
                    turn_page_interval=3,
                    click_url_interval=1,
                    win_width=1000,
                    win_height=600):
        app = Application('uia').connect(process=23556)
        self.main_win = app.window(title=u"微信", class_name="WeChatMainWndForPC")
        self.main_win.set_focus()
        self.app = app
        self.visible_top = 70
        self.turn_page_interval = turn_page_interval
        self.click_url_interval = click_url_interval
        self.browser = None
        self.win_width = win_width
        self.win_height = win_height

    def click_center(self, control, click_main=True):
        coords = control.rectangle()
        if click_main:
            win_rect = self.main_win.rectangle()
            x = (coords.left + coords.right) // 2 - win_rect.left
            y = (coords.top + coords.bottom) // 2 - win_rect.top
            self.main_win.click_input(coords=(x, y))
        else:
            win_rect = self.browser.rectangle()
            self.browser.click_input(coords=((coords.left + coords.right) // 2 - win_rect.left,
                                             (coords.top + coords.bottom) // 2 - win_rect.top))

    def locate_user(self, user, retry=5):
        if not self.main_win:
            raise RuntimeError("you should call init_window first")
        search_btn = self.main_win.child_window(title="搜索", control_type="Edit")
        search_btn.draw_outline(colour='red')
        self.click_center(search_btn)
        self.main_win.type_keys("^a")
        self.main_win.type_keys("{BACKSPACE}")
        self.main_win.type_keys(user)
        for i in range(retry):
            time.sleep(1)
            print(i)
            try:
                search_list = self.main_win.child_window(title="搜索结果")
                match_result = search_list.child_window(title=user, control_type="ListItem")
                self.click_center(match_result)
                # match_result.print_control_identifiers()
                return True
            except Exception as e:
                print(e)
                return False

    def chat_message(self):
        """
        点击右上角的聊天信息按钮，
        :return:
        """
        try:
            message_window = self.main_win.child_window(title="聊天信息", control_type="Button")
            message_window.draw_outline(colour='red')
            self.click_center(message_window)
            message_window.print_control_identifiers()
        except Exception as e:
            print(e)

    def session_chat_room_Detail_Wnd(self):
        """
        聊天信息详情
        :return:
        """
        detail_win = self.main_win.child_window(class_name="SessionChatRoomDetailWnd")
        detail_win.draw_outline(colour='red')
        # detail_win.print_control_identifiers()

        more_button = detail_win.child_window(title="查看更多群成员", control_type="Button")
        more_button.draw_outline(colour='red')
        time.sleep(2)
        self.click_center(more_button)
        # more_button.print_control_identifiers()

        # member_win = detail_win.child_window(title="聊天成员", control_type="List")
        # member_win.draw_outline(colour='red')
        # for item in member_win:
        #     self.click_center(item)


        # member_win.print_control_identifiers()


    def main(self):
        self.locate_user("闪聚•长沙15群")
        time.sleep(1)
        self.chat_message()
        time.sleep(1)
        self.session_chat_room_Detail_Wnd()


if __name__ == '__main__':
    wc = WeChatGet()
    wc.main()
