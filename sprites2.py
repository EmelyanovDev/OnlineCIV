from PIL import Image
import os

INPUT_FOLDER = "sprites"
OUTPUT_FOLDER = "sprites_processed"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def remove_white_and_trim(image_path, output_path, threshold=240):
    img = Image.open(image_path).convert("RGBA")
    pixels = img.getdata()

    new_pixels = []
    for r, g, b, a in pixels:
        # если пиксель почти белый — делаем прозрачным
        if r > threshold and g > threshold and b > threshold:
            new_pixels.append((255, 255, 255, 0))
        else:
            new_pixels.append((r, g, b, a))

    img.putdata(new_pixels)

    # обрезаем прозрачные края
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    img.save(output_path)

# обработка всех файлов
for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        remove_white_and_trim(input_path, output_path)

print("Готово!")