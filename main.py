import cv2
import numpy as np

img_original = cv2.imread('dublin.jpg')
img_with_kevin = cv2.imread('dublin_edited.jpg')

height, width, use = img_original.shape

blue_original = np.zeros((height, width), dtype=np.uint8)
green_original = np.zeros((height, width), dtype=np.uint8)
red_original = np.zeros((height, width), dtype=np.uint8)

blue_modified = np.zeros((height, width), dtype=np.uint8)
green_modified = np.zeros((height, width), dtype=np.uint8)
red_modified = np.zeros((height, width), dtype=np.uint8)
diff_blue = np.zeros((height, width), dtype=np.uint8)
diff_green = np.zeros((height, width), dtype=np.uint8)
diff_red = np.zeros((height, width), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        blue_original[y, x], green_original[y, x], red_original[y, x] = img_original[y, x]
        blue_modified[y, x], green_modified[y, x], red_modified[y, x] = img_with_kevin[y, x]
        diff_blue[y, x] = abs(int(blue_original[y, x]) - int(blue_modified[y, x]))/3
        diff_green[y, x] = abs(int(green_original[y, x]) - int(green_modified[y, x]))/3
        diff_red[y, x] = abs(int(red_original[y, x]) - int(red_modified[y, x]))/3


diff = np.zeros((height, width), dtype=np.uint8)
for y in range(height):
    for x in range(width):
        total_diff = diff_blue[y, x] + diff_green[y, x] + diff_red[y, x]
        diff[y, x] = np.clip(total_diff, 0, 255)


threshold = 11

mask = (diff > threshold)

visited = np.zeros_like(mask, dtype=bool)
bounding_boxes = []

for y in range(height):
    for x in range(width):
        if mask[y, x] and not visited[y, x]:
            visited[y, x] = True

            range_x_left = max(0, x - 50)
            range_x_right = min(width, x + 50)
            range_y_down = min(height, y + 100)

            min_x, max_x, min_y, max_y = width, 0, height, 0
            for ny in range(y, range_y_down):
                for nx in range(range_x_left, range_x_right):
                    if mask[ny, nx]:
                        visited[ny, nx] = True
                        min_x, max_x = min(min_x, nx), max(max_x, nx)
                        min_y, max_y = min(min_y, ny), max(max_y, ny)

            if max_x - min_x > 0 and max_y - min_y > 0:
                bounding_box = (min_x, max_x, min_y, max_y)
                bounding_boxes.append(bounding_box)

for i, (x_min, y_min, x_max, y_max) in enumerate(bounding_boxes):
    print(f"Bounding Box {i+1}: Xmin={x_min}, Xmax={x_max}, Ymin={y_min}, Y_max={y_max}")

box_size = 2

i = 0
while i < len(bounding_boxes):
    frame = bounding_boxes[i]
    left = frame[0]
    right = frame[1]
    top = frame[2]
    bottom = frame[3]

    j = top - box_size
    while j <= bottom + box_size:
        blue_modified[j, left - box_size] = 255
        green_modified[j, left - box_size] = 0
        red_modified[j, left - box_size] = 0
        blue_modified[j, right + box_size] = 255
        green_modified[j, right + box_size] = 0
        red_modified[j, right + box_size] = 0
        j += 1

    j = left - box_size
    while j <= right + box_size:
        blue_modified[top - box_size, j] = 255
        green_modified[top - box_size, j] = 0
        red_modified[top - box_size, j] = 0
        blue_modified[bottom + box_size, j] = 255
        green_modified[bottom + box_size, j] = 0
        red_modified[bottom + box_size, j] = 0
        j += 1

    i += 1

biggest_frame = []
max_area = 0

for frame in bounding_boxes:
    x_min, x_max, y_min, y_max = frame
    area = (x_max - x_min) * (y_max - y_min)
    if area > max_area:
        max_area = area
        biggest_frame = frame


merged_image = np.stack((blue_modified, green_modified, red_modified), axis=-1)

x_min, x_max, y_min, y_max = biggest_frame


diff2 = np.zeros((height, width), dtype=np.uint8)
for y in range(y_min, y_max):
    for x in range(x_min, x_max):
        total_diff = diff_blue[y, x] + diff_green[y, x] + diff_red[y, x]
        diff2[y, x] = np.clip(total_diff, 0, 255)

crop_width = x_max - x_min
crop_height = y_max - y_min

cropped_mask = mask[y_min:y_max, x_min:x_max]

for y in range(cropped_mask.shape[0]):
    left = 0
    right = 0

    for x in range(cropped_mask.shape[1]):
        if cropped_mask[y, x]:
            left = x
            if left == 1:
                left -= 1
            break

    for x in range(cropped_mask.shape[1] - 1, -1, -1):
        if cropped_mask[y, x]:
            right = x
            if right == cropped_mask.shape[1] - 2:
                right += 1
            break

    if left is not None and right is not None:
        for x in range(left, right + 1):
            cropped_mask[y, x] = True

for y in range(1, cropped_mask.shape[0] - 1):
    for x in range(cropped_mask.shape[1]):
        if cropped_mask[y - 1, x] == 1 and cropped_mask[y + 1, x] == 1:
            cropped_mask[y, x] = 1

cropped_image = np.zeros((crop_height, crop_width, 4), dtype=np.uint8)
cropped_image[:, :, :3] = img_with_kevin[y_min:y_max, x_min:x_max, :]
for y in range(cropped_mask.shape[0]):
    for x in range(cropped_mask.shape[1]):
        if cropped_mask[y, x]:
            cropped_image[y, x, 3] = 255
        else:
            cropped_image[y, x, 3] = 0

cv2.imwrite('wyciety_obraz.png', cropped_image)
cropped_mask_display = (cropped_mask.astype(np.uint8) * 255)
cv2.imshow('Wyciety Obraz', cropped_mask_display)
cv2.imwrite('zmodyfikowany_obraz.jpg', merged_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
