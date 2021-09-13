# -*- coding: utf-8 -*-
import sys, io
import pywinauto
import pyautogui
from pywinauto.application import Application
import time
import psutil
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='')


class WeChatGet:

    def __init__(self):
        self.init_window()

    def init_window(self, turn_page_interval=3,
                    click_url_interval=1,
                    counter_interval=48 * 3600,
                    read_count_init_pg_down=5,
                    win_width=1000,
                    win_height=1000):
        # 连接程序， 微信Process

        wechat_pid = self.get_wechat_pid()
        if not wechat_pid:
            raise Exception("未找到WeChat.exe程序，请确定是否已经登录微信")
        app = Application('uia').connect(process=wechat_pid)
        self.main_win = app.window(title=u"微信", class_name="WeChatMainWndForPC")
        self.main_win.set_focus()
        self.app = app
        self.visible_top = 70
        self.turn_page_interval = turn_page_interval
        self.click_url_interval = click_url_interval
        self.counter_interval = counter_interval
        self.read_count_init_pg_down = read_count_init_pg_down
        self.win_width = win_width
        self.win_height = win_height
        self.app2 = Application().connect(process=wechat_pid)
        self.move_window()

    def get_wechat_pid(self):
        process_list = list(psutil.process_iter())
        for item in process_list:
            if item.name() == "WeChat.exe":
                return item.pid
        return None

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
            try:
                search_list = self.main_win.child_window(title="搜索结果")
                match_result = search_list.child_window(title=user, control_type="ListItem")
                self.click_center(match_result)
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

    def click_head_element(self, elem):
        """
        获取微信昵称
        :param elem:
        :return:
        """
        try:
            elem.draw_outline(colour='blue')
            head_dailog = self.main_win.child_window(class_name="ContactProfileWnd")
            # head_dailog.print_control_identifiers()
            pane = head_dailog.children()[1].children()[0].children()[0].children()[0].children()[0].children()[0]
            nick_name = pane.element_info.name
            print(nick_name)
            head_dailog.type_keys("{ESC}")
        except Exception as e:
            print(e)

    def get_wechat_id(self):
        try:
            text = self.main_win.child_window(title="聊天", control_type="Button")
            btn = text.parent().children()[0]
            self.click_center(btn)
            label = self.main_win.child_window(title="微信号：")
            p = label.parent().children()[1]
            wechat_id = p.element_info.name
            self.click_center(btn)
        except:
            pass
        return wechat_id

    def session_chat_room_Detail_Wnd(self):
        """
        聊天信息详情
        :return:
        """
        detail_win = self.main_win.child_window(class_name="SessionChatRoomDetailWnd")
        detail_win.draw_outline(colour='red')
        more_button = detail_win.child_window(title="查看更多群成员", control_type="Button")
        more_button.draw_outline(colour='red')
        self.click_center(more_button, pywingui_click=True)
        time.sleep(0.1)
        member_win = detail_win.child_window(title="聊天成员", control_type="List")
        member_win.draw_outline(colour='red')
        pane = member_win.children()
        resultList = []
        for item in pane:
            try:
                print(item)
                nick_name = str(item).split('-')[1].split(',')[0]
                print(nick_name)
                resultList.append(nick_name)
            except Exception as e:
                print(e)
        if resultList is not None:
            self.saveNicknameAndGroupName(resultList, "123")

    def saveNicknameAndGroupName(self, nicknameList, groupName):
        """
        保存数据
        :return:
        """
        with open("./result.txt", 'a') as f:
            for nickname in nicknameList:
                f.writelines(nickname + "\n")

    def main(self):
        self.locate_user("云龙名邸业主物业交流群")
        time.sleep(1)
        # print(self.get_wechat_id())
        self.chat_message()
        self.session_chat_room_Detail_Wnd()


if __name__ == '__main__':
    wc = WeChatGet()
    wc.main()
