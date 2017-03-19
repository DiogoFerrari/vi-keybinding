# Introduction

It was created and tested to work on ubuntu 16+. This script is used to turn on and off a particular remapping of the keyboard keys. It displays an icon on the top bar showing when the remapping is on. It also creates a system wide keybinding ("Ctrl+[" is e one I use) to quickly turn the remapping on and off.

Dependencies:

1. Python 3+
2. [xbindkeys](http://www.nongnu.org/xbindkeys/)
3. [xvkbd](http://t-sato.in.coocan.jp/xvkbd/#misc)
4. the python modules you can see in the file  vim-keybindings.py

# Installation and Usage

1. In your preferred folder, clone the repository
```
git clone https://github.com/DiogoFerrari/vi-keybinding.git
```
2. Copy the file .xbindkeysrc to ~/ and modify that file according to your preferences (see [xbindkeys](http://www.nongnu.org/xbindkeys/))
3. Open the terminal, go to the local folder you saved the repository and run
```
python3 vim-keybindings.py &
```
4. Close the terminal
5. Use ctrl+[ to change the keyboard functionalities

Note: in ubuntu, I particularly have a shortcut to start the script: System Settings -> keyboard -> Shortcuts -> Custom Shortcuts. Then add a new shortcut with keybinding you prefer and command
```
python3 <path-to-the-script>/vim-keybindings.py
```
This shortcut will be used only to start the script. The ctrl+[ will still be used to change the keyboard setup

# Details

The *xbindkeys* is an application that uses a file "\~/.xbindkeysrc" in which the keybindings and remaps are defined. For more details, check [here](https://wiki.archlinux.org/index.php/Xbindkeys). I use that file to also call other keyboard remapping application, *xvkbd* (you find more details [xvkbd](http://t-sato.in.coocan.jp/xvkbd/#misc)). Basically, after installing these two applications, you run *xbindkeys -p*, and the keyboard will use whatever is defined in the file "\~/.xbindkeysrc". When you modify "\~/.xbindkeysrc", you run *xbindkeys -p* to update the configuration. Given that, my script just select all the lines below a line mark that I use in the file "\~/.xbindkeysrc" and comment (uncomment) them when I (do not) want to use my alternative keyboard map. Then, it reloads the configuration by executing *xbindkeys -p* again. So you need to create your own "\~/.xbindkeysrc" (for instance, by running *xbindkeys -d > \~/.xbindkeysrc*) or use the "\~/.xbindkeysrc" of this repository (copy it to \~/).

I use the same global keybinding to turn on and off the two system-wide keyboard configurations I use (the standard and the vim-like one). My personal choice was to use "Crtl+[" for that purpose. So, the script vim-keybindings.py keeps track of the current keyboard state (standard versus vim-like). When I press "Crtl+[", it just changes the system to the other state. 

# Why do I need this?

I use emacs evil mode to emulate the vim navigation with *hjkl* as usually in vim. I also use [Vimium](https://chrome.google.com/webstore/detail/vimium/dbepggeogbaibhgnhhndojpepiihcmeb?hl=en), which is a vim-like navigation extension for chrome. The *vimium* has a limitation. It does not work when one opens a pdf in the browser and in other situations too (when the focus in on a text input box, for instance). So, the script allow me to turn on the keyboard functionalities that I need even in those cases in which vimium fails.

I use an additional setup to work on chrome in all situations, including pdfs, as following (=> means remapped to using xbindkeysrc):

- Alt+Shift+Tab => Shift+j : previous tab
- Alt+Tab => Shift+k : next tab
- Ctrl+w => q : close tab
- Ctrl+s => z : save
- Ctrl+t => t : new tab

# Enjoy !