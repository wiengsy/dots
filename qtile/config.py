import os
import subprocess
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal


mod = "mod1"
terminal = "kitty"

green = "008000"
black = "000000"
gray  = "808080"
red   = "ff0000"

@lazy.function
def focusfloat(qtile):
    group = qtile.current_screen.group
    desire = not qtile.current_window.floating
    for window in group.windows:
        if window.floating == desire:
            group.focus(window)
            break



keys = [
    Key([mod, "control"], "t", lazy.spawn(os.path.expanduser("~/src/qtile/scripts/xephyr")), desc="spawn test window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "o", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "q", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen",),
    Key([mod], "b", lazy.hide_show_bar()),
    Key([mod], "z", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),
    Key([mod, "shift"], "space", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "space", focusfloat(), desc="toggle focus floating"),

    # pactl
    Key(["mod4"], "k", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key(["mod4"], "j", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%")),

    # playerctl 
    Key(["mod4"], "h", lazy.spawn("playerctl previous")),
    Key(["mod4"], "l", lazy.spawn("playerctl next")),


    # apps
    Key([mod], "e", lazy.spawn("rofi -show drun")),
    Key([mod], "p", lazy.spawn("rofi -show power")),
    Key([mod], "u", lazy.spawn(os.path.expanduser("~/.config/qtile/scripts/swapCapsEsc")), desc="esc/capslock"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

groups = [
        Group("a", label = "󰍳"),
        Group("s", label = "󰍳"),
        Group("d", label = "󰍳"),
        Group("f", label = "󰍳"),
        Group("g", label = "󰍳", matches=[Match(wm_class="mpv")]), 
        Group("1", label = "󰍳"),
        Group("2", label = "󰍳"),
        Group("3", label = "󰍳"),
        Group("4", label = "󰍳")]

for i in groups:
    keys.extend(
        [
            Key(
                [mod], i.name,
                lazy.group[i.name].toscreen(),
            ),

            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
            ),
        ]
    )

layouts = [
    layout.Columns(
        border_focus=[green],
        border_normal=["#123524"],
        border_width=5
    ),
    layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

floating_layout = layout.Floating(
    border_focus=[green],
    border_normal=["#123524"],
    border_width=5,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)



widget_defaults = dict(
    font="JetBrainsMono",
    foreground=gray,
    background="#000000",
    fontsize=19,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper="/home/wiengsy/pictures/Creeper.png",
        wallpaper_mode="stretch",

        bottom=bar.Bar(
            [
                 widget.Prompt(
                     foreground="#d75f5f"
                 ),

                widget.GroupBox(
                    fontsize=25,
                    margin=3,  
                    padding=2,
                    highlight_method="border",
                    borderwidth=0,

                    block_highlight_text_color="#ffffff",
                    active=green,
                    inactive="#404040",
                ),



                    
                widget.Sep(
                    padding=10,
                    linewidth=4,
                    size_percent=100,
                    foreground=green
                ),


                widget.CurrentLayoutEx(exclude="columns", foreground="#ff0000"),



                # midle
                widget.Spacer(background="#00000000"),
            
                widget.Sep(
                    padding=10,
                    linewidth=4,
                    size_percent=100,
                    foreground=green
                ),

                widget.TextBox(
                    text="", 
                    mouse_callbacks={"Button1":lazy.window.kill()},
                    foreground=green
                    ),

                widget.Sep(
                    padding=10,
                    linewidth=4,
                    size_percent=100,
                    foreground=green
                ),

                widget.TextBox(text="Reg:"),
                widget.Clipboard(
                    max_width=20,
                    timeout=0
                ),

                widget.Sep(
                    padding=10,
                    linewidth=4,
                    size_percent=100,
                    foreground=green
                ),

                widget.TextBox(text=""),

                widget.Clock(),

                widget.Sep(
                    padding=10,
                    linewidth=4,
                    size_percent=100,
                    foreground=green
                ),

                widget.Volume(
                    mute_foreground=red,
                    step=5,
                    padding=0,
                    fontsize=20,
                    emoji=True,
                    emoji_list=["󰖁","󰕿","󰖀","󰕾"],
                    ),
                widget.Volume(
                    mute_foreground=red,
                    step=5,
                    unmute_format="{volume}"
                    ),

                widget.Sep(
                    padding=10,
                    linewidth=4,
                    size_percent=100,
                    foreground=green
                ),


                widget.TextBox(
                        foreground=green,
                        mouse_callbacks={"Button1":lazy.spawn("rofi -show power")},
                        text="",
                        ),

                widget.Sep(
                    padding=0,
                    linewidth=5,
                    size_percent=100,
                    foreground=black
                ),



            ],
            25,
            background="#00000000",
            border_width=[3, 4, 3, 4],
            border_color=["#008000", "#008000", "#008000", "#008000"]
        ),
    ),
]


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wl_input_rules = None




@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('/home/wiengsy/.config/qtile/autostart.sh')
    subprocess.call(home)





# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"





# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )
