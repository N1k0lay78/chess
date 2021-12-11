from core.textures.load_image import load_image
from core.textures.Tileset import TileSet

test_image = False
test_tileset = False

if test_tileset:
    tile_set = TileSet('board', (50, 50))
    print(tile_set[63])
    try:
        tile_set[64]
        print("ERROR")
    except Exception:
        print("OK")
    print(tile_set[7,7])
    try:
        tile_set[8, 7]
        print("ERROR")
    except Exception:
        print("OK")
    try:
        tile_set[8, 8]
        print("ERROR")
    except Exception:
        print("OK")
    try:
        tile_set[7, 8]
        print("ERROR")
    except Exception:
        print("OK")
if test_image:
    print(load_image('board'))
