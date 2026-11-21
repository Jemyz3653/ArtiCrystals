# ArtiCrystals pixel icon

Redrawn in code on 1 November 2026 at the author's request.
The original drawing is a 32×32 RGB pixel grid using a fixed palette of
12 colors. All shapes are integer-coordinate polygons and lines drawn with
Pillow. No image-generation service or external bitmap is used.

The design is a tall red ruby with a shorter cyan crystal and a small golden
crystal against a plain dark background. Large shapes and a small palette
match the simple pixel icons of the author's other Minecraft mods.

## Reproduce

Install Python 3 and Pillow, then run in the project root:

```sh
python tools/draw_icon.py
```

Outputs:

- `docs/articrystals-icon-32.png` — original 32×32 pixel drawing.
- `docs/articrystals-curseforge-icon.png` — 512×512 PNG for CurseForge.
- `src/main/resources/assets/articrystals/icon.png` — 256×256 in-game icon.

Both enlarged files use nearest-neighbour sampling with no antialiasing.
The script is deterministic. Rerunning it produces identical PNG files.
The model gallery renderer preserves this separately maintained icon.
