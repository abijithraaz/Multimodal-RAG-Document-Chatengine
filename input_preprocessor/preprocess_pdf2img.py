import os


from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image

# Convert the PDF into images (one image per page)
def pdf_to_png(pdf_path, dpi=300):
    # Convert PDF to list of PIL images (one image per page)
    pages = convert_from_bytes(pdf_path, poppler_path = r"poppler-0.89.0\bin", dpi=dpi) # replace your poplerpath
    # pages = convert_from_path(r'C:\Users\BEST\Downloads\wordpress-pdf-invoice-plugin-sample.pdf', poppler_path = r"D:\My_Data\aims\release\poppler-0.89.0\bin", dpi=dpi)

    return pages

# Combine all PNGs into a single image
def combine_images_vertically(images, img_count=5):
    # Calculate total width and height for the combined image
    total_width = max(image.width for image in images)
    total_height = sum(image.height for image in images)

    # Create a new blank image with the combined size
    combined_image = Image.new('RGB', (total_width, total_height))

    # Paste each image on the new blank image
    y_offset = 0
    # Consider first 5 images
    if len(images) > img_count:
        images = images[:img_count]

    for image in images:
        combined_image.paste(image, (0, y_offset))
        y_offset += image.height

    return combined_image

# Save the final combined image
def save_combined_image(combined_image, output_path):
    combined_image.save(output_path, 'PNG')

# Main function to handle the conversion
def pdf_to_single_png(pdf_path, output_path='', dpi=300):
    # Step 1: Convert PDF pages to images
    images = pdf_to_png(pdf_path, dpi=dpi)

    # Step 2: Combine images vertically
    combined_image = combine_images_vertically(images)
    return combined_image