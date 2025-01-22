import pytesseract
from PIL import Image, ImageDraw, ImageFont
from googletrans import Translator
from io import BytesIO
import asyncio
from django.core.files.storage import FileSystemStorage

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # For Windows

async def generate_translated_image(image_path):
    try:
        image = Image.open(image_path)
        extract_text = pytesseract.image_to_string(image)
        if not extract_text:
            return None
        translator = Translator()
        translation = await asyncio.to_thread(translator.translate, extract_text, src='auto', dest='en')
        translated_text = translation.text
        new_image = Image.new('RGB', image.size, color=(255, 255, 255))
        new_image.paste(image)
        draw = ImageDraw.Draw(new_image)
        font = ImageFont.load_default()
        draw.text((10, 10), translated_text, font=font, fill=(0, 0, 0))
        img_byte_arr = BytesIO()
        new_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        fs = FileSystemStorage()
        translated_image_path = fs.save('translated_image.png', img_byte_arr)
        return fs.url(translated_image_path)
    except Exception as e:
        print(f"Error in generating translated image: {str(e)}")
        return None


async def process_image_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        if not text:
            return "No text extracted from image."
        return text
    except Exception as e:
        print(f"Error in processing image text: {str(e)}")
        return None
