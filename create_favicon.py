from PIL import Image, ImageDraw
import os

def create_favicon():
    # Create a small square image for the favicon
    size = 32
    favicon = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(favicon)
    
    # Colors
    primary_color = (65, 105, 225)  # Royal Blue
    accent_color = (255, 69, 0)     # Red-Orange
    
    # Draw a simple "E" shape
    margin = 4
    
    # Background
    draw.rectangle([(margin, margin), (size-margin, size-margin)], fill=primary_color)
    
    # Draw "E" shape with lines
    line_width = 2
    # Horizontal lines of the E
    draw.rectangle([(margin+2, margin+2), (size-margin-2, margin+5)], fill=accent_color)  # Top
    draw.rectangle([(margin+2, size//2-2), (size-margin-6, size//2+2)], fill=accent_color)  # Middle
    draw.rectangle([(margin+2, size-margin-5), (size-margin-2, size-margin-2)], fill=accent_color)  # Bottom
    
    # Vertical line of the E
    draw.rectangle([(margin+2, margin+2), (margin+5, size-margin-2)], fill=accent_color)
    
    # Save the favicon
    static_dir = os.path.join('static', 'images')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    favicon_path = os.path.join(static_dir, 'favicon.ico')
    favicon.save(favicon_path)
    print(f"Favicon saved to {favicon_path}")
    
    # Also save as PNG
    favicon_png_path = os.path.join(static_dir, 'favicon.png')
    favicon.save(favicon_png_path)
    print(f"Favicon PNG saved to {favicon_png_path}")
    
    return favicon_path

if __name__ == "__main__":
    create_favicon()
