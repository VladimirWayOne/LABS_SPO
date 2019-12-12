import pandas as pd
import sqlite3
import folium


def color_change(turnout):
    if (turnout < 100):
        return ('#1AFF00')
    elif (100 <= turnout < 200):
        return ('#91FF00')
    elif (200 <= turnout < 300):
        return ('#BCFF00')
    elif (300 <= turnout < 400):
        return ('#FFEF00')
    elif (400 <= turnout < 500):
        return ('#FFA200')
    elif (500 <= turnout < 600):
        return ('#FF8000')
    elif (600 <= turnout < 700):
        return ('#FF4D00')
    elif (700 <= turnout < 800):
        return ('#FA6039')
    else:
        return ('#FF0000')


URL = 'http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217443&type=222'

page = pd.read_html(URL, encoding='CP1251')
header = page[6].drop(12).T
data = page[7].drop(12).T
header[0] = "№ УИК"
data.columns = header.iloc[1]


def popup_html(i, df, data):
    html = '<h5> УИК № {}</h5>'.format(df.iloc[i, 0])
    html += '<br><b> Амосов Михаил Иванович </b>: {} '.format(data.iloc[i, 12].split(' ')[1])
    html += '<br><b> Беглов Александр Дмитриевич </b>: {} '.format(data.iloc[i, 13].split(' ')[1])
    html += '<br><b> Тихонова Надежда Геннадьевна </b>: {} '.format(data.iloc[i, 14].split(' ')[1])
    html += '<br><b> Явка </b>: {} %'.format(float((int(data.iloc[i, 7])+int(data.iloc[i, 6]))/int(data.iloc[0, 1])*100).__format__('2.4'))
    html += '<br><b> Количество проголосовавших</b>: {} '.format(int(data.iloc[i, 7])+int(data.iloc[i, 6]))
    return html


base = sqlite3.connect('coord.db')
readbase = pd.read_sql("SELECT * FROM coordinates", base)

map = folium.Map(location=[59.976040, 30.45],
                  tiles='OpenStreetMap',
                  zoom_start=11.5)


for i in range(0, len(data.iloc[:, 0])):
    folium.Marker(location=[readbase.iloc[i, 1], readbase.iloc[i, 2]],
                  popup=folium.Popup(popup_html(i, readbase, data), max_width=1000, height=250),
                  icon=folium.Icon(icon_color=color_change(int(data.iloc[i, 7])+int(data.iloc[i, 6])), icon='flag',
                                   color='lightgray')).add_to(map)

legend_html =   '''
                <div style="position: fixed; 
                            bottom: 50px; left: 50px; width: 125px; height: 350px; 
                            border:4px solid black; z-index:9999; font-size:14px;
                            background:#FFFFFF;
                            ">&nbsp; Цвет флага зависит от количества проголосовавших <br>
                              &nbsp;100 &nbsp; <i class="fa fa-flag fa-lg" style="color:#1AFF00"></i><br>
                              &nbsp;100-200 &nbsp; <i class="fa fa-flag fa-lg" style="color:#91FF00"></i>
                              &nbsp;200-300 &nbsp; <i class="fa fa-flag fa-lg" style="color:#BCFF00"></i>
                              &nbsp;300-400 &nbsp; <i class="fa fa-flag fa-lg" style="color:#FFEF00"></i>
                              &nbsp;400-500 &nbsp; <i class="fa fa-flag fa-lg" style="color:#FFA200"></i>
                              &nbsp;500-600 &nbsp; <i class="fa fa-flag fa-lg" style="color:#FF8000"></i>
                              &nbsp;600-700 &nbsp; <i class="fa fa-flag fa-lg" style="color:#FF4D00"></i>
                              &nbsp;700-800 &nbsp; <i class="fa fa-flag fa-lg" style="color:#FA6039"></i>
                              &nbsp;800< &nbsp; <i class="fa fa-flag fa-lg" style="color:#FF0000"></i>
                </div>
                '''


map.get_root().html.add_child(folium.Element(legend_html))
map.save('Elections_map.html')
