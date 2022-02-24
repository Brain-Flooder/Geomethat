import os,webbrowser,random
import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageDraw, ImageChops, ImageStat

sg.theme('SystemDefault1')

menu_def = [
    ['File',['Open','Save']],
    ['Help',['About','Open an issue','Contact']]
]

column_settings = sg.Column([
    [sg.Text('Shapes'), sg.Input('1000',size=[10,30],key='shapes')],
    [sg.Text('Sides'), sg.Slider([3,360],key='sides',orientation="h")],
    [sg.Button('Accurate generator',key='accurate'),sg.Button('Fast generator',key='fast')]
])

layout = [
    [sg.Menu(menu_def)],
    [sg.Image(key='image',size=[500,500]),sg.VerticalSeparator(pad=None),column_settings]
]
window = sg.Window(
    title='Geomethat',
    layout = layout,
    icon=r'.\assets\icon.ico',
    resizable=True,
)

image_hehe = Image.Image()
old_image = Image.Image()

while True:
    event, values = window.read()
    if event == 'About':
        webbrowser.open('https://github.com/Brain-Flooder/Geomethat')
    if event == 'Open an issue':
        webbrowser.open('https://github.com/Brain-Flooder/Geomethat/issues')
    if event == 'Contact':
        webbrowser.open('https://github.com/Brain-Flooder')
    if event == sg.WIN_CLOSED:
        break
    if event == 'Open':
        file = sg.popup_get_file(
            'Select an image',
            file_types=(
                ('*JPEG image* *PNG image*','*.jpeg* *.png* *.jpg*'),
            )
        )
        if file is None or file == '' or not os.path.exists(file):
            continue
        with Image.open(file)as img:
            img = img.convert('RGBA')
            old_image = img.copy()
            img.thumbnail((500,500))
            window['image'].update(data = ImageTk.PhotoImage(img),visible=True,size=[500,500])
    if event == 'Save':
        file = sg.popup_get_file(
            'Save image as',
            save_as=True
        )
        old_image.save(file+'.png')
        sg.popup(f'Saved as {file}.png')
    if event == 'accurate':
        image = old_image.copy()
        shapes = int(values['shapes'])
        sides = int(values['sides'])
        if shapes <= 0:
            sg.popup_error('Please resize your attribute(s)')
            continue
        dominant_img = image.copy()
        dominant_img.resize((1,1))
        dominant_color = dominant_img.getpixel((0,0))
        new_image = Image.new(mode='RGBA',size=[image.width,image.height],color=dominant_color)
        for x in range(shapes):
            best_scores = 0.0
            radius = 1
            good_image = Image.new(
                mode='RGBA',
                size=[image.width,image.height],
                color=dominant_color
            )
            for y in range(5):
                test_image = new_image.copy()
                random_x_pos = random.randint(1,image.width-1)
                random_y_pos = random.randint(1,image.height-1)
                color = image.getpixel((random_x_pos, random_y_pos))
                draw = ImageDraw.Draw(test_image)
                draw.regular_polygon(
                    bounding_circle=[random_x_pos,random_y_pos,radius],
                    fill=color,
                    n_sides=sides)
                diff_img = ImageChops.difference(image, test_image)
                stat = ImageStat.Stat(diff_img)
                image_accuracy = 100 - (sum(stat.mean) / (len(stat.mean) * 255) * 100)
                radius+=5
                if image_accuracy > best_scores:
                    best_scores = image_accuracy
                    good_image = test_image
            new_image = good_image
            sg.one_line_progress_meter('Generating...',x+1,shapes)
        old_image = new_image.copy()
        thumbnail = new_image.copy()
        thumbnail.thumbnail((500,500))
        window['image'].update(data = ImageTk.PhotoImage(thumbnail),visible=True,size=[500,500])
    if event == 'fast':
        image = old_image.copy()
        shapes = int(values['shapes'])
        sides = int(values['sides'])
        image.convert('RGBA')
        if shapes <= 0:
            sg.popup_error('Please resize your attribute(s)')
            continue
        dominant_img = image.copy()
        dominant_img.resize((1,1))
        dominant_color = dominant_img.getpixel((0,0))
        new_image = Image.new(
            mode='RGBA',
            size=[image.width,image.height],
            color=dominant_color
        )
        for x in range(shapes):
            test_image = new_image.copy()
            random_x_pos = random.randint(1,image.width-1)
            random_y_pos = random.randint(1,image.height-1)
            color = image.getpixel((random_x_pos, random_y_pos))
            draw = ImageDraw.Draw(test_image)
            draw.regular_polygon(
                bounding_circle=[random_x_pos,random_y_pos,10],
                fill=color,
                n_sides=sides
            )
            new_image = test_image
            sg.one_line_progress_meter('Generating...',x+1,shapes)
        thumbnail = new_image.copy()
        thumbnail.thumbnail((500,500))
        window['image'].update(data = ImageTk.PhotoImage(thumbnail),visible=True,size=[500,500])
        old_image = new_image.copy()

window.close()
