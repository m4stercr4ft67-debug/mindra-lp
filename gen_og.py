from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
NAVY   = (6, 13, 31)
BLUE   = (14, 65, 148)
BLUE_L = (26, 90, 191)
ORANGE = (236, 103, 25)
WHITE  = (240, 244, 255)
GREY   = (160, 175, 200)

img = Image.new("RGB", (W, H), NAVY)
draw = ImageDraw.Draw(img)

# Gradient background: vertical, navy → blue-ish
for y in range(H):
    t = y / H
    r = int(NAVY[0] + (BLUE[0] - NAVY[0]) * t * 0.6)
    g = int(NAVY[1] + (BLUE[1] - NAVY[1]) * t * 0.6)
    b = int(NAVY[2] + (BLUE[2] - NAVY[2]) * t * 0.6)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Decorative circle (large, blurred look via multiple transparent circles)
for i in range(20, 0, -1):
    alpha = int(8 * i / 20)
    r_ = 280 + (20 - i) * 4
    cx, cy = W - 160, 80
    draw.ellipse([cx - r_, cy - r_, cx + r_, cy + r_],
                 fill=(BLUE[0], BLUE[1], BLUE[2]))

# Orange bar at bottom
draw.rectangle([0, H - 8, W, H], fill=ORANGE)

# Orange accent top-left line
draw.rectangle([0, 0, 4, H], fill=ORANGE)

# Load fonts (system fonts fallback)
def load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/SegoeUI-Bold.ttf" if bold else "C:/Windows/Fonts/SegoeUI.ttf",
        "C:/Windows/Fonts/Arial Bold.ttf" if bold else "C:/Windows/Fonts/Arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

font_brand  = load_font(52, bold=True)
font_title  = load_font(72, bold=True)
font_sub    = load_font(30)
font_tag    = load_font(22)

# Logo image (branca)
logo_path = "C:/claude code/clientes/mindra/mindra-lp/assets/logo-branca.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    logo_w = 280
    ratio = logo_w / logo.width
    logo_h = int(logo.height * ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo, (72, 72), logo)
    text_y = 72 + logo_h + 40
else:
    # Fallback: text logo
    draw.text((72, 72), "mindra", font=font_brand, fill=WHITE)
    text_y = 160

# Main headline
headline = "Blog Mindra"
draw.text((72, text_y), headline, font=font_title, fill=WHITE)

# Subheadline
bb = draw.textbbox((0, 0), headline, font=font_title)
text_y += (bb[3] - bb[1]) + 20

sub = "Gestão de Riscos Psicossociais & NR-1"
draw.text((72, text_y), sub, font=font_sub, fill=GREY)

# Tags row
tag_y = H - 60
tags = ["NR-1", "Saúde Mental", "RH Corporativo", "Compliance"]
tx = 72
for tag in tags:
    bb = draw.textbbox((0, 0), tag, font=font_tag)
    tw = bb[2] - bb[0] + 24
    th = bb[3] - bb[1] + 12
    draw.rounded_rectangle([tx, tag_y, tx + tw, tag_y + th],
                            radius=6, fill=BLUE)
    draw.text((tx + 12, tag_y + 6), tag, font=font_tag, fill=WHITE)
    tx += tw + 12

out = "C:/claude code/clientes/mindra/mindra-lp/assets/og-blog.png"
img.save(out, "PNG", optimize=True)
print(f"Salvo: {out}  ({W}x{H})")
