import random
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename, asksaveasfile
from PIL import Image, ImageTk
from tkinter import filedialog

WINDOW_MINSIZE_X = 512
WINDOW_MINSIZE_Y = 512
WINDOW_MAXSIZE_X = 1600
WINDOW_MAXSIZE_Y = 1100

main = Tk()
main.configure(bg='#162123')
main.title("WSU CrimsonCode 2025")
main.geometry(f"{WINDOW_MAXSIZE_X}x{WINDOW_MAXSIZE_Y}")
main.minsize(WINDOW_MINSIZE_X, WINDOW_MINSIZE_Y)
main.maxsize(WINDOW_MAXSIZE_X, WINDOW_MAXSIZE_Y)

blank_image = Image.new("RGBA", (100, 100), (255, 255, 255, 0))  # White with transparency
tk_image = ImageTk.PhotoImage(blank_image)
filename = None

# title label setup
label = Label(main, text="Color By Numbers", font=('Arial', 36), bg='#162123', fg='#e2e9ec', padx=5, pady=5)
label.pack()


# load image setup
def get_image():
    global filename
    filename = askopenfilename()
    if filename:
        global tk_image
        tk_image = ImageTk.PhotoImage(Image.open(filename))
    else:
        print("ERROR: could not open file")


# save image setup
def save_image():
    global tk_image
    if tk_image:
        files = [('All Files', '*.*'),
                 ('PNG Files', '*.png'),
                 ('JPEG Files', '*.jpeg')]
        save_path = filedialog.asksaveasfile(filetypes=files, defaultextension=".jpeg", confirmoverwrite=True)
        print(save_path)
        img = ImageTk.getimage(tk_image)
        img.save(save_path)


# save/load button setup
button_grid = Frame(padx=2, pady=2, bg='#090d0e')
button_grid.pack()

load_image_button = Button(button_grid, text="Upload an image", width=16, height=1)
load_image_button.config(
    bd=0, bg="#a90448", fg="#e2e9ec",
    activebackground="grey", activeforeground="white",
    font=('Arial', 24),
    relief=FLAT, cursor="plus",
    command=get_image
)
load_image_button.grid(row=0, column=0, padx=2, pady=2)
save_image_button = Button(button_grid, text="save image", width=16, height=1)
save_image_button.config(
    bd=0, bg="#a90448", fg="#e2e9ec",
    activebackground="grey", activeforeground="white",
    font=('Arial', 24),
    relief=FLAT, cursor="plus",
    command=save_image
)
save_image_button.grid(row=0, column=1, padx=2, pady=2)

selected_color = None


def select_color(color):
    global selected_color
    selected_color = color


solved_states = {}


def on_rect_click(event, rect, color, text):
    if solved_states[rect]:
        return
    color_grid.itemconfig(rect, fill=selected_color)
    if selected_color == color:
        solved_states[rect] = True
        color_grid.itemconfig(text, text="")


# replace these colors with haddies colors
colors = {
    1: "#0000ff",
    2: "#00ff00",
    3: "#ff0000",
    4: "#ff00ff",
    5: "#00ffff",
    6: "#ffff00"
}
haddies_colors = {}


# get the pixel color from the list
def get_pixel_color(row, col):
    # color = haddies_colors[col + row * height]
    return random.choice(list(colors.items()))


# color grid setup
# need to update these values to be dynamic based on image from haddison
cols = 96
rows = 60
WIDTH = cols * 15
HEIGHT = (int)(WIDTH / (cols / rows))
color_grid = Canvas(main, width=WIDTH, height=HEIGHT, bg='black')
size = int(500 / rows)
standard_size = size
for i in range(1, rows + 1):
    for j in range(1, cols + 1):
        x1, y1, x2, y2 = (
            (((WIDTH / cols) * j) - (WIDTH / cols)),
            (((HEIGHT / rows) * i) - (HEIGHT / rows)),
            ((WIDTH / cols) * j),
            ((HEIGHT / rows) * i)
        )
        rect_id = color_grid.create_rectangle(x1, y1, x2, y2, fill='#a4bac4', outline="")

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        color_pair = get_pixel_color(i, j)
        key = color_pair[0]
        color = color_pair[1]
        solved_states[rect_id] = False
        text_id = color_grid.create_text(
            center_x, center_y,
            text=f"{key}", font=("Arial", size),
            fill="black", state="disabled"
        )
        color_grid.tag_bind(rect_id, "<Button-1>",
                            lambda event, r=rect_id, c=color, t=text_id: on_rect_click(event, r, c, t))

color_grid.pack()

# color picker frame setup
palette_frame = Frame(main)
palette_frame.config(bg='black', height=256, width=512)
for col in range(1, len(colors) + 1):
    button = Button(
        palette_frame,
        width=5, height=1,
        bg=colors[col],
        relief=FLAT,
        anchor=CENTER,
        cursor="spraycan",
        text=f"{col}",
        font=('Arial', 24)
    )
    button.grid(row=0, column=col, padx=2, pady=2)
    button.config(command=lambda c=colors[col]: select_color(c))
palette_frame.pack()

# zoom setup
zoom_level = 100


def zoom(event):
    amount = 0.5 if event.delta < 0 else 1.7
    global zoom_level
    zoom_level += 10 if event.delta < 0 else -10
    global size
    size = int(zoom_level / standard_size)
    print(zoom_level)

    def get_all_text_items(canvas):
        for item in canvas.find_all():
            if canvas.type(item) == "text":
                color_grid.itemconfig(item, font=("Arial", size))

    get_all_text_items(color_grid)

    x = main.winfo_pointerx()
    y = main.winfo_pointery()
    abs_coord_x = main.winfo_pointerx() - main.winfo_vrootx()
    abs_coord_y = main.winfo_pointery() - main.winfo_vrooty()
    color_grid.scale(ALL, abs_coord_x, abs, amount, amount)


color_grid.bind('<MouseWheel>', zoom)

main.mainloop()
