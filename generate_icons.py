"""
Generates Minecraft-style pixel art icons as PNG files.
Each icon is 64x64 pixels with the classic Minecraft UI aesthetic:
- Stone/dark grey background with beveled border
- Pixel-art symbol rendered in Minecraft color palette
"""

from PIL import Image, ImageDraw
import os

# Minecraft color palette
MC_COLORS = {
    # Stone button colors (background)
    "stone_light":   (198, 198, 198),
    "stone_mid":     (148, 148, 148),
    "stone_dark":    (100, 100, 100),
    "stone_shadow":  ( 55,  55,  55),
    "border_light":  (255, 255, 255),
    "border_dark":   ( 85,  85,  85),

    # Accent / symbol colors
    "red":           (255,  85,  85),
    "dark_red":      (170,   0,   0),
    "gold":          (255, 170,   0),
    "dark_gold":     (170, 117,   0),
    "green":         ( 85, 255,  85),
    "dark_green":    (  0, 170,   0),
    "white":         (255, 255, 255),
    "light_grey":    (170, 170, 170),
    "grey":          ( 85,  85,  85),
    "black":         (  0,   0,   0),
    "yellow":        (255, 255,  85),
    "blue":          ( 85,  85, 255),
    "aqua":          ( 85, 255, 255),
    "dark_purple":   (170,   0, 170),
    "skull_white":   (210, 210, 210),
    "skull_shadow":  (130, 130, 130),
}

ICON_SIZE = 256
SCALE = 1  # Each "pixel" is 16x16 actual pixels
PIXEL = 16

OUTPUT_DIR = "/workspace/icons"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def new_canvas():
    """Create a blank RGBA canvas."""
    return Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))


def draw_mc_button_bg(img: Image.Image):
    """
    Draw the classic Minecraft stone-button background with a beveled border.
    Border structure (outer → inner):
      1px border_dark  outer shadow
      1px stone_dark   inner shadow
      fill stone_mid   body
      1px stone_light  highlight (top/left inside)
      1px border_light outer highlight
    We simplify to a clean 3-zone bevel that looks like the MC inventory button.
    """
    d = ImageDraw.Draw(img)
    S = ICON_SIZE

    # Fill body
    d.rectangle([0, 0, S - 1, S - 1], fill=MC_COLORS["stone_mid"])

    # Bevel light (top + left edges)
    bevel = [
        (0, 0, S - 1, 0),        # top
        (0, 0, 0, S - 1),        # left
    ]
    for line in bevel:
        d.line(line, fill=MC_COLORS["stone_light"], width=2)

    # Bevel dark (bottom + right edges)
    bevel_dark = [
        (0, S - 2, S - 1, S - 2),   # bottom inner
        (S - 2, 0, S - 2, S - 1),   # right inner
        (0, S - 1, S - 1, S - 1),   # bottom outer
        (S - 1, 0, S - 1, S - 1),   # right outer
    ]
    for line in bevel_dark:
        d.line(line, fill=MC_COLORS["stone_shadow"])

    # Slightly darker center fill for depth
    d.rectangle([2, 2, S - 3, S - 3], fill=MC_COLORS["stone_mid"])

    # Pixel noise pattern (subtle texture like MC stone)
    for y in range(4, S - 4, 8):
        for x in range(4, S - 4, 8):
            d.point((x, y), fill=MC_COLORS["stone_dark"])
            d.point((x + 4, y + 4), fill=MC_COLORS["stone_light"])


def px(x, y):
    """Convert grid coords (in 4-px units) to pixel coords."""
    return x * PIXEL, y * PIXEL


def draw_pixel(d, gx, gy, color, size=1):
    """Draw a minecraft 'pixel' (4x4 block) at grid position (gx, gy)."""
    x0, y0 = gx * PIXEL, gy * PIXEL
    x1, y1 = x0 + PIXEL * size - 1, y0 + PIXEL * size - 1
    d.rectangle([x0, y0, x1, y1], fill=color)


def draw_pixels(d, pixel_map, ox=0, oy=0):
    """
    Draw a list of (gx, gy, color_key) tuples.
    ox, oy are grid-unit offsets.
    """
    for item in pixel_map:
        gx, gy, ck = item
        draw_pixel(d, gx + ox, gy + oy, MC_COLORS[ck])


# ─────────────────────────────────────────────
#  FORFEIT  –  A white flag being waved / planted
#  (Classic "surrender" flag: pole + white flag with grey shadow)
# ─────────────────────────────────────────────
def make_forfeit():
    img = new_canvas()
    draw_mc_button_bg(img)
    d = ImageDraw.Draw(img)

    # Grid is 16x16 over 64x64 canvas
    # Pole: column 3, rows 1-13
    pole = [(3, r, "grey") for r in range(1, 14)]
    # Pole shadow
    pole_shadow = [(4, r, "stone_shadow") for r in range(2, 14)]

    # Flag body (rows 1-6, cols 4-10) — white with shadow detail
    flag = []
    for r in range(1, 7):
        for c in range(4, 11):
            flag.append((c, r, "white"))
    # Shadow side of flag (right col + bottom row)
    flag_shadow = [(10, r, "light_grey") for r in range(1, 7)]
    flag_shadow += [(c, 6, "light_grey") for c in range(4, 11)]

    # Red X on flag = surrender / forfeit
    x_mark = [
        (5, 2, "red"), (6, 3, "red"), (7, 4, "red"), (8, 5, "red"),
        (8, 2, "red"), (7, 3, "red"), (6, 4, "red"), (5, 5, "red"),
        # Dark shadow pixels
        (5, 3, "dark_red"), (8, 3, "dark_red"),
    ]

    draw_pixels(d, pole)
    draw_pixels(d, pole_shadow)
    draw_pixels(d, flag)
    draw_pixels(d, flag_shadow)
    draw_pixels(d, x_mark)

    # Ground base
    ground = [(c, 13, "stone_dark") for c in range(2, 6)]
    draw_pixels(d, ground)

    img.save(os.path.join(OUTPUT_DIR, "forfeit.png"))
    print("✓ forfeit.png")


# ─────────────────────────────────────────────
#  RETURN TO GAME  –  A door with an arrow
# ─────────────────────────────────────────────
def make_return_to_game():
    img = new_canvas()
    draw_mc_button_bg(img)
    d = ImageDraw.Draw(img)

    # Door frame (outer) cols 2-8, rows 2-13
    door_frame = []
    for r in range(2, 14):
        for c in range(2, 9):
            door_frame.append((c, r, "stone_dark"))

    # Door inner (open) – lighter wood color inside cols 3-7, rows 3-13
    door_inner = []
    for r in range(3, 14):
        for c in range(3, 8):
            door_inner.append((c, r, "dark_gold"))

    # Door panel details
    door_detail = [
        (4, 4, "gold"), (5, 4, "gold"), (6, 4, "gold"),
        (4, 5, "gold"), (6, 5, "gold"),
        (4, 6, "gold"), (5, 6, "gold"), (6, 6, "gold"),
        (4, 8, "gold"), (5, 8, "gold"), (6, 8, "gold"),
        (4, 9, "gold"), (6, 9, "gold"),
        (4, 10, "gold"), (5, 10, "gold"), (6, 10, "gold"),
        # knob
        (7, 8, "light_grey"),
    ]

    # Arrow pointing INTO door (right-facing) cols 9-13, row 7-9
    arrow = [
        # shaft
        (9, 8, "green"), (10, 8, "green"), (11, 8, "green"),
        # arrowhead
        (12, 7, "green"), (12, 8, "green"), (12, 9, "green"),
        (13, 8, "green"),
        # shadow
        (9, 9, "dark_green"), (10, 9, "dark_green"),
        (12, 10, "dark_green"),
    ]

    draw_pixels(d, door_frame)
    draw_pixels(d, door_inner)
    draw_pixels(d, door_detail)
    draw_pixels(d, arrow)

    img.save(os.path.join(OUTPUT_DIR, "return_to_game.png"))
    print("✓ return_to_game.png")


# ─────────────────────────────────────────────
#  RESTART  –  Circular arrow (refresh symbol)
# ─────────────────────────────────────────────
def make_restart():
    img = new_canvas()
    draw_mc_button_bg(img)
    d = ImageDraw.Draw(img)

    # Draw circular arrow using pixel art – 16x16 grid
    # Arc pixels: approximate circle ring at radius ~5 with a gap + arrowhead
    arc_pixels = [
        # Top arc (left half going counterclockwise from top)
        (8, 2, "gold"),
        (7, 2, "gold"), (6, 3, "gold"),
        (5, 4, "gold"), (4, 5, "gold"),
        (4, 6, "gold"), (4, 7, "gold"),
        (5, 8, "gold"), (5, 9, "gold"),
        (6, 10, "gold"), (7, 10, "gold"),
        (8, 10, "gold"),
        # Right half
        (9, 10, "gold"), (10, 10, "gold"),
        (11, 9, "gold"),
        (12, 8, "gold"), (12, 7, "gold"),
        (12, 6, "gold"), (12, 5, "gold"),
        (11, 4, "gold"),
        (10, 3, "gold"), (9, 2, "gold"),
        # Shadow strip
        (8, 3, "dark_gold"), (7, 3, "dark_gold"),
        (5, 5, "dark_gold"), (4, 8, "dark_gold"),
        (6, 11, "dark_gold"), (9, 11, "dark_gold"),
        (12, 9, "dark_gold"), (11, 3, "dark_gold"),
    ]

    # Arrowhead at top-right (pointing right/clockwise direction)
    arrow_head = [
        (10, 1, "gold"),
        (11, 2, "gold"),
        (10, 2, "gold"),
        (11, 1, "gold"),
        (12, 2, "gold"),
        # shadow
        (11, 3, "dark_gold"),
    ]

    # Inner circle (hole)
    inner_hole = [
        (7, 5, "stone_mid"), (8, 5, "stone_mid"), (9, 5, "stone_mid"),
        (6, 6, "stone_mid"), (7, 6, "stone_mid"), (8, 6, "stone_mid"), (9, 6, "stone_mid"), (10, 6, "stone_mid"),
        (6, 7, "stone_mid"), (7, 7, "stone_mid"), (8, 7, "stone_mid"), (9, 7, "stone_mid"), (10, 7, "stone_mid"),
        (6, 8, "stone_mid"), (7, 8, "stone_mid"), (8, 8, "stone_mid"), (9, 8, "stone_mid"), (10, 8, "stone_mid"),
        (7, 9, "stone_mid"), (8, 9, "stone_mid"), (9, 9, "stone_mid"),
    ]

    draw_pixels(d, arc_pixels)
    draw_pixels(d, inner_hole)
    draw_pixels(d, arrow_head)

    img.save(os.path.join(OUTPUT_DIR, "restart.png"))
    print("✓ restart.png")


# ─────────────────────────────────────────────
#  PAUSE  –  Two vertical bars (classic pause symbol)
# ─────────────────────────────────────────────
def make_pause():
    img = new_canvas()
    draw_mc_button_bg(img)
    d = ImageDraw.Draw(img)

    # Left bar: cols 4-6, rows 3-12
    # Right bar: cols 9-11, rows 3-12
    bar_color = "white"
    bar_shadow = "light_grey"

    bars = []
    for r in range(3, 13):
        for c in range(4, 7):
            bars.append((c, r, bar_color))
        for c in range(9, 12):
            bars.append((c, r, bar_color))

    # Shadow (right edge of each bar, bottom edge)
    shadows = []
    for r in range(3, 13):
        shadows.append((6, r, bar_shadow))
        shadows.append((11, r, bar_shadow))
    for c in range(4, 7):
        shadows.append((c, 12, bar_shadow))
    for c in range(9, 12):
        shadows.append((c, 12, bar_shadow))

    draw_pixels(d, bars)
    draw_pixels(d, shadows)

    img.save(os.path.join(OUTPUT_DIR, "pause.png"))
    print("✓ pause.png")


# ─────────────────────────────────────────────
#  DEATH  –  Minecraft skull (like the death screen skull)
# ─────────────────────────────────────────────
def make_death():
    img = new_canvas()
    draw_mc_button_bg(img)
    d = ImageDraw.Draw(img)

    # Skull shape – 16x16 pixel grid
    # Skull head outline
    skull_body = []
    # Top rounded part of skull (rows 1-6)
    for r in range(2, 8):
        for c in range(3, 13):
            skull_body.append((c, r, "skull_white"))

    # Remove corners to round the skull
    corners = [(3, 2), (12, 2), (3, 7), (12, 7)]
    skull_body = [p for p in skull_body if (p[0], p[1]) not in corners]

    # Eye sockets (dark holes)
    left_eye = [(4, 4), (5, 4), (4, 5), (5, 5)]
    right_eye = [(9, 4), (10, 4), (9, 5), (10, 5)]
    eyes = [(c, r, "stone_shadow") for c, r in left_eye + right_eye]

    # Nose bridge
    nose = [(7, 5, "stone_shadow"), (8, 5, "stone_shadow")]

    # Jaw area (rows 8-10)
    jaw = []
    for r in range(8, 11):
        for c in range(4, 12):
            jaw.append((c, r, "skull_white"))
    # Jaw teeth gaps
    teeth_gaps = [
        (5, 9), (5, 10), (7, 9), (7, 10), (9, 9), (9, 10), (11, 9), (11, 10),
    ]
    jaw = [p for p in jaw if (p[0], p[1]) not in teeth_gaps]

    # Teeth color fill (visible between gaps — actually the background shows through)
    teeth_dark = [(c, r, "stone_shadow") for c, r in teeth_gaps]

    # Shadow on skull (right side + bottom)
    skull_shadow = []
    for r in range(2, 11):
        skull_shadow.append((12, r, "skull_shadow"))
    for c in range(3, 12):
        skull_shadow.append((c, 10, "skull_shadow"))

    # Red X eyes for "dead" look (overlay on eye sockets)
    red_x = [
        (4, 4, "red"), (5, 5, "red"),
        (5, 4, "red"), (4, 5, "red"),
        (9, 4, "red"), (10, 5, "red"),
        (10, 4, "red"), (9, 5, "red"),
        # shadow
        (4, 6, "dark_red"), (9, 6, "dark_red"),
    ]

    # Crossed bones below skull (rows 11-14)
    bone_h = [(c, 12, "skull_white") for c in range(2, 14)]
    bone_v = [(7, r, "skull_white") for r in range(11, 15)]
    bone_v += [(8, r, "skull_white") for r in range(11, 15)]
    bone_ends = [
        (2, 11, "skull_white"), (2, 12, "skull_white"), (2, 13, "skull_white"),
        (13, 11, "skull_white"), (13, 12, "skull_white"), (13, 13, "skull_white"),
        (6, 13, "skull_white"), (9, 13, "skull_white"),
        (6, 14, "skull_white"), (7, 14, "skull_white"), (8, 14, "skull_white"), (9, 14, "skull_white"),
    ]

    draw_pixels(d, skull_body)
    draw_pixels(d, jaw)
    draw_pixels(d, skull_shadow)
    draw_pixels(d, eyes)
    draw_pixels(d, nose)
    draw_pixels(d, teeth_dark)
    draw_pixels(d, red_x)
    draw_pixels(d, bone_h)
    draw_pixels(d, bone_v)
    draw_pixels(d, bone_ends)

    img.save(os.path.join(OUTPUT_DIR, "death.png"))
    print("✓ death.png")


if __name__ == "__main__":
    print("Generating Minecraft-style icons…")
    make_forfeit()
    make_return_to_game()
    make_restart()
    make_pause()
    make_death()
    print(f"\nAll icons saved to: {OUTPUT_DIR}")
