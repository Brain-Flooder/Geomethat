import random
from PIL import Image, ImageDraw, ImageChops, ImageStat

def geometrize_accurate(image:Image, shapes:int = 5000, sides:int = 3):
    """

    """
    image.convert('RGBA')
    if shapes <= 0 or sides < 3:
        raise ValueError('Please resize your attribute(s)')
    dominant_img = image.copy()
    dominant_img.resize((1,1))
    dominant_color = dominant_img.getpixel((0,0))
    new_image = Image.new(
        mode='RGBA',
        size=[image.width,image.height],
        color=dominant_color
    )
    for _ in range(shapes):
        best_scores = 0.0
        radius = 1
        good_image = Image.new(mode='RGBA',size=[image.width,image.height],color=dominant_color)
        for _ in range(5):
            test_image = new_image.copy()
            random_x_pos = random.randint(1,image.width-1)
            random_y_pos = random.randint(1,image.height-1)
            color = image.getpixel(
                (random_x_pos, random_y_pos)
            )
            draw = ImageDraw.Draw(test_image)
            draw.regular_polygon(
                bounding_circle=[random_x_pos,random_y_pos,radius],
                fill=color,
                n_sides=sides
            )
            diff_img = ImageChops.difference(image, test_image)
            stat = ImageStat.Stat(diff_img)
            image_accuracy = 100 - (sum(stat.mean) / (len(stat.mean) * 255) * 100)
            radius+=5
            if image_accuracy > best_scores:
                best_scores = image_accuracy
                good_image = test_image
        new_image = good_image
    return new_image

def geometrize_fast(image:Image, shapes:int = 15000, sides:int = 3):
    """

    """
    image.convert('RGBA')
    if shapes <= 0 or sides < 3:
        raise ValueError('Please resize your attribute(s)')
    dominant_img = image.copy()
    dominant_img.resize((1,1))
    dominant_color = dominant_img.getpixel((0,0))
    new_image = Image.new(
        mode='RGBA',
        size=[image.width,image.height],
        color=dominant_color)
    for _ in range(shapes):
        radius = 10
        test_image = new_image.copy()
        random_x_pos = random.randint(1,image.width-1)
        random_y_pos = random.randint(1,image.height-1)
        color = image.getpixel((random_x_pos, random_y_pos))
        draw = ImageDraw.Draw(test_image)
        draw.regular_polygon(
            bounding_circle=[random_x_pos,random_y_pos,radius],
            fill=color,
            n_sides=sides
        )
        new_image = test_image
    return new_image
