# Image Difference Highlighter

## Description

This Python script compares two images to detect changes and highlights these differences. It's particularly useful for identifying modifications or anomalies when comparing an original image to a modified one. The script uses OpenCV and NumPy libraries for image processing and manipulation.

## Features

- Detects differences between two images.
- Highlights differences with bounding boxes.
- Extracts the most significant changed area into a separate image.
- Visualizes the area of change directly on the modified image.

## How It Works

### Difference Detection
- Separates the images into their respective color channels.
- Calculates the absolute difference between the corresponding color channels of the two images.

```python
for y in range(height):
    for x in range(width):
        total_diff = diff_blue[y, x] + diff_green[y, x] + diff_red[y, x]
        diff[y, x] = np.clip(total_diff, 0, 255)
```
### Highlighting Differences
- Combines the differences from all color channels and applies a threshold to identify significant changes.
- Marks these significant changes by drawing bounding boxes around them.

```python
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
```
![modified](zmodyfikowany_obraz.jpg)

### Extracting the Main Change Area
- Identifies the largest bounding box as the main area of change.
- Extracts this area and saves it as a separate image with transparency for unchanged parts.

```python
cropped_image[:, :, :3] = img_with_kevin[y_min:y_max, x_min:x_max, :]
```
![kevin](wyciety_obraz.png)

### Conclusion
This script showcases a practical approach to detecting and visualizing changes between two images. It can be adapted for various applications, such as detecting modifications in surveillance footage, verifying document authenticity, or even in version control for graphical assets.

