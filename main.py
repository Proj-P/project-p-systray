#! /usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import webbrowser
import requests
from threading import Thread
from socketIO_client import SocketIO, LoggingNamespace

LOCATION_ID = 2
API_URL = 'https://api.project-p.xyz'

TRAY_TOOLTIP = 'Project P'
TRAY_ICON_OPEN = './project-p-tray-16-open.png'
TRAY_ICON_CLOSED = './project-p-tray-16-closed.png'

class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)

        self.SetTopWindow(frame)
        self.tbicon = TaskBarIcon(frame)

        return True

    def on_ws_location(self, *args):
        res, = args # Unpack tuple

        self.tbicon.set_icon(res['data']['occupied'])

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self._initialize_icon()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self._create_menu_item(menu, 'Open Project P website', self._open_site)
        menu.AppendSeparator()
        self._create_menu_item(menu, 'Exit', self._on_exit)

        return menu

    def set_icon(self, occupied):
        if occupied:
            icon = wx.IconFromBitmap(wx.Bitmap(TRAY_ICON_CLOSED))
        else:
            icon = wx.IconFromBitmap(wx.Bitmap(TRAY_ICON_OPEN))

        self.SetIcon(icon, TRAY_TOOLTIP)

    def _open_site(self, event):
        webbrowser.open('https://project-p.xyz')

    def _on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    def _create_menu_item(self, menu, label, func):
        item = wx.MenuItem(menu, -1, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.AppendItem(item)

        return item

    def _initialize_icon(self):
        try:
            r = requests.get('%s/locations/%d' % (API_URL, LOCATION_ID))
        except Exception as e:
            print e
            self.set_icon(True)
            return

        location = r.json()

        self.set_icon(location['data']['occupied'])

def main():
    app = App(False)
    socketIO = SocketIO(API_URL, 443, LoggingNamespace)
    socketIO.on('location', app.on_ws_location)

    Thread(target=socketIO.wait).start()
    app.MainLoop()

if __name__ == '__main__':
    main()
