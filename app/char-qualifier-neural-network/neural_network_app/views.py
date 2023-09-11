import base64, json, io, threading
from PIL import Image

from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.db.models import Max

from . import models

from .neural_network.cropper import rework_image_to_network
from .neural_network.network import start_train, get_train_data, process, n, progress



def index(request :HttpRequest):
    return render(request, 'network/index.html')

@csrf_exempt
def upload_image(request :HttpRequest):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        image_data = json_data.get('image_data', None)
        image_char = json_data.get('char', None)

        if image_data and image_char:
            image_bytes = base64.b64decode(image_data)
            stream = io.BytesIO(image_bytes)
            image = Image.open(stream)

            image = rework_image_to_network(image, (72,72))

            stream = io.BytesIO()
            image.save(stream, format='PNG')
            byte_data = stream.getvalue()

            image_file = ContentFile(byte_data)
            
            max_id = models.ImageModel.objects.aggregate(max_id=Max('id'))['max_id']

            image_model = models.ImageModel()
            image_model.image.save(f'image_{max_id}.jpg', image_file)
            image_model.char = image_char
            image_model.save()

            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def train_network(request :HttpRequest):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        train_iter_count = json_data.get('train_iter_count', None)
        if train_iter_count:
            train_iter_count = int(train_iter_count)
            images = models.ImageModel.objects.all()

            images_list = []
            for image_item in images:
                images_list.append({'image': image_item.image.file.name, 'char': image_item.char})
            
            train_data = get_train_data(images_list)

            thread = threading.Thread(target=start_train, args=(n, train_data, train_iter_count))
            thread.start()

            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def train_progress(request :HttpRequest):
    if request.method == 'GET':
        return JsonResponse({'status': 'success', 'progress' : progress[0]})
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def process_image(request :HttpRequest):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        image_data = json_data.get('image_data', None)

        image_bytes = base64.b64decode(image_data)
        stream = io.BytesIO(image_bytes)
        image = Image.open(stream)

        result = process(rework_image_to_network(image, (72,72)))

        return JsonResponse({'status': 'success', 'result' : result})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def verify_train_data(request :HttpRequest):
    if request.method == 'GET':
        alphabet = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "@", "А", "Б",
        "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р",
        "С", "Т", "У", "Ф","Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ы", "Ъ", "Э", "Ю", "Я"]

        images = models.ImageModel.objects.all()
        

        for image in images:
            result = process(Image.open(image.image))
            result = result.split(" ")
            result = [float(item) for item in result]
            max_index = result.index(max(result))
            if alphabet[max_index] != image.char:
                print(image.image, alphabet[max_index], image.char)
                    
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)