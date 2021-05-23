from enum import Enum
from PIL import ImageFont, ImageDraw, Image

# plots mode
class ModeRange(Enum):
    VISIBLE = 0
    ALL = 1


class ModeDisplay(Enum):
    TERRAIN = 0
    BATIMENTS = 1
    ALL = 2


# colors definitions
colors_tiles = {
    "A": "black",  # "Abyss"
    "F": "lightgreen",  # "Field"
    "M": "brown",  # "Mountain"
    "R": "gold",  # "Ressource"
    # Bâtiments :
    "W": "gray",  # "Wall"
}
colors_dynamic = {
    (True, True): "blue",
    (True, False): "lightblue",
    (False, True): "red",
    (False, False): "pink",
}
# region Tile identification
def is_terrain(tile):
    return tile["type"] in "AFMR"


def is_batiment(tile):
    return tile["type"] in "CSTW"


def is_army(tile):
    return tile["type"] in "LVH"


def is_ours(tile):
    return tile["ours"]


# endregion
all_positions_lines = []


def draw_tile(draw, size, cord_x, cord_y, tile_A, tile_B, current_modedisplay):
    points = [
        (cord_x + size / 2, cord_y),
        (cord_x, cord_y + size),
        (cord_x + size, cord_y + size),
        (cord_x + 3 * size / 2, cord_y),
    ]
    positions_A = [points[0], points[1], points[2]]
    positions_B = [points[0], points[3], points[2]]
    for (tile, position) in zip([tile_A, tile_B], [positions_A, positions_B]):
        color_final = "white"
        txt_draw = False
        if current_modedisplay in [ModeDisplay.TERRAIN, ModeDisplay.ALL]:
            if is_terrain(tile):
                color_final = colors_tiles[tile["terrain"]]
        if current_modedisplay in [ModeDisplay.BATIMENTS, ModeDisplay.ALL]:
            if is_batiment(tile) or is_army(tile):
                color_final = colors_dynamic[(is_ours(tile), is_batiment(tile))]
                txt_draw = True  # get the name of the tile
            if tile["type"] == "W":
                color_final = colors_tiles[tile["type"]] # useful for walls
                txt_draw = False

        draw.polygon(position, outline="black", fill=color_final)
        if is_batiment(tile):
            for i in range(3):
                all_positions_lines.append([position[i % 3], position[(i + 1) % 3]])

        font = ImageFont.truetype("src/gameviz/fonts/arial.ttf", size=18)
        if txt_draw:
            pos_txt = (
                -5
                + (max([x[0] for x in position]) + min([x[0] for x in position])) / 2,
                -10 + sum([x[1] for x in position]) / 3,
            )

            draw.text(pos_txt, tile["type"], fill="black", font=font)




def get_cord_x(i, j, size, len_x):
    return size * (len_x - 1 / 2 + i - j / 2)


def get_cord_y(i, j, size):
    return size * (1 / 2 + j)


def draw_map(draw, size_img, game_map, mode_range: ModeRange.ALL, mode_display=ModeDisplay.ALL):
    len_x = len(game_map[0]) // 2
    len_y = len(game_map)
    size = min(size_img / (len_y + 1), size_img / (len_x + len_y / 2 + 1))
    for i in range(len_x):
        for j in range(len_y):
            obj_1 = game_map[j][2 * i]
            obj_2 = game_map[j][2 * i + 1]
            draw_tile(
                draw,
                size,
                get_cord_x(i, j, size, len_x),
                size * (1 / 2 + j),
                game_map[j][2 * i],
                game_map[j][2 * i + 1],
                current_modedisplay = mode_display
            )
    for position_line in all_positions_lines:
        draw.line(
            position_line,
            fill="white",
            width=4,
        )
