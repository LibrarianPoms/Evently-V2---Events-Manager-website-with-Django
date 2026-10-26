from django.http import HttpResponse
from django.conf import settings
import os
import random
import math
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import base64
from django.core.cache import cache
import hashlib
import colorsys
import datetime

class ImageGenerator:
    """A class to generate sophisticated AI-like images"""
    
    @staticmethod
    def generate_color_palette(base_hue=None, scheme='complementary'):
        """Generate a harmonious color palette"""
        if base_hue is None:
            base_hue = random.random()  # Random hue between 0 and 1
        
        # Create different color schemes
        if scheme == 'complementary':
            hues = [base_hue, (base_hue + 0.5) % 1.0]
        elif scheme == 'triadic':
            hues = [base_hue, (base_hue + 0.33) % 1.0, (base_hue + 0.66) % 1.0]
        elif scheme == 'analogous':
            hues = [base_hue, (base_hue + 0.1) % 1.0, (base_hue - 0.1) % 1.0]
        elif scheme == 'monochromatic':
            hues = [base_hue] * 3
        else:  # Default to complementary
            hues = [base_hue, (base_hue + 0.5) % 1.0]
        
        # Generate RGB colors with varying saturation and value
        colors = []
        for hue in hues:
            saturation = random.uniform(0.6, 0.9)
            value = random.uniform(0.7, 0.9)
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            colors.append((int(r * 255), int(g * 255), int(b * 255)))
        
        # Add some neutral colors
        neutral = random.randint(220, 255)
        colors.append((neutral, neutral, neutral))  # Light neutral
        dark = random.randint(20, 60)
        colors.append((dark, dark, dark))  # Dark neutral
        
        return colors
    
    @staticmethod
    def generate_gradient_background(width, height, colors, direction='radial'):
        """Generate a gradient background"""
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        if direction == 'radial':
            # Create a radial gradient
            center_x, center_y = width // 2, height // 2
            max_radius = math.sqrt(width**2 + height**2) / 2
            
            for y in range(height):
                for x in range(width):
                    # Calculate distance from center
                    distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = distance / max_radius
                    
                    # Interpolate between colors
                    if ratio >= 1:
                        pixel = colors[1]
                    else:
                        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
                        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                        pixel = (r, g, b)
                    
                    image.putpixel((x, y), pixel)
        
        elif direction == 'linear':
            # Create a linear gradient
            for y in range(height):
                ratio = y / height
                r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                for x in range(width):
                    image.putpixel((x, y), (r, g, b))
        
        elif direction == 'diagonal':
            # Create a diagonal gradient
            for y in range(height):
                for x in range(width):
                    ratio = (x + y) / (width + height)
                    r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                    g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
                    b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                    image.putpixel((x, y), (r, g, b))
        
        return image
    
    @staticmethod
    def add_noise(image, intensity=0.1):
        """Add noise to an image"""
        pixels = image.load()
        width, height = image.size
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                noise = random.uniform(-intensity * 255, intensity * 255)
                pixels[x, y] = (
                    max(0, min(255, int(r + noise))),
                    max(0, min(255, int(g + noise))),
                    max(0, min(255, int(b + noise)))
                )
        
        return image
    
    @staticmethod
    def add_texture(image, texture_type='noise', opacity=0.2):
        """Add texture to an image"""
        width, height = image.size
        
        if texture_type == 'noise':
            # Create noise texture
            texture = Image.new('RGB', (width, height), color=(0, 0, 0))
            for y in range(height):
                for x in range(width):
                    noise = random.randint(0, 255)
                    texture.putpixel((x, y), (noise, noise, noise))
        
        elif texture_type == 'dots':
            # Create dots texture
            texture = Image.new('RGB', (width, height), color=(255, 255, 255))
            draw = ImageDraw.Draw(texture)
            dot_size = max(width, height) // 100
            for _ in range(width * height // 500):
                x = random.randint(0, width)
                y = random.randint(0, height)
                color = (random.randint(200, 255),) * 3
                draw.ellipse((x, y, x + dot_size, y + dot_size), fill=color)
        
        elif texture_type == 'lines':
            # Create lines texture
            texture = Image.new('RGB', (width, height), color=(255, 255, 255))
            draw = ImageDraw.Draw(texture)
            for _ in range(50):
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                x2 = random.randint(0, width)
                y2 = random.randint(0, height)
                color = (random.randint(200, 255),) * 3
                draw.line((x1, y1, x2, y2), fill=color, width=1)
        
        # Convert texture to grayscale and set as alpha channel
        texture = texture.convert('L')
        texture = ImageEnhance.Contrast(texture).enhance(1.5)
        
        # Create a new image with the original as base
        result = image.copy()
        pixels = result.load()
        texture_pixels = texture.load()
        
        # Blend the texture with the original image
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                t = texture_pixels[x, y] / 255.0 * opacity
                pixels[x, y] = (
                    int(r * (1 - t) + 255 * t),
                    int(g * (1 - t) + 255 * t),
                    int(b * (1 - t) + 255 * t)
                )
        
        return result
    
    @staticmethod
    def add_shapes(image, shape_type='geometric', count=20, color=None):
        """Add shapes to an image"""
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        if color is None:
            # Use a contrasting color
            avg_color = ImageGenerator.get_average_color(image)
            brightness = (avg_color[0] + avg_color[1] + avg_color[2]) / 3
            if brightness > 128:
                color = (0, 0, 0, 100)  # Semi-transparent black
            else:
                color = (255, 255, 255, 100)  # Semi-transparent white
        
        if shape_type == 'geometric':
            for _ in range(count):
                shape = random.choice(['circle', 'rectangle', 'triangle'])
                size = random.randint(width // 20, width // 5)
                x = random.randint(0, width - size)
                y = random.randint(0, height - size)
                
                if shape == 'circle':
                    draw.ellipse((x, y, x + size, y + size), fill=color)
                elif shape == 'rectangle':
                    draw.rectangle((x, y, x + size, y + size), fill=color)
                elif shape == 'triangle':
                    draw.polygon([
                        (x + size // 2, y),
                        (x, y + size),
                        (x + size, y + size)
                    ], fill=color)
        
        elif shape_type == 'abstract':
            for _ in range(count):
                # Create abstract blob shapes
                points = []
                center_x = random.randint(width // 4, width * 3 // 4)
                center_y = random.randint(height // 4, height * 3 // 4)
                radius = random.randint(width // 20, width // 8)
                num_points = random.randint(5, 12)
                
                for i in range(num_points):
                    angle = math.pi * 2 * i / num_points
                    distance = radius * random.uniform(0.5, 1.5)
                    x = center_x + math.cos(angle) * distance
                    y = center_y + math.sin(angle) * distance
                    points.append((x, y))
                
                draw.polygon(points, fill=color)
        
        return image
    
    @staticmethod
    def get_average_color(image):
        """Get the average color of an image"""
        pixels = image.load()
        width, height = image.size
        r_total, g_total, b_total = 0, 0, 0
        count = 0
        
        # Sample pixels to get average color
        for y in range(0, height, 10):
            for x in range(0, width, 10):
                r, g, b = pixels[x, y]
                r_total += r
                g_total += g
                b_total += b
                count += 1
        
        return (r_total // count, g_total // count, b_total // count)
    
    @staticmethod
    def add_text_with_effects(image, text, position=None, font_size=None, color=None):
        """Add text with effects to an image"""
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Determine font size based on image dimensions
        if font_size is None:
            font_size = min(width, height) // 15
        
        # Try to load a font, or use default
        try:
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'OpenSans-Bold.ttf')
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, size=font_size)
            else:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        # Determine text color based on background
        if color is None:
            avg_color = ImageGenerator.get_average_color(image)
            brightness = (avg_color[0] + avg_color[1] + avg_color[2]) / 3
            if brightness > 128:
                color = (0, 0, 0)  # Black text on light background
            else:
                color = (255, 255, 255)  # White text on dark background
        
        # Calculate text size
        try:
            text_width, text_height = draw.textsize(text, font=font)
        except:
            # Fallback for newer Pillow versions
            text_width, text_height = font.getsize(text)
        
        # Determine position
        if position is None:
            position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Add shadow effect
        shadow_color = (0, 0, 0, 128)  # Semi-transparent black
        shadow_offset = max(1, font_size // 20)
        draw.text((position[0] + shadow_offset, position[1] + shadow_offset), text, font=font, fill=shadow_color)
        
        # Draw the main text
        draw.text(position, text, font=font, fill=color)
        
        return image
    
    @staticmethod
    def generate_placeholder(width=800, height=600, category=None, text=None):
        """Generate a sophisticated placeholder image with text"""
        # Determine text if not provided
        if category and not text:
            text = f"{category.title()} Event"
        elif not text:
            text = "Evently"
        
        # Generate color palette based on category
        if category:
            # Use consistent colors for specific categories
            category_hues = {
                'conference': 0.6,  # Blue
                'workshop': 0.1,   # Orange
                'meetup': 0.3,     # Green
                'seminar': 0.8,    # Purple
                'banner': 0.5,     # Cyan
                'gallery': 0.9,    # Pink
                'testimonial': 0.7, # Blue-purple
                'featured': 0.2,   # Yellow-orange
            }
            base_hue = category_hues.get(category.lower(), random.random())
            scheme = 'complementary'
        else:
            base_hue = random.random()
            scheme = random.choice(['complementary', 'triadic', 'analogous'])
        
        colors = ImageGenerator.generate_color_palette(base_hue, scheme)
        
        # Choose gradient direction based on image dimensions and type
        if width > height * 1.5:
            direction = 'linear'  # Horizontal image
        elif height > width * 1.5:
            direction = 'diagonal'  # Vertical image
        else:
            direction = 'radial'  # Square-ish image
        
        # Generate base image with gradient
        image = ImageGenerator.generate_gradient_background(width, height, colors[:2], direction)
        
        # Add texture based on category
        if category:
            if category.lower() in ['conference', 'seminar']:
                texture_type = 'lines'
            elif category.lower() in ['workshop', 'meetup']:
                texture_type = 'dots'
            else:
                texture_type = 'noise'
        else:
            texture_type = random.choice(['noise', 'dots', 'lines'])
        
        image = ImageGenerator.add_texture(image, texture_type, opacity=0.1)
        
        # Add shapes based on category
        if category:
            if category.lower() in ['gallery', 'featured']:
                shape_type = 'abstract'
            else:
                shape_type = 'geometric'
            
            shape_count = width * height // 40000  # Scale with image size
            image = ImageGenerator.add_shapes(image, shape_type, shape_count, color=(*colors[2], 100))
        
        # Add text with effects
        image = ImageGenerator.add_text_with_effects(image, text)
        
        # Apply final touches
        image = image.filter(ImageFilter.SMOOTH)
        
        # Return the image
        img_io = BytesIO()
        image.save(img_io, 'JPEG', quality=85)
        img_io.seek(0)
        return img_io

    @staticmethod
    def generate_profile_image(text=None, width=200, height=200):
        """Generate a profile/avatar image with initials"""
        # Generate a consistent color based on the text
        if text:
            # Use text to generate a consistent hue
            text_hash = sum(ord(c) for c in text)
            hue = (text_hash % 100) / 100.0
            colors = ImageGenerator.generate_color_palette(hue, 'monochromatic')
            
            # Get initials from text (up to 2 characters)
            initials = ''.join([word[0].upper() for word in text.split()[:2]])
            if not initials and text:
                initials = text[0].upper()
        else:
            colors = ImageGenerator.generate_color_palette(None, 'monochromatic')
            initials = "?"
        
        # Create circular avatar
        image = Image.new('RGB', (width, height), color=colors[0])
        draw = ImageDraw.Draw(image)
        
        # Draw circle
        padding = width // 20
        draw.ellipse((padding, padding, width - padding, height - padding), fill=colors[1])
        
        # Add text
        font_size = width // 3
        try:
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'OpenSans-Bold.ttf')
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, size=font_size)
            else:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        # Calculate text position to center it
        try:
            text_width, text_height = draw.textsize(initials, font=font)
        except:
            # Fallback for newer Pillow versions
            text_width, text_height = font.getsize(initials)
            
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Draw text
        draw.text(position, initials, fill=(255, 255, 255), font=font)
        
        # Apply some effects
        image = image.filter(ImageFilter.SMOOTH)
        
        # Return the image
        img_io = BytesIO()
        image.save(img_io, 'PNG', quality=95)
        img_io.seek(0)
        return img_io
    
    @staticmethod
    def generate_event_image(category, text=None, width=800, height=600):
        """Generate a sophisticated event image"""
        # Use category-specific settings
        return ImageGenerator.generate_placeholder(width, height, category, text)
    
    @staticmethod
    def generate_banner_image(text=None, width=1200, height=400):
        """Generate a banner image"""
        # Create a wide banner with special formatting
        if not text:
            text = "Evently - Event Management Platform"
            
        # Use a specific color scheme for banners
        colors = ImageGenerator.generate_color_palette(0.5, 'complementary')  # Cyan-ish base
        
        # Create gradient background (horizontal for banners)
        image = ImageGenerator.generate_gradient_background(width, height, colors[:2], 'linear')
        
        # Add texture and shapes
        image = ImageGenerator.add_texture(image, 'lines', opacity=0.1)
        image = ImageGenerator.add_shapes(image, 'abstract', count=width//100, color=(*colors[2], 80))
        
        # Add text with larger font
        font_size = height // 8
        position = (width // 20, height // 2 - font_size // 2)
        image = ImageGenerator.add_text_with_effects(image, text, position, font_size)
        
        # Apply final touches
        image = image.filter(ImageFilter.SMOOTH)
        
        # Return the image
        img_io = BytesIO()
        image.save(img_io, 'JPEG', quality=90)
        img_io.seek(0)
        return img_io
    
    @staticmethod
    def generate_gallery_image(text=None, width=400, height=300):
        """Generate a gallery image"""
        return ImageGenerator.generate_placeholder(width, height, 'gallery', text)
    
    @staticmethod
    def get_image(image_type, width=800, height=600, category=None, text=None):
        """Get an image based on the requested type"""
        # Select the appropriate image generator based on type
        if image_type == 'profile' or image_type == 'testimonial':
            return ImageGenerator.generate_profile_image(text, width, height)
        elif image_type == 'banner':
            return ImageGenerator.generate_banner_image(text, width, height)
        elif image_type == 'gallery':
            return ImageGenerator.generate_gallery_image(text, width, height)
        elif image_type == 'event':
            return ImageGenerator.generate_event_image(category or 'conference', text, width, height)
        elif image_type == 'featured':
            return ImageGenerator.generate_event_image('featured', text, width, height)
        else:
            # Default to placeholder
            return ImageGenerator.generate_placeholder(width, height, category, text)


def serve_generated_image(request):
    """View to serve generated images"""
    # Get parameters from request
    image_type = request.GET.get('type', 'event')
    width = int(request.GET.get('width', 800))
    height = int(request.GET.get('height', 600))
    category = request.GET.get('category', None)
    text = request.GET.get('text', None)
    
    # Generate a cache key based on the parameters
    cache_key = f"img_{image_type}_{width}_{height}_{category}_{text}"
    cache_key = hashlib.md5(cache_key.encode()).hexdigest()
    
    # Check if the image is in cache
    cached_image = cache.get(cache_key)
    if cached_image:
        return HttpResponse(cached_image, content_type='image/jpeg')
    
    # Generate the image
    img_io = ImageGenerator.get_image(image_type, width, height, category, text)
    
    # Cache the image for future requests (1 hour)
    cache.set(cache_key, img_io.getvalue(), 3600)
    
    # Return the image
    return HttpResponse(img_io.getvalue(), content_type='image/jpeg')
