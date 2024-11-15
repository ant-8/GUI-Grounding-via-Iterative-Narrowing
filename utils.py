import json
from PIL import Image, ImageDraw, ImageFont
import re

def extract_tuple_from_string(input_string):
    matches = re.findall(r'(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)[\)\]]', input_string)
    if matches:
        x, y = float(matches[-1][0]), float(matches[-1][1])
        return (x, y)
    else:
        return None

def load_screenspot_ds():
    result = {}
    
    for mode in ['desktop', 'mobile', 'web']:
        with open(f'./screenspot/screenspot_{mode}.json', 'r') as f:
            data = json.load(f)
            
        entries = {
            "text": [],
            "icon": []
        }
        
        for x in data:
            row = {
                "image": Image.open(f"./screenspot/images/{x['img_filename']}"),
                "target": x["instruction"],
                "bbox": x["bbox"],
                "data_type": x["data_type"]
            }
            entries[row["data_type"]].append(row)
    
        result[mode] = entries
    return result

def render_crosshair_center(image):
    rendered_image = image.copy()
    draw = ImageDraw.Draw(rendered_image)
    width, height = image.size
    center_x = width // 2
    center_y = height // 2
    line_color = "blue"
    line_width = 3

    draw.line([(center_x, 0), (center_x, height)], fill=line_color, width=line_width)
    draw.line([(0, center_y), (width, center_y)], fill=line_color, width=line_width)
    return rendered_image

def render_crosshair(image, x, y):
    rendered_image = image.copy()
    draw = ImageDraw.Draw(rendered_image)
    width, height = image.size

    line_color = "blue"
    line_width = 2

    draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)
    draw.line([(0, y), (width, y)], fill=line_color, width=line_width)

    return rendered_image

def draw_bbox_on_image(image, bbox_coords, color='blue', width=3):
    image = image.copy()
    draw = ImageDraw.Draw(image)
    draw.rectangle(bbox_coords, outline=color, width=width)
    return image

def is_in_bbox(bbox, x, y):
    x_min, y_min, width, height = bbox
    x_max = x_min + width
    y_max = y_min + height
    return x_min <= x <= x_max and y_min <= y <= y_max

def get_bbox_midpoint(bbox):
    x_min, y_min, width, height = bbox
    x_mid = x_min + (width / 2)
    y_mid = y_min + (height / 2)
    
    return (x_mid, y_mid)