#!/usr/bin/env python3
"""Draw the ArtiCrystals icon on a 32px grid using integer polygons only.

Run: python tools/draw_icon.py
Requires Pillow. No image-generation service, external images or fonts are used.
The 32px master is enlarged with nearest-neighbour sampling, without smoothing.
"""
from pathlib import Path
from PIL import Image, ImageDraw

SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parents[1] if SCRIPT.parent.name == 'tools' else SCRIPT.parent


def draw_icon():
    # A small, fixed palette: flat background, dark outline, three gem colors.
    p = {
        'bg': '#25242b', 'edge': '#121117',
        'cyan_dark': '#1e6e8b', 'cyan': '#37bed1', 'cyan_light': '#a2edf0',
        'red_dark': '#7d193b', 'red': '#bc2b4b',
        'red_light': '#ed5368', 'red_shine': '#ffb2af',
        'gold_dark': '#a75c25', 'gold': '#e2a536', 'gold_light': '#ffe58a',
    }
    im = Image.new('RGB', (32, 32), p['bg'])
    d = ImageDraw.Draw(im)

    def poly(points, color):
        d.polygon(points, fill=p[color])

    # Short quartz point, behind the central ruby.
    poly([(8, 10), (13, 15), (13, 23), (8, 28), (3, 23), (3, 15)], 'edge')
    poly([(8, 12), (11, 15), (8, 18), (5, 15)], 'cyan_light')
    poly([(4, 16), (7, 19), (7, 26), (4, 23)], 'cyan')
    poly([(8, 19), (12, 16), (12, 23), (8, 26)], 'cyan_dark')
    d.line([(5, 17), (5, 22)], fill=p['cyan_light'])

    # A small, broad golden crystal, with its own silhouette.
    poly([(25, 14), (29, 19), (29, 24), (25, 28), (20, 24), (20, 19)], 'edge')
    poly([(25, 16), (27, 19), (25, 21), (22, 19)], 'gold_light')
    poly([(21, 20), (24, 22), (24, 26), (21, 23)], 'gold')
    poly([(25, 22), (28, 20), (28, 24), (25, 26)], 'gold_dark')

    # Main ruby: one clear outline and a few large cut facets.
    poly([(16, 3), (22, 9), (22, 21), (16, 28), (10, 21), (10, 9)], 'edge')
    poly([(16, 5), (20, 9), (16, 12), (12, 9)], 'red_light')
    poly([(11, 10), (15, 13), (15, 25), (11, 21)], 'red')
    poly([(16, 13), (21, 10), (21, 21), (16, 26)], 'red_dark')
    poly([(12, 11), (14, 13), (14, 22), (12, 20)], 'red_light')
    poly([(16, 14), (19, 12), (19, 20), (16, 23)], 'red')
    d.line([(13, 9), (16, 6), (18, 8)], fill=p['red_shine'])
    d.line([(12, 12), (12, 16)], fill=p['red_shine'])
    return im


def main():
    master = draw_icon()
    docs = ROOT / 'docs'
    asset = ROOT / 'src/main/resources/assets/articrystals/icon.png'
    docs.mkdir(parents=True, exist_ok=True)
    asset.parent.mkdir(parents=True, exist_ok=True)
    master.save(docs / 'articrystals-icon-32.png')
    master.resize((256, 256), Image.Resampling.NEAREST).save(asset)
    master.resize((512, 512), Image.Resampling.NEAREST).save(docs / 'articrystals-curseforge-icon.png')
    print(docs / 'articrystals-curseforge-icon.png')


if __name__ == '__main__':
    main()
