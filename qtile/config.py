# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import re
import socket
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401
import os
import subprocess

mod = "mod4"
terminal = "alacritty"
myBrowser = "vivaldi"
myPrompt = "dmenu_run"

keys = [
    Key(
        [mod], "o",
        lazy.spawn("feh --bg-fill --randomize /home/sodium/wallpapers-master/")
    ),
    # Switch between windows
    Key(
        [mod], "h",
        lazy.layout.left(),
        desc="Move focus to left"
    ),
    Key(
        [mod], "l",
        lazy.layout.right(),
        desc="Move focus to right"
    ),
    Key(
        [mod], "j",
        lazy.layout.down(),
        desc="Move focus down"
    ),
    Key([mod], "k",
        lazy.layout.up(),
        desc="Move focus up"
        ),
    Key([mod], "space",
        lazy.layout.next(),
        desc="Move window focus to other window"
        ),
    Key(["control", "shift"], "e",
        lazy.spawn("emacsclient -c -a emacs"),
        desc='Doom Emacs'
        ),
    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
        ),
    Key([mod, "shift"], "Tab",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'
        ),




    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"
    ),
    Key(
        [mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"
    ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"
    ),
    Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"
    ),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [mod], "h",
        lazy.layout.grow_left(),
        desc="Grow window to the left"
    ),
    Key(
        [mod], "l",
        lazy.layout.grow_right(),
        desc="Grow window to the right"
    ),
    Key([mod], "j",
        lazy.layout.grow_down(),
        desc="Grow window down"
        ),
    Key(
        [mod], "k",
        lazy.layout.grow_up(),
        desc="Grow window up"
    ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc="Reset all window sizes"
        ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"
    ),
    Key(
        [mod], "Return",
        lazy.spawn(terminal),
        desc="Launch terminal"
    ),
    # Toggle between different layouts as defined below
    Key(
        [mod], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"
    ),
    Key(
        [mod], "w",
        lazy.window.kill(),
        desc="Kill focused window"
    ),

    Key(
        [mod, "control"], "r",
        lazy.restart(),
        desc="Restart Qtile"),
    Key(
        [mod, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"
    ),
    Key(
        [mod], "p",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"
    ),
    Key(
        [mod], "r",
        lazy.spawn(myPrompt),
        desc="Spawn a command using a prompt widget"
    ),
]

group_names = [("WWW", {'layout': 'max'}),
               ("CODE", {'layout': 'ratitile'}),
               ("SYS", {'layout': 'treetab'}),
               ("DOC", {'layout': 'treetab'}),
               ("VBOX", {'layout': 'ratiotile'}),
               ("CHAT", {'layout': 'monadtall'}),
               ("MUS", {'layout': 'monadtall'}),
               ("VID", {'layout': 'floating'}),
               ("GFX", {'layout': 'floating'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group


layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
        font = "mononoki",
        fontsize = 14,
        border_width = 2,
        bg_color = "1c1f24",
        active_bg = "c678dd",
        active_fg = "000000",
        inactive_bg = "a9a1e1",
        inactive_fg = "1c1f24",
        padding_left = 0,
        padding_x = 0,
        padding_y = 5,
        section_top = 10,
        section_bottom = 20,
        level_shift = 8,
        vspace = 3,
        panel_width = 200
    ),
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font="mononoki",
    fontsize = 13,
    padding = 2
)

def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[2],
            background = colors[0]
        ),

        widget.Image(
            filename = "~/qtile/logo.png",
            scale = "False",
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("feh --bg-fill --randomize /home/sodium/wallpapers-master/"),
            		       'Button2': lambda: qtile.cmd_spawn("xscreensaver-command -activate")}
        ),
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[2],
            background = colors[0]
        ),
        widget.GroupBox(
            font = "Ubuntu Bold",
            fontsize = 9,
            margin_y = 3,
            margin_x = 0,
            padding_y = 5,
            padding_x = 3,
            borderwidth = 3,
            active = colors[2],
            inactive = colors[7],
            rounded = False,
            highlight_color = colors[1],
            highlight_method = "line",
            this_current_screen_border = colors[6],
            this_screen_border = colors [4],
            other_current_screen_border = colors[6],
            other_screen_border = colors[4],
            foreground = colors[2],
            background = colors[0]
        ),
        widget.Prompt(
            prompt = myPrompt,
            font = "Ubuntu Mono",
            padding = 10,
            foreground = colors[3],
            background = colors[1]
        ),
        widget.Sep(
            linewidth = 0,
            padding = 40,
            foreground = colors[2],
            background = colors[0]
        ),

        widget.WindowName(
            foreground = colors[6],
            background = colors[0],
            padding = 0
        ),
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors[0],
            background = colors[0]
        ),
        widget.Image(
            filename = "~/.config/qtile/blue.png",
            scale = True,
            background = colors[0]
        ),
        widget.Systray(
            foreground = colors[2],
            background = colors[5],
            padding = 5
        ),
        widget.Image(
            filename = "~/.config/qtile/pink.png",
            scale = True,
            background = colors[5]
        ),
        widget.Net(
            interface = "wlx002e2d5cb58d",
            format = '{down} ↓↑ {up}',
            foreground = colors[2],
            background = colors[4],
            padding = 5
        ),
        widget.Image(
            filename = "~/.config/qtile/blue.png",
            scale = True,
            background = colors[4]
        ),
        widget.TextBox(
            text = "🌡",
            padding = 2,
            foreground = colors[2],
            background = colors[5],
            fontsize = 11
        ),
        widget.ThermalSensor(
            foreground = colors[2],
            background = colors[5],
            threshold = 90,
            padding = 5
        ),

        widget.Image(
            filename = "~/.config/qtile/pink.png",
            scale = True,
            background = colors[5]
        ),
        widget.TextBox(
            text = " ⟳",
            padding = 2,
            foreground = colors[2],
            background = colors[4],
            fontsize = 14
        ),
        widget.CheckUpdates(
            update_interval = 1800,
            distro = "Ubuntu",
            display_format = "{updates} Updates",
            foreground = colors[2],
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo apt full-upgrade')},
            background = colors[4]
        ),

        widget.Image(
            filename = "~/.config/qtile/blue.png",
            scale = True,
            background = colors[4]
        ),
        widget.TextBox(
            text = " 🖬",
            foreground = colors[2],
            background = colors[5],
            padding = 0,
            fontsize = 14
        ),

        widget.Memory(
            foreground = colors[2],
            background = colors[5],
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
            padding = 5
        ),

        widget.Image(
            filename = "~/.config/qtile/pink.png",
            scale = True,
            background = colors[5]
        ),
        widget.TextBox(
            text = " ₿",
            padding = 0,
            foreground = colors[2],
            background = colors[4],
            fontsize = 12
        ),
        widget.CryptoTicker(
            foreground = colors[2],
            background = colors[4],
            padding = 5
        ),

        widget.Image(
            filename = "~/.config/qtile/blue.png",
            scale = True,
            background = colors[4]
        ),
        widget.TextBox(
            text = " Vol:",
            foreground = colors[2],
            background = colors[5],
            padding = 0
        ),
        widget.Volume(
            foreground = colors[2],
            background = colors[5],
            padding = 5
        ),

        widget.Image(
            filename = "~/.config/qtile/pink.png",
            scale = True,
            background = colors[5]
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground = colors[0],
            background = colors[4],
            padding = 0,
            scale = 0.7
        ),
        widget.CurrentLayout(
            foreground = colors[2],
            background = colors[4],
            padding = 5
        ),

        widget.Image(
            filename = "~/.config/qtile/blue.png",
            scale = True,
            background = colors[4]
        ),
        widget.Clock(
            foreground = colors[2],
            background = colors[5],
            format = "%A, %B %d - %H:%M "
        ),
    ]
    return widgets_list



extension_defaults = widget_defaults.copy()

colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]] # backbround for inactive screens

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

#282B50
# Drag floating layouts.

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.8, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('/home/sodium/.config/qtile/autostart.sh')
    subprocess.call([home])
    # XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
    # string besides java UI toolkits; you can see several discussions on the
    # mailing lists, GitHub issues, and other WM documentation that suggest setting
    # this string if your java app doesn't work correctly. We may as well just lie
    # and say that we're a working one by default.
    #
    # We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
    # java that happens to be on java's whitelist.
wmname = "LG3D"
