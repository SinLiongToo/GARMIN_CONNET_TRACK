"""
Generate high-resolution PWA and Apple Touch icons for Garmin Connect Track WebApp.
Renders crisp modern athletic icons with Garmin blue & emerald pulse accents.
"""
from pathlib import Path
from PIL import Image, ImageDraw

def create_icon(size: int, is_maskable: bool = False) -> Image.Image:
    # Render at 4x resolution for super-sampled anti-aliasing
    scale = 4
    canvas_size = size * scale
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background
    bg_radius = 0 if is_maskable else int(canvas_size * 0.22)
    # Outer rounded rect or full square for maskable
    margin = 0 if is_maskable else int(canvas_size * 0.02)
    
    # Gradient-like background simulation
    draw.rounded_rectangle(
        [margin, margin, canvas_size - margin, canvas_size - margin],
        radius=bg_radius,
        fill=(15, 23, 42, 255) # slate-900
    )

    # Subtle inner border
    draw.rounded_rectangle(
        [margin, margin, canvas_size - margin, canvas_size - margin],
        radius=bg_radius,
        outline=(56, 189, 248, 70), # sky-400 with opacity
        width=int(4 * scale)
    )

    # Effective content center & radius (safe zone for maskable is 80% diameter)
    cx, cy = canvas_size // 2, canvas_size // 2
    r_outer = int(canvas_size * (0.32 if is_maskable else 0.36))

    # Outer activity ring (Garmin Cyan to Emerald)
    ring_width = int(10 * scale)
    draw.arc(
        [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer],
        start=135,
        end=405,
        fill=(0, 124, 195, 255), # Garmin Blue
        width=ring_width
    )
    # Emerald accent arc
    draw.arc(
        [cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer],
        start=315,
        end=390,
        fill=(16, 185, 129, 255), # Emerald-500
        width=ring_width
    )

    # Stylized Heart Rate & Speed Pulse Line through center
    pulse_width = int(8 * scale)
    pts = [
        (cx - int(r_outer * 0.72), cy),
        (cx - int(r_outer * 0.36), cy),
        (cx - int(r_outer * 0.18), cy - int(r_outer * 0.42)),
        (cx - int(r_outer * 0.02), cy + int(r_outer * 0.48)),
        (cx + int(r_outer * 0.16), cy - int(r_outer * 0.28)),
        (cx + int(r_outer * 0.32), cy + int(r_outer * 0.08)),
        (cx + int(r_outer * 0.44), cy),
        (cx + int(r_outer * 0.72), cy),
    ]
    draw.line(pts, fill=(56, 189, 248, 255), width=pulse_width, joint="curve")

    # Athletic runner dot / apex highlight
    apex_x, apex_y = pts[2]
    dot_r = int(7 * scale)
    draw.ellipse([apex_x - dot_r, apex_y - dot_r, apex_x + dot_r, apex_y + dot_r], fill=(251, 191, 36, 255)) # amber-400

    # Downsample with Lanczos
    return img.resize((size, size), Image.Resampling.LANCZOS)

def main():
    icons_dir = Path("assets/icons")
    icons_dir.mkdir(parents=True, exist_ok=True)

    targets = [
        ("icon-192.png", 192, False),
        ("icon-512.png", 512, False),
        ("icon-maskable-192.png", 192, True),
        ("icon-maskable-512.png", 512, True),
        ("apple-touch-icon.png", 180, False),
    ]

    for fname, size, is_maskable in targets:
        out_path = icons_dir / fname
        icon = create_icon(size, is_maskable)
        icon.save(out_path, format="PNG", optimize=True)
        print(f"[OK] Generated {out_path} ({size}x{size}, maskable={is_maskable})")

if __name__ == "__main__":
    main()
