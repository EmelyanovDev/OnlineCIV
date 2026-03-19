from PIL import Image
import numpy as np
import os

input_path = "spritesheet.png"
output_dir = "sprites"

# Диапазон "серого" (можно подправить)
GRAY_MIN = 180
GRAY_MAX = 220
COLOR_TOLERANCE = 10  # насколько R,G,B должны быть близки

os.makedirs(output_dir, exist_ok=True)


def is_gray(pixel):
    r, g, b, a = pixel

    r = int(r)
    g = int(g)
    b = int(b)

    if a == 0:
        return False

    return (
        GRAY_MIN <= r <= GRAY_MAX and
        GRAY_MIN <= g <= GRAY_MAX and
        GRAY_MIN <= b <= GRAY_MAX and
        abs(r - g) < COLOR_TOLERANCE and
        abs(r - b) < COLOR_TOLERANCE
    )

def find_grid_lines(img_array, axis=0, threshold=0.6):
    """
    axis=0 → горизонтальные линии (по строкам)
    axis=1 → вертикальные линии (по столбцам)
    """
    lines = []
    length = img_array.shape[axis]

    for i in range(length):
        if axis == 0:
            line = img_array[i, :, :]
        else:
            line = img_array[:, i, :]

        gray_pixels = sum(is_gray(tuple(px)) for px in line)
        ratio = gray_pixels / len(line)

        if ratio > threshold:
            lines.append(i)

    return lines


def group_lines(lines):
    """Объединяем соседние линии в одну (толстые линии сетки)"""
    groups = []
    current = [lines[0]]

    for i in lines[1:]:
        if i - current[-1] <= 1:
            current.append(i)
        else:
            groups.append(current)
            current = [i]

    groups.append(current)
    return [int(sum(g)/len(g)) for g in groups]


def slice_by_grid():
    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img)

    # Находим линии
    h_lines = find_grid_lines(arr, axis=0)
    v_lines = find_grid_lines(arr, axis=1)

    h_lines = group_lines(h_lines)
    v_lines = group_lines(v_lines)

    print(f"Horizontal lines: {len(h_lines)}")
    print(f"Vertical lines: {len(v_lines)}")

    count = 0

    # Режем по промежуткам между линиями
    for i in range(len(h_lines) - 1):
        for j in range(len(v_lines) - 1):
            top = h_lines[i]
            bottom = h_lines[i + 1]
            left = v_lines[j]
            right = v_lines[j + 1]

            # 🚑 защита от ошибки
            if bottom - top < 10 or right - left < 10:
                continue

            pad = 2
            crop = img.crop((
                left + pad,
                top + pad,
                right - pad,
                bottom - pad
            ))

            crop.save(f"{output_dir}/sprite_{i}_{j}.png")
            count += 1

    print(f"Saved {count} sprites")


if __name__ == "__main__":
    slice_by_grid()