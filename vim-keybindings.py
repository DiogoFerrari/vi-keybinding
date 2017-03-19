#!/usr/bin/env python3.6
"""
=====================================================
.py
---
Author: Diogo A. Ferrari 

This script turns on and off xbindkeys with some remaping to emulate vim-like keyboard. It shows the status on the top bar and on a notification message. The notifications can be turned off easily below. 

=====================================================
"""
import signal, os, re, subprocess
import pgi
from pgi.repository import Gtk as gtk
from pgi.repository import Keybinder as kbd
from pgi.repository import AppIndicator3 as appindicator
from pgi.repository import Notify as notify
from pgi.repository import GObject
from threading import Thread
pgi.require_version('Gtk', '3.0')
pgi.require_version('Keybinder', '3.0')
pgi.require_version('AppIndicator3', '0.1')


path=os.path.dirname(os.path.abspath(__file__))
APPINDICATOR_ID = 'myappindicator'

class Indicator():
    def __init__(self):
        self.app='Vim_Keyboard'
        self.state=int(0)
        self.icon_on=os.path.join(path, "icon", "vim-on.png")
        self.icon_off=os.path.join(path, "icon", "vim-off.png")
        # after you defined the initial indicator, you can alter the icon!
        self.ind  = appindicator.Indicator.new(self.app, self.icon_off ,
                                            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)       
        self.ind.set_menu(self.build_menu())
        # the thread: (to update the icon)
        self.update = Thread(target=self.deactivate)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()
    
    def build_menu(self):
        menu = gtk.Menu()

        item_activate = gtk.MenuItem('Activate')
        item_activate.connect('activate', self.activate)
        menu.append(item_activate)

        item_deactivate = gtk.MenuItem('Deactivate')
        item_deactivate.connect('activate', self.deactivate)
        menu.append(item_deactivate)

        menu_sep = gtk.SeparatorMenuItem()
        menu.append(menu_sep)

        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        
        menu.show_all()
        return menu

    def quit(self, source):
        self.deactivate()
        gtk.main_quit()

    def activate(self):
        self.state=int(1)
        self.ind.set_icon(self.icon_on)
        # self.notification_show()
        change_keybindings(self.state)
        subprocess.call(["xbindkeys", "-p"])

    def deactivate(self):
        self.state=int(0)
        self.ind.set_icon(self.icon_off)
        # self.notification_show()
        change_keybindings(self.state)
        subprocess.call(["xbindkeys", "-p"])

    def notification_show(self):
        msg_off="Vi mode inactive ! (State : "+str(self.state)+")"
        notification_vim_off =  notify.Notification.new(msg_off, "", self.icon_off)
        msg_on="Vi mode active ! (State : "+str(self.state)+")"
        notification_vim_on = notify.Notification.new(msg_on, "", self.icon_on)
        if self.state == 1:
            notification_vim_off.close()
            notification_vim_on.show()
        else:
            notification_vim_on.close()
            notification_vim_off.show()

    def switch_state(self, keystr, _arg):
        if (self.state == 1):
            self.deactivate()
        else:
            self.activate()

def change_keybindings(state):
    filename=os.path.expanduser('~/.xbindkeysrc')
    with open(filename) as f:
        content=f.readlines()
    ini_position = [idx for idx, text in enumerate(content) if '## --------------' in text][0]
    if state == 1:
        newlines=[re.sub("^#*", "", t) for t in content[ini_position+1:]]
    else:
        newlines=[re.sub("^", "#", t) for t in content[ini_position+1:]]
    content[ini_position+1:]=newlines
    with open(filename, 'w') as f:
        f.write(''.join(content))

def main():
    
    indicator=Indicator()
    notify.init(indicator.app)
    ## keybinding
    ## keystr = "<Ctrl>bracketleft"
    keystr = "<Ctrl>l"
    kbd.init()
    kbd.bind(keystr, indicator.switch_state)

    ## dynamic indicator
    GObject.threads_init()
    signal.signal(signal.SIGINT, signal.SIG_DFL)   
    subprocess.call(["xbindkeys", "-p"])
    gtk.main()                     ## start an endless loop till quit

if __name__ == "__main__":
    main()
