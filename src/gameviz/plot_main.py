# %%
from PIL import ImageFont, ImageDraw, Image
from enum import Enum
import plot_tools as plot_tools
import json
import os
import shutil
from tqdm import tqdm
source_file = "game_logs/summon_game.json"
target_dir = "summon_game"
with open(source_file,'r') as file:
    data = json.load(file)
# data["state_0"](is_ours(tile), is_batiment(tile))
# %%
size_img = 1000
current_moderange = plot_tools.ModeRange.ALL
current_modedisplay = plot_tools.ModeDisplay.ALL
dirpath = f"game_viz/{target_dir}"
if os.path.exists(dirpath) and os.path.isdir(dirpath):
    shutil.rmtree(dirpath)
os.makedirs(dirpath)
border_lgd = 200
for index, state in tqdm(enumerate(data), total = len(data)):
    game_map = state["map_representation"]
    
    im = Image.new(mode = 'RGB', size = (size_img+border_lgd,size_img))
    draw = ImageDraw.Draw(im)
    draw.polygon([(0,0), (0, size_img), (size_img+border_lgd,size_img), (size_img+border_lgd, 0)], fill = 'white')
    plot_tools.draw_map(draw, size_img, game_map, current_moderange)

    font_lgd = ImageFont.truetype("src/gameviz/fonts/arial.ttf", size=30)
    draw.text((size_img, size_img//10), text=f"Balance : {state['balance']}", font = font_lgd, fill="black")
    im.save(f'game_viz/{target_dir}/{index:04d}.png')




    
