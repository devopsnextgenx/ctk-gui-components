from devopsnextgenx.components.messageHub.Alert import Alert
from devopsnextgenx.components.messageHub.Banner import Banner
from devopsnextgenx.components.messageHub.Notification import Notification

root_frame = None
def set_root_frame(rt_frame):
    global root_frame
    root_frame = rt_frame

def show_alert(state, title, body_text, btn1="Ok", btn2="Cancel"):
    alertx = Alert(state=state, title=title, body_text=body_text, btn1=btn1, btn2=btn2)

def show_banner(state, title, side="right_bottom", btn1=None, btn2=None):
    global root_frame
    bannerx = Banner(master=root_frame, state=state, title=title,
                     btn1=btn1, btn2=btn2, side=side)

def show_notification(state, message, side="right_bottom"):
    global root_frame
    notificationx = Notification(master=root_frame, state=state, message=message, side=side)
