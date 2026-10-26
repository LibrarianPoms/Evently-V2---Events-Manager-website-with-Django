from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os
import math
from PIL.ImageColor import getrgb
import random

def create_gradient(width, height, color1, color2, direction='horizontal'):
    """Create a gradient image between two colors"""
    base = Image.new('RGBA', (width, height), color1)
    top = Image.new('RGBA', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    
    if direction == 'horizontal':
        for y in range(height):
            for x in range(width):
                mask_data.append(int(255 * (x / width)))
    elif direction == 'vertical':
        for y in range(height):
            for x in range(width):
                mask_data.append(int(255 * (y / height)))
    elif direction == 'radial':
        center_x, center_y = width // 2, height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)
        for y in range(height):
            for x in range(width):
                dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                mask_data.append(int(255 * (dist / max_dist)))
    
    mask.putdata(mask_data)
    return Image.composite(top, base, mask)

def add_text_with_effects(img, text, position, font_size, font_color, shadow=True, glow=False):
    """Add text with shadow and/or glow effects"""
    draw = ImageDraw.Draw(img)
    
    # Try to load a custom font, fall back to default if not available
    try:
        font_path = os.path.join('static', 'fonts', 'OpenSans-Bold.ttf')
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Create a temporary image for the text
    text_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    
    # Add shadow
    if shadow:
        shadow_offset = max(2, font_size // 20)
        shadow_color = (0, 0, 0, 100)
        text_draw.text((position[0] + shadow_offset, position[1] + shadow_offset), 
                      text, font=font, fill=shadow_color)
    
    # Add glow
    if glow:
        glow_iterations = 10
        glow_color = (*font_color[:3], 50)  # Semi-transparent version of font color
        for i in range(glow_iterations):
            offset = i + 1
            text_draw.text((position[0] - offset, position[1]), text, font=font, fill=glow_color)
            text_draw.text((position[0] + offset, position[1]), text, font=font, fill=glow_color)
            text_draw.text((position[0], position[1] - offset), text, font=font, fill=glow_color)
            text_draw.text((position[0], position[1] + offset), text, font=font, fill=glow_color)
    
    # Add main text
    text_draw.text(position, text, font=font, fill=font_color)
    
    # Apply slight blur to the text for smoothing
    text_img = text_img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Composite the text onto the original image
    return Image.alpha_composite(img.convert('RGBA'), text_img)

def create_beautiful_logo():
    # Create a new image with transparent background
    width, height = 600, 200
    logo = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # Modern color palette
    primary_color = (41, 128, 185)  # Blue
    secondary_color = (52, 152, 219)  # Lighter blue
    accent_color = (231, 76, 60)  # Red
    
    # Create a gradient background for the logo
    gradient = create_gradient(width, height, (*primary_color, 40), (*secondary_color, 40), 'horizontal')
    logo = Image.alpha_composite(logo, gradient)
    
    # Add a decorative element - abstract event symbol
    symbol_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    symbol_draw = ImageDraw.Draw(symbol_img)
    
    # Draw a stylized calendar/event icon
    icon_size = 80
    icon_x = width // 4 - icon_size // 2
    icon_y = height // 2 - icon_size // 2
    
    # Calendar outline
    symbol_draw.rounded_rectangle(
        [icon_x, icon_y, icon_x + icon_size, icon_y + icon_size],
        radius=10,
        fill=(*accent_color, 220),
        outline=None
    )
    
    # Calendar top bar
    symbol_draw.rounded_rectangle(
        [icon_x, icon_y, icon_x + icon_size, icon_y + icon_size // 5],
        radius=5,
        fill=(255, 255, 255, 220),
        outline=None
    )
    
    # Calendar grid lines
    line_spacing = icon_size // 4
    line_y = icon_y + icon_size // 4
    for i in range(3):
        symbol_draw.line(
            [(icon_x + 10, line_y + i * line_spacing), 
             (icon_x + icon_size - 10, line_y + i * line_spacing)],
            fill=(255, 255, 255, 180),
            width=2
        )
    
    # Add highlight to the icon
    for i in range(5):
        symbol_draw.rounded_rectangle(
            [icon_x - i, icon_y - i, icon_x + icon_size - i, icon_y + icon_size - i],
            radius=10,
            fill=None,
            outline=(255, 255, 255, 10 + i * 5)
        )
    
    # Apply blur to the symbol for a soft effect
    symbol_img = symbol_img.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Composite the symbol onto the logo
    logo = Image.alpha_composite(logo, symbol_img)
    
    # Add the main text "Evently"
    text_position = (width // 3, height // 2 - 30)
    logo = add_text_with_effects(
        logo, 
        "Evently", 
        text_position, 
        80, 
        (255, 255, 255, 255),
        shadow=True,
        glow=True
    )
    
    # Add tagline
    tagline_position = (width // 3 + 10, height // 2 + 40)
    logo = add_text_with_effects(
        logo, 
        "Event Management Made Simple", 
        tagline_position, 
        20, 
        (255, 255, 255, 220),
        shadow=True,
        glow=False
    )
    
    # Save the logo
    static_dir = os.path.join('static', 'images')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    logo_path = os.path.join(static_dir, 'evently_logo.png')
    logo.save(logo_path)
    print(f"Beautiful logo saved to {logo_path}")
    
    # Create a smaller version for the navbar
    navbar_logo = logo.copy()
    navbar_logo = navbar_logo.resize((240, 80), Image.LANCZOS)
    navbar_logo_path = os.path.join(static_dir, 'evently_logo_small.png')
    navbar_logo.save(navbar_logo_path)
    print(f"Navbar logo saved to {navbar_logo_path}")
    
    # Create a favicon
    favicon_size = 32
    favicon = Image.new('RGBA', (favicon_size, favicon_size), (0, 0, 0, 0))
    favicon_draw = ImageDraw.Draw(favicon)
    
    # Draw a small "E" in the accent color
    favicon_draw.rounded_rectangle(
        [2, 2, favicon_size-2, favicon_size-2],
        radius=5,
        fill=accent_color,
        outline=None
    )
    
    # Add "E" shape
    favicon_draw.rectangle([8, 6, favicon_size-8, 10], fill=(255, 255, 255))
    favicon_draw.rectangle([8, 14, favicon_size-12, 18], fill=(255, 255, 255))
    favicon_draw.rectangle([8, 22, favicon_size-8, 26], fill=(255, 255, 255))
    favicon_draw.rectangle([8, 6, 12, 26], fill=(255, 255, 255))
    
    favicon_path = os.path.join(static_dir, 'favicon.ico')
    favicon.save(favicon_path)
    print(f"Favicon saved to {favicon_path}")
    
    return logo_path, navbar_logo_path

if __name__ == "__main__":
    create_beautiful_logo()
