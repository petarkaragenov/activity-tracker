import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import time
import os
from win32api import GetSystemMetrics
from colors import bar_colors


plt.style.use("seaborn")
plt.rc('xtick',labelsize=8, color="white")
plt.rc('ytick',labelsize=8, color="white")

sg.ChangeLookAndFeel('Black')

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
today = datetime.now().strftime("%Y-%m-%d")

bar_colors.reverse()


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def clear_old():
    current = f'activity_{datetime.now().strftime("%Y-%m-%d")}.csv'
    for name in os.listdir():
        if name.endswith(".csv") and name != current:
            os.remove(name)

def Button(text, bg):
    return sg.Button(text, expand_x=True, button_color=('white', bg))


layout = [[sg.Text('App Usage', expand_x=True, justification="center", font=('Verdana', 12), key='-TEXT-')],
          [sg.Canvas(key='-CANVAS-', pad=((0, 0), (0, 10)))],
          [Button("Close", "#008ecc"), Button("Clear", "#f38b00")]]


window = sg.Window('Running Timer', layout, finalize=True, no_titlebar=True, auto_size_buttons=False, keep_on_top=True,
                   grab_anywhere=True, alpha_channel=0.7, location=(width-260, height-290))

window.bind('<Enter>', '-MENTER-')
window.bind('<Leave>', '-MLEAVE-')
window["Close"].set_cursor("hand2")
window["Clear"].set_cursor("hand2")

fig = plt.figure(figsize=(2.2, 1.6), facecolor="black")
ax = fig.add_subplot(111)
plt.subplots_adjust(bottom=0.19, left=0.32)
fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)


while True:
    activity = []
    try:
        with open(f"activity_{today}.csv", "r", newline='') as file:
            for row in file:
                row = row.strip()
                activity.append(row.split(","))
    except FileNotFoundError:
        break

    try:
        activity[1] = [int(val) for val in activity[1]]
        activity_dict = dict(zip(activity[0], activity[1]))
        activity_sorted = {key: val for key, val in sorted(activity_dict.items(), key=lambda x: x[1])}

    except IndexError:
        pass
    else:
        headings = list(activity_sorted.keys())
        vals = list(activity_sorted.values())

        ax.barh(headings, vals, color=bar_colors[:len(headings)])
        fig_agg.draw()
    
    event, values = window.read(timeout=0)

    if event == sg.WIN_CLOSED or event == 'Close':
        break

    elif event == '-MENTER-':
        window.set_alpha(1)
        window.set_cursor("fleur")

    elif event == '-MLEAVE-':
        window.set_alpha(0.7)

    elif event == "Clear":
        clear_old()
    
    time.sleep(0.5)
    window.refresh()


window.close()