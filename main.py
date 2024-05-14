import os
import tkinter
from tkinter import colorchooser
import customtkinter  # Custom module for GUI
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageColor

global_image = None  # Global variable for the loaded image
img_watermark = None  # Global variable for the image with applied watermark
open_file_extension = None  # Extension of the loaded file
text_color = ((255, 0, 0), '#ff0000')  # Text color for watermark (RGB value and hex code)
text_transparency = 255  # Transparency of the text for watermark (0 - fully transparent, 255 - fully opaque)
text_size_var = 50  # Initial size of the text for watermark

# Define the appearance switch event function
def appearance_switch_event():
    # Check if the appearance switch is turned on/off and set the appearance mode to "light" or "dark"
    if appearance_var.get() == "on":
        appearance_mode = "light"
        customtkinter.set_appearance_mode("light")
    elif appearance_var.get() == "off":
        appearance_mode = "dark"
        customtkinter.set_appearance_mode("dark")

# Function to set the thumbnail of the image
def setThumbnail(image):
    global tk_resized_img

    width, height = image.size
    ratio = height / width
    if ratio <= 0.84:
        resized_img = image.resize((700, int(700 * ratio)))
    elif ratio > 0.84:
        ratio = width / height
        resized_img = image.resize((int(700 * ratio), 700))

    # Set the image thumbnail
    tk_resized_img = ImageTk.PhotoImage(resized_img)
    show_image_lbl.configure(image=tk_resized_img)

# Function to select a file
def selectFile():
    global global_image, open_file_extension
    try:
        open_file_path = tkinter.filedialog.askopenfilename(initialdir="/images", title="Select Image",
                                                            filetypes=[("JPEG files", "*.jpg;*.jpeg"),
                                                                       ("PNG files", "*.png"),
                                                                       ("BMP files", "*.bmp"),
                                                                       ("TIFF files", "*.tiff;*.tif"),
                                                                       ("GIF files", "*.gif")])
        open_file_extension = os.path.splitext(open_file_path)[1].lower()

        image_url_var.set(open_file_path)
        img = Image.open(image_url_var.get()).convert("RGBA")
        width, height = img.size
        global_image = img

        # Set image thumbnail
        setThumbnail(img)
        addWatermark(image=global_image, text=watermark_text_var.get(), font_size=int(text_size_var.get()),
                     color=text_color[0], transparency=text_transparency,
                     pos_x=slider_x.get(), pos_y=slider_y.get())

        # Activate the state of watermark features
        watermark_text.configure(state="normal")
        text_size_menu.configure(state="normal")
        color_lbl.configure(text=(f'Select Color: {text_color[0]}'))
        select_color_btn.configure(state="normal", fg_color=text_color[1])
        transparency_slider.configure(state="normal")
        transparency_slider.set(text_transparency)
        slider_x.configure(state="normal", to=width)
        slider_x.set(width/2)
        slider_y.configure(state="normal", from_=height, to=0)
        slider_y.set(height/2)
        pos_lbl.configure(text=(f'Watermark position XY axis: ({int(slider_x.get())},{int(slider_y.get())})'))
        save_file_btn.configure(state="normal")


    except:
        print("Operation Error")

# Function to handle text change event
def on_text_changed(*args):
    addWatermark(image=global_image, text=watermark_text_var.get(), font_size=int(text_size_var.get()),
                 color=text_color[0], transparency=text_transparency,
                 pos_x=slider_x.get(), pos_y=slider_y.get())

# Callback function for text size selection
def textSizeCallback(choice):
    addWatermark(image=global_image, text=watermark_text_var.get(), font_size=int(text_size_var.get()), color=text_color[0], transparency=text_transparency,
                 pos_x=slider_x.get(), pos_y=slider_y.get())

# Function to change text color
def changeColor():
    global text_color
    color = colorchooser.askcolor(title="Tkinter Color Chooser")
    if color:
        text_color = color
        addWatermark(image=global_image, text=watermark_text_var.get(), font_size=int(text_size_var.get()),
                     color=text_color[0], transparency=text_transparency,
                     pos_x=slider_x.get(), pos_y=slider_y.get())
        color_lbl.configure(text=(f'Select Color: {text_color[0]}'))
        select_color_btn.configure(fg_color=text_color[1])

# Function to handle transparency slider event
def transparency_slider_event(value):
    global text_transparency
    text_transparency = int(transparency_slider.get())
    transparency_lbl.configure(text=(f'Select Transparency: ({text_transparency})'))

    addWatermark(image=global_image, text=watermark_text_var.get(), font_size=int(text_size_var.get()),
                 color=text_color[0], transparency=text_transparency,
                 pos_x=slider_x.get(), pos_y=slider_y.get())

# Function to add watermark to the image
def addWatermark(image=global_image, text="", font_size=text_size_var, color=text_color[0], transparency=text_transparency, pos_x=None, pos_y=None):
    global img_watermark
    width, height = image.size

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", image.size, (255, 255, 255, 0))

    # get a font
    font = ImageFont.truetype('arial.ttf', font_size)

    # get a drawing context
    draw = ImageDraw.Draw(txt)

    # calculate the x,y coordinates of the text
    _, _, textwidth, textheight = draw.textbbox((0, 0), text=text, font=font)
    margin = 10

    if not pos_x:
        x = width/2 - textwidth/2
    else:
        x=pos_x

    if not pos_y:
        y = height/2 - textheight/2
    else:
        y=pos_y

    # draw text, half opacity
    text_color_RGBA = color + (transparency,)

    draw.text((x, y), text, font=font, fill=text_color_RGBA)

    img_watermark = Image.alpha_composite(image, txt)

    setThumbnail(img_watermark)

# Function to handle slider X axis event
def slider_x_event(value):
    pos_lbl.configure(text=(f'Watermark position XY axis: ({int(slider_x.get())},{int(slider_y.get())})'))
    addWatermark(image=global_image, text=watermark_text_var.get(), font_size=int(text_size_var.get()), color=text_color[0], transparency=text_transparency, pos_x=slider_x.get(), pos_y=slider_y.get())


# Function to handle slider Y axis event
def slider_y_event(value):
    pos_lbl.configure(text=(f'Watermark position XY axis: ({int(slider_x.get())},{int(slider_y.get())})'))
    addWatermark(image=global_image, text=watermark_text_var.get(), font_size=int(text_size_var.get()), color=text_color[0], transparency=text_transparency, pos_x=slider_x.get(), pos_y=slider_y.get())


# Function to save the image with watermark
def saveImage():
    global img_watermark, open_file_extension

    save_file_path = tkinter.filedialog.asksaveasfilename(initialdir="/images", title="Save Image", defaultextension=open_file_extension,
                                                          filetypes=[("Same format as import", "*"+open_file_extension),
                                                                     ("JPEG files", "*.jpg;*.jpeg"),
                                                                     ("PNG files", "*.png"),
                                                                     ("BMP files", "*.bmp"),
                                                                     ("TIFF files", "*.tiff;*.tif"),
                                                                     ("GIF files", "*.gif")])

    saved_file_extension = os.path.splitext(save_file_path)[1].lower()

    if not saved_file_extension in [".png", ".tiff", ".gif", ".tif"]:
        saved_image = img_watermark.convert("RGB")

    else:
        saved_image = img_watermark

    if save_file_path:
        saved_image.save(save_file_path)
        print("Image saved with success at path: ", save_file_path)

# System Settings
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

# App windows
app = customtkinter.CTk()
# app.geometry("1200x720")
app.title("Image Watermarking Desktop")


# Create 3 frames for the app content
first_frame = customtkinter.CTkFrame(app, width=720, height=120, fg_color="transparent", border_color="#FF0000", border_width=0)
first_frame.grid(column=0, row=0, sticky="w n")
second_frame = customtkinter.CTkFrame(app, width=720, height=600, fg_color="transparent", border_color="#FF0000", border_width=0)
second_frame.grid(column=0, row=1, sticky="w n")
third_frame = customtkinter.CTkFrame(app, width=480, height=600, fg_color="transparent", border_color="#7F7F7F", border_width=1)
third_frame.grid(column=1, row=1, sticky="e n")


# Add UI Elements
path_lbl = customtkinter.CTkLabel(first_frame, text="Image URL: ")
path_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# URL path
image_url_var = tkinter.StringVar()
image_path= customtkinter.CTkEntry(first_frame, width=600, height=15, textvariable=image_url_var)
image_path.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Select file button
select_file_btn = customtkinter.CTkButton(first_frame, text="Select image", command=selectFile)
select_file_btn.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Select appearance mode Dark/Light mode
appearance_var = customtkinter.StringVar(value="on")
appearance_switch = customtkinter.CTkSwitch(app, text="Appearance mode (dark/light)", command=appearance_switch_event,
                                 variable=appearance_var, onvalue="on", offvalue="off")
appearance_switch.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Show Image
show_image_lbl = customtkinter.CTkLabel(second_frame, text="")
show_image_lbl.place(x=0, y=0)
show_image_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="n w e")

# Watermark title
watermark_title= customtkinter.CTkLabel(third_frame, text="ADD WATERMARK ", font=('Helvetica',14,'bold'))
watermark_title.grid(row=0, column=0, padx=10, pady=10, sticky="n w")

# Watermark text
text_lbl = customtkinter.CTkLabel(third_frame, text="Text:")
text_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Watermark input text
watermark_text_var = tkinter.StringVar()
watermark_text_var.trace_add("write", on_text_changed)
watermark_text= customtkinter.CTkEntry(third_frame, width=400, height=30, state="disabled", textvariable=watermark_text_var)
watermark_text.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Text size
text_size_lbl = customtkinter.CTkLabel(third_frame, text="Text size:")
text_size_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")

# Text size menu
text_sizes = list(range(8, 73, 2))
text_sizes_str = [str(size) for size in text_sizes]
text_size_var = customtkinter.StringVar(value=text_sizes_str[21])
text_size_menu = customtkinter.CTkOptionMenu(third_frame,values=text_sizes_str,
                                         command=textSizeCallback,
                                         variable=text_size_var,
                                             state="disabled")
text_size_menu.grid(row=4, column=0, padx=10, pady=10, sticky="w")


# Text color
color_lbl = customtkinter.CTkLabel(third_frame, text="Select Color:")
color_lbl.grid(row=5, column=0, padx=10, pady=10, sticky="w")

# Select color button
select_color_btn = customtkinter.CTkButton(third_frame, text="Select color", state="disabled", command=changeColor)
select_color_btn.grid(row=6, column=0, padx=10, pady=10, sticky="w")


# Text transparency
transparency_lbl = customtkinter.CTkLabel(third_frame, text="Select Transparency:")
transparency_lbl.grid(row=7, column=0, padx=10, pady=10, sticky="w")

# Transparency slider
transparency_slider = customtkinter.CTkSlider(third_frame, from_=0, to=255, orientation="horizontal", state="disabled", command=transparency_slider_event)
transparency_slider.grid(row=8, column=0, padx=10, pady=10, sticky="w n")


# Watermark position label
pos_lbl = customtkinter.CTkLabel(third_frame, text="Watermark position XY axis: ")
pos_lbl.grid(row=9, column=0, padx=10, pady=10, sticky="w")

# Slider X
slider_x = customtkinter.CTkSlider(third_frame, from_=0, to=100, orientation="horizontal", state="disabled", command=slider_x_event)
slider_x.grid(row=10, column=0, padx=10, pady=10, sticky="w n")

# Slider Y
slider_y = customtkinter.CTkSlider(third_frame, from_=0, to=100, orientation="vertical", state="disabled", command=slider_y_event)
slider_y.grid(row=10, column=0, padx=10, pady=10, sticky="w s")


# Button to save watermark
save_file_btn = customtkinter.CTkButton(third_frame, text="Save image", state="disabled", command=saveImage)
save_file_btn.grid(row=11, column=0, padx=10, pady=10, sticky="w n")


# Run app
app.mainloop()
