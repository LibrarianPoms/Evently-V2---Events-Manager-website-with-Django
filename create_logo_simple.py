from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_logo():
    # Create a new image with white background
    width, height = 400, 100
    logo = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(logo)
    
    # Colors
    primary_color = (65, 105, 225)  # Royal Blue
    accent_color = (255, 69, 0)     # Red-Orange
    
    # Draw a simple text logo
    try:
        # Use default font
        font = ImageFont.load_default()
        font_size = 48
    except:
        font = None
        font_size = 48
    
    # Draw the main text "Evently"
    text = "Evently"
    text_width = 200  # Approximate width
    text_height = 50  # Approximate height
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    # Draw text
    draw.text(position, text, fill=primary_color, font=font)
    
    # Draw a small accent line
    line_y = position[1] + text_height + 5
    draw.line([(width//4, line_y), (width*3//4, line_y)], fill=accent_color, width=3)
    
    # Save the logo
    static_dir = os.path.join('static', 'images')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    logo_path = os.path.join(static_dir, 'evently_logo.png')
    logo.save(logo_path)
    print(f"Logo saved to {logo_path}")
    
    # Create a smaller version for the navbar
    navbar_logo = logo.copy()
    navbar_logo_path = os.path.join(static_dir, 'evently_logo_small.png')
    navbar_logo.save(navbar_logo_path)
    print(f"Navbar logo saved to {navbar_logo_path}")
    
    return logo_path, navbar_logo_path

if __name__ == "__main__":
    create_simple_logo()
