from PIL import Image, ImageEnhance
import logging

def add_watermark(image_path, logo_path, output_path, opacity=0.4):
    logging.debug(f'Adding watermark to {image_path} using logo {logo_path}')
    base_image = Image.open(image_path).convert("RGBA")
    watermark = Image.open(logo_path).convert("RGBA")

    # Calculate the size of the watermark based on a fixed proportion of the base image
    base_width, base_height = base_image.size
    logo_scale = 0.2  # Scale of the logo relative to the smaller dimension of the base image
    watermark_ratio = watermark.width / watermark.height

    # Determine the new size of the watermark while maintaining its aspect ratio
    if base_width < base_height:
        watermark_width = int(base_width * logo_scale)
        watermark_height = int(watermark_width / watermark_ratio)
    else:
        watermark_height = int(base_height * logo_scale)
        watermark_width = int(watermark_height * watermark_ratio)

    watermark = watermark.resize((watermark_width, watermark_height), Image.LANCZOS)
    logging.debug(f'Watermark resized to {watermark_width}x{watermark_height}')

    # Adjust watermark opacity
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    logging.debug(f'Watermark opacity set to {opacity}')

    # Calculate position for watermark to be centered
    position = (
        (base_width - watermark_width) // 2,
        (base_height - watermark_height) // 2
    )
    logging.debug(f'Watermark position set to {position}')

    # Create a new image with the watermark
    transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    logging.debug(f'Watermark applied to the image')

    # Convert back to RGB if needed
    watermarked_image = transparent.convert("RGB")
    watermarked_image.save(output_path, "JPEG")
    logging.debug(f'Watermarked image saved to {output_path}')
