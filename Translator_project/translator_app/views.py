from django.shortcuts import render
from googletrans import Translator, LANGUAGES
from django.core.files.storage import FileSystemStorage
import asyncio
from .image_utils import *
import os


def Home(request):
    return render(request, 'Home.html')


LANGUAGES1 = {value.capitalize(): key for key, value in LANGUAGES.items()}

async def Google_T(request):
    translated_text = None
    text = ''
    source_lang = 'auto'
    target_lang = 'en'
    if request.method == 'POST':
        text = request.POST.get('text')
        source_lang = request.POST.get('source_language', 'auto')
        target_lang = request.POST.get('target_language', 'en')
        if 'swap_languages' in request.POST:
            source_lang, target_lang = target_lang, source_lang
        translator = Translator()
        try:
            translation = await asyncio.to_thread(translator.translate, text, src=source_lang, dest=target_lang)
            translated_text = translation.text
        except Exception as e:
            translated_text = f"Error: {str(e)}"
    return render(request, 'text_translate.html', {
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang,
        'translated_text': translated_text,
        'languages': LANGUAGES1
    })


async def ImageTranslation(request):
    uploaded_image_url = None
    translated_image = None
    uploaded_image_text = None
    translated_text = None
    selected_language = 'en'
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        selected_language = request.POST.get('language', 'en')
        if image.name.endswith('.png'):
            fs = FileSystemStorage()
            uploaded_image_path = fs.save(image.name, image)
            uploaded_image_absolute_path = os.path.join(fs.location, uploaded_image_path)
            uploaded_image_url = fs.url(uploaded_image_path)
            uploaded_image_text = await process_image_text(uploaded_image_absolute_path)
            if uploaded_image_text is None:
                print("Error: No text extracted from the image.")
            translated_image = await generate_translated_image(uploaded_image_absolute_path)
            if translated_image is None:
                print("Error: No translated image generated.")
            translator = Translator()
            try:
                translation = await asyncio.to_thread(translator.translate, uploaded_image_text, src='auto', dest=selected_language)
                translated_text = translation.text
            except Exception as e:
                translated_text = f"Error: {str(e)}"
    return render(request, 'image_translate.html', {
        'uploaded_image_url': uploaded_image_url,
        'translated_image': translated_image,
        'uploaded_image_text': uploaded_image_text,
        'translated_text': translated_text,
        'languages': LANGUAGES,
        'selected_language': selected_language,
    })