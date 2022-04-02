"""
MIT License
Copyright (c) 2022 Brain-Flooder
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import traceback
import os
import webbrowser
import random
import platform
import json

import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageDraw, ImageChops, ImageStat

THEME = 'default'

if platform.system() == 'Windows':
    THEME = 'vista'

sg.theme('SystemDefault1')

keys_thingy = ['Geometrize', 'Open File', 'Save File','shapes','sides']

menu_def = [
    ['File',['Open &File','&Save File']],
    ['Help',['About','Open an issue','Contact']]
]

disabled_menu_def = [
    ['!File',['!Open &File','!&Save File']],
    ['!Help',['!About','!Open an issue','!Contact']]
]

frame_settings = sg.Frame(
    'Options',
    [
        [sg.Text('Shapes'), sg.Input('1000',size=[10,30],key='shapes')],
        [
            sg.Text('Sides'),
            sg.Spin([x for x in range(3,361)],key='sides',expand_x=True)
        ],
        [sg.Button('Geometrize',key='Geometrize',expand_x=True)],
        [
            sg.Button(
                'Export',
                expand_x=True,
                key='export'
            ),
            sg.Button(
                'Import',
                expand_x=True,
                key='import'
            )
        ]
    ],
    expand_x=True,
    expand_y=True
)

frame_image = sg.Frame(
    'Geometrizer',
    [
        [sg.ProgressBar(
            1000,
            orientation='h',
            size=(20, 20),
            key='progressbar',
            expand_x=True
        )
        ],
        [
            sg.Button(
                'Open file',
                key='Open File',
                expand_x=True
            ),
            sg.Button('Save file', key='Save File', expand_x=True)
        ],
        [sg.Image(key='image',size=[500,500])]
    ],
    expand_x=True,
    expand_y=True
)

layout = [
    [sg.Menu(menu_def,key='menu')],
    [frame_image,frame_settings]
]
window = sg.Window(
    title='Geomethat',
    layout = layout,
    icon='./assets/icon.ico',
    resizable=True,
    use_ttk_buttons=True,
    ttk_theme=THEME
)

to_json={}
image_hehe = Image.Image()
old_image = Image.Image()

while True:
    try:
        event, values = window.read()

        if event == 'About':
            webbrowser.open('https://github.com/Brain-Flooder/Geomethat')

        if event == 'Open an issue':
            webbrowser.open('https://github.com/Brain-Flooder/Geomethat/issues')

        if event == 'Contact':
            webbrowser.open('https://github.com/Brain-Flooder')

        if event == sg.WIN_CLOSED:
            break

        if event == 'Open File':
            file = sg.popup_get_file(
                'Select an image',
                no_window=True,
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
                window['image'].update(
                    data = ImageTk.PhotoImage(img),
                    visible=True,
                    size=[500,500]
                )

        if event == 'Save File':
            file = sg.popup_get_file(
                'Save image as',
                file_types=(
                    ('PNG image','*.png'),
                ),
                no_window=True,
                save_as=True
            )
            if file is None or file == '':
                continue
            try:
                old_image.save(file)
            except ValueError:
                sg.popup_error('Invalid file path.')
                continue
            sg.popup(f'Saved as {file}.png')

        if event == 'import':
            file = sg.popup_get_file(
                'Select an image',
                no_window=True,
                file_types=(
                    ('*JSON File*','*.json*'),
                )
            )

            if file is None or file == '' or not os.path.exists(file):
                continue

            with open(file, encoding='UTF-8') as f:
                json_data = json.loads(f.read())
                new_image = Image.new(
                    mode='RGBA',
                    size=json_data['size'],
                    color=tuple(json_data['color'])
                )
                draw = ImageDraw.Draw(new_image)

                X = 0

                for shape in json_data['shapes']:
                    shape_position_and_thing = tuple(
                        shape['bounding_circle']
                    )

                    draw.regular_polygon(
                        bounding_circle=shape_position_and_thing,
                        fill=tuple(shape['color']),
                        n_sides=json_data['sides']
                    )

                    thumbnail = new_image.copy()
                    thumbnail.thumbnail((500,500))
                    window['image'].update(
                        data = ImageTk.PhotoImage(thumbnail),
                        size=[500,500]
                    )

                    window['progressbar'].update(
                        X+1,
                        len(json_data['shapes']),
                        visible=True
                    )

                    X+=1

            sg.popup('Successfully imported')

        if event == 'export':
            file = sg.popup_get_file(
                'Save image as',
                file_types=(
                    ('JSON files','*.json'),
                ),
                no_window=True,
                save_as=True
            )

            if file is None or file == '':
                continue

            try:
                with open(file,'w',encoding='UTF-8')as f:
                    f.write(json.dumps(to_json))

            except ValueError:
                sg.popup_error('Invalid file path.')
                continue

            sg.popup(f'Saved as {file}.png')

        if event == 'Geometrize':
            for x in keys_thingy:
                window[x].update(disabled = True)

            window['menu'].update(disabled_menu_def)
            image = old_image.copy()
            shapes = int(values['shapes'])
            sides = int(values['sides'])

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

            to_json={
                'color':dominant_color,
                'size':[image.width,image.height],
                'sides':sides
            }

            shapes_export=[]

            for x in range(shapes):

                EXPORT_RADIUS = 3
                BEST_SCORE = 0.0
                RADIUS = 3
                good_image = Image.new(
                    mode='RGBA',
                    size=[image.width,image.height],
                    color=dominant_color
                )

                random_x_pos = random.randint(1,image.width-1)
                random_y_pos = random.randint(1,image.height-1)
                color = image.getpixel((random_x_pos, random_y_pos))

                for y in range(10):
                    test_image = new_image.copy()

                    draw = ImageDraw.Draw(test_image)

                    draw.regular_polygon(
                        bounding_circle=[random_x_pos,random_y_pos,RADIUS],
                        fill=color,
                        n_sides=sides
                    )

                    diff_img = ImageChops.difference(image, test_image)
                    stat = ImageStat.Stat(diff_img)
                    image_accuracy = 100 - (
                        sum(stat.mean) / (len(stat.mean) * 255) * 100
                    )

                    RADIUS+=5

                    if image_accuracy > BEST_SCORE:
                        BEST_SCORE = image_accuracy
                        good_image = test_image
                        EXPORT_RADIUS = RADIUS

                new_image = good_image.copy()
                thumbnail = new_image.copy()
                thumbnail.thumbnail((500,500))
                window['image'].update(
                    data = ImageTk.PhotoImage(thumbnail),
                    size=[500,500]
                )

                window['progressbar'].update(x+1,shapes,visible=True)

                shapes_export.append(
                    {
                        'bounding_circle':(
                            random_x_pos,
                            random_y_pos,
                            EXPORT_RADIUS
                        ),
                        'color':color
                    }
                )

            old_image = new_image.copy()
            thumbnail = new_image.copy()
            thumbnail.thumbnail((500,500))
            window['image'].update(
                data = ImageTk.PhotoImage(thumbnail),
                size=[500,500]
            )

            for x in keys_thingy:
                window[x].update(disabled = False)
            window['menu'].update(disabled_menu_def)
            to_json['shapes'] = shapes_export

            sg.popup('Geometrization completed')

    except Exception:
        sg.popup_scrolled(
            traceback.format_exc(),
            title='A wild error just appeared!'
        )

window.close()
