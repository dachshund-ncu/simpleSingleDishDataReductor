from PyQt5.QtGui import QIcon
import os
icon_cat = os.path.dirname(__file__)
# -- generate icons --
confirmation_icon = QIcon(os.path.join(icon_cat, "check-solid.svg"))
satellite_dish = QIcon(os.path.join(icon_cat, "satellite-dish-solid.svg"))
x_mark_icon = QIcon(os.path.join(icon_cat, "xmark-solid.svg"))
arrow_left_icon = QIcon(os.path.join(icon_cat, "arrow-left-solid.svg"))
arrow_right_icon = QIcon(os.path.join(icon_cat, "arrow-right-solid.svg"))
trash_can_icon = QIcon(os.path.join(icon_cat, "trash-can-solid.svg"))
eraser_icon = QIcon(os.path.join(icon_cat, "eraser-solid.svg"))
chart_line_icon = QIcon(os.path.join(icon_cat, "chart-line-solid.svg"))
robot_icon = QIcon(os.path.join(icon_cat, "robot-solid.svg"))
square_minus_icon = QIcon(os.path.join(icon_cat, "square-minus-regular.svg"))
rectangle_xmark_icon = QIcon(os.path.join(icon_cat, "rectangle-xmark-regular.svg"))
ban_icon = QIcon(os.path.join(icon_cat, "ban-solid.svg"))
minus_solid_icon = QIcon(os.path.join(icon_cat, "minus-solid.svg"))
flag_icon = QIcon(os.path.join(icon_cat, "flag-checkered-solid.svg"))
play_icon = QIcon(os.path.join(icon_cat, "play-solid.svg"))
bars_icon = QIcon(os.path.join(icon_cat, "bars-solid.svg"))
rotate_icon = QIcon(os.path.join(icon_cat, "rotate-left-solid.svg"))
paper_plane = QIcon(os.path.join(icon_cat, "paper-plane-regular.svg"))
weight_red = QIcon(os.path.join(icon_cat, "weight-scale-solid-red.svg"))
weight_white = QIcon(os.path.join(icon_cat, "weight-scale-solid-white.svg"))
gears_icon = QIcon(os.path.join(icon_cat, "gears-solid.svg"))
magn_glass_icon = QIcon(os.path.join(icon_cat, "magnifying-glass-plus-solid.svg"))
house_icon = QIcon(os.path.join(icon_cat, "house-solid.svg"))


__all__ = [
    "confirmation_icon",
    "satellite_dish",
    "x_mark_icon",
    "arrow_left_icon",
    "arrow_right_icon",
    "trash_can_icon",
    "eraser_icon",
    "chart_line_icon",
    "robot_icon",
    "square_minus_icon",
    "ban_icon",
    "minus_solid_icon",
    "flag_icon",
    "play_icon",
    "bars_icon",
    "rotate_icon",
    "paper_plane",
    "weight_red",
    "weight_white",
    "gears_icon",
    "magn_glass_icon",
    "house_icon"
]