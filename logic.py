from django.core.mail import send_mail

from PIL import Image

from geopy import distance


def watermark_with_transparency(input_image_path,
                                output_image_path,
                                watermark_image_path,
                                position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)
    watermark.thumbnail(base_image.size)
    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.save(output_image_path)


def jpg_to_png(img_url):
    return img_url.replace('.jpg', '.png')


def send_love_message(email, message):
    print("I'm sending...")
    send_mail(
        'Вы понравились кому-то в LikeMe!',
        message,
        'igimadeev2016@litsey2.ru',
        [email],
        fail_silently=False,
    )


def geo_distance(coord1, coord2):
    return distance.geodesic(coord1, coord2).km


def float_normalize(f):
    return f.replace(',', '.')
