# -*- coding: utf-8 -*-
import sys, io
import pywinauto
import pyautogui
from pywinauto.application import Application
import time


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='GB2312')


class WeChatGet:

    def __init__(self):
        self.init_window()
        # app = Application().connect(handle=0x3070c)
        # app = Application().start('notepad.exe')
        # 打印当前窗口的所有controller（控件和属性）
        # win_main_Dialog.print_control_identifiers(depth=None, filename=None)

    def init_window(self, exe_path=r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
                    turn_page_interval=3,
                    click_url_interval=1,
                    counter_interval=48 * 3600,
                    read_count_init_pg_down=5,
                    win_width=1000,
                    win_height=1000,
                    find_window_timeout=30):
        # 连接程序， 微信Process
        app = Application('uia').connect(process=4688)
        self.main_win = app.window(title=u"微信", class_name="WeChatMainWndForPC")
        self.main_win.set_focus()
        self.app = app
        self.visible_top = 70
        self.turn_page_interval = turn_page_interval
        self.click_url_interval = click_url_interval
        self.counter_interval = counter_interval
        self.read_count_init_pg_down = read_count_init_pg_down
        self.browser = None
        self.win_width = win_width
        self.win_height = win_height
        self.app2 = Application().connect(process=4688)
        self.move_window()

    def move_window(self):
        self.app2.window(title=u"微信", class_name="WeChatMainWndForPC")\
            .move_window(0, 0, width=self.win_width, height=self.win_height)

    def click_center(self, control, click_main=True, pywingui_click=False):
        """
         元素点击
         :param control: 控件
         :param click_main:
         :return:
         """
        coords = control.rectangle()
        if click_main:
            win_rect = self.main_win.rectangle()
            x = (coords.left + coords.right) // 2 - win_rect.left
            y = (coords.top + coords.bottom) // 2 - win_rect.top
            print(x, y)
            if pywingui_click:
                pyautogui.leftClick(x=x, y=y)
            else:
                self.main_win.click_input(coords=(x, y))
        else:
            win_rect = self.browser.rectangle()
            self.browser.click_input(coords=((coords.left + coords.right) // 2 - win_rect.left,
                                             (coords.top + coords.bottom) // 2 - win_rect.top))

    def click(self, coords):
        pywinauto.mouse.move((coords[0], coords[1]))
        pywinauto.mouse.click(coords=(coords[0], coords[1]))

    def double_click(self, coords):
        pywinauto.mouse.move((coords[0], coords[1]))
        pywinauto.mouse.double_click(coords=(coords[0], coords[1]))

    def get_central_point(self, control):
        """
        元素点击，点击改为pyautogui
        :param control:
        :return:
        """
        coords = control.rectangle()
        win_rect = self.main_win.rectangle()
        moveToX = (coords.left + coords.right) // 2 - win_rect.left
        moveToY = (coords.top + coords.bottom) // 2 - win_rect.top
        print(moveToX, moveToY)
        pyautogui.leftClick(x=moveToX, y=moveToY)


    def locate_user(self, user, retry=5):
        """
        根据user搜索群
        :param user:
        :param retry:
        :return:
        """
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
        self.click_center(more_button, pywingui_click=True)
        time.sleep(30)
        # time.sleep(1)
        # coords = pyautogui.locateOnScreen("./more.png")
        # print("移动鼠标", coords)
        # x = coords.left + coords.width//2
        # y = coords.top + coords.height//2
        # print(x, y)
        # detail_win.click_input(coords=(x, y))
        # time.sleep(10)

        # member_win = detail_win.child_window(title="聊天成员", control_type="List")
        # member_win.draw_outline(colour='red')
        # for item in member_win:
        #     print(item)
            # self.click_center(item)

    def main(self):
        self.locate_user("产研运大军")
        time.sleep(1)
        self.chat_message()
        time.sleep(1)
        self.session_chat_room_Detail_Wnd()


if __name__ == '__main__':
    wc = WeChatGet()
    wc.main()
