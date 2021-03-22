import os
import time
import tkinter
from datetime import datetime

from PIL import Image
import pyscreenshot
from selenium import webdriver

# Removing fields from Google Maps
remove_from_view = [
    "var element = document.getElementById(\"omnibox-container\");element.remove();",
    "var element = document.getElementById(\"watermark\");element.remove();",
    "var element = document.getElementById(\"vasquette\");element.remove();",
    "var element = document.getElementsByClassName(\"app-viewcard-strip\");element[0].remove();",
    "var element = document.getElementsByClassName(\"scene-footer-container\");element[0].remove();",

]

# Removing labels from Google Maps Satellite View
remove_labels = [
    "var element = document.getElementsByClassName(\"searchbox-hamburger-container\")[0];"
    "element.getElementsByTagName(\"button\")[0].click();",
    "var element = document.getElementsByClassName(\"widget-settings-earth-item\")[0];"
    "element.getElementsByTagName(\"button\")[1].click();",

]


def js_code_execute(driver, js_string: str):
    """Execute the JS code"""
    driver.execute_script(js_string)


def get_screen_resolution() -> tuple:
    """Return tuple of (width, height) of screen resolution in pixels."""
    root = tkinter.Tk()
    root.withdraw()
    return root.winfo_screenwidth(), root.winfo_screenheight()


def calc_latitude_shift(screen_height: int, percent_hidden: float, zoom: int) -> float:
    """Return the amount to shift latitude per row of screenshots."""
    return -0.000002051 * screen_height * (1 - percent_hidden) * (1 / 1.7 ** (zoom - 18))


def calc_longitude_shift(screen_width: int, percent_hidden: float, zoom: int) -> float:
    """Return the amount to shift longitude per column of screenshots."""
    return 0.00000268 * screen_width * (1 - percent_hidden) * (1 / 1.7 ** (zoom - 18))


def screenshot(screen_width: int, screen_height: int,
               offset_left: float, offset_top: float,
               offset_right: float, offset_bottom: float) -> Image:
    """Return a screenshot of only the pure maps area."""
    x1 = offset_left * screen_width
    y1 = offset_top * screen_height
    x2 = (offset_right * -screen_width) + screen_width
    y2 = (offset_bottom * -screen_height) + screen_height
    image = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
    return image


def scale_image(image: Image, scale: float) -> Image:
    """Scale an Image by a proportion, maintaining aspect ratio."""
    width = round(image.width * scale)
    height = round(image.height * scale)
    image.thumbnail((width, height))
    return image


def combine_images(images: list) -> Image:
    """Return combined image from a grid of identically-sized images.
    images is a 2d list of Image objects. The images should
    be already sorted/arranged when provided to this function.
    """
    img_width = images[0][0].width
    img_height = images[0][0].height
    new_size = (img_width * len(images[0]), img_height * len(images))
    new_image = Image.new('RGB', new_size)

    # Add all the images from the grid to the new, blank image
    for rowindex, row in enumerate(images):
        for colindex, image in enumerate(row):
            location = (colindex * img_width, rowindex * img_height)
            new_image.paste(image, location)

    return new_image


def create_map(lat_start: float, long_start: float, zoom: int,
               number_rows: int, number_cols: int,
               scale: float = 1, sleep_time: float = 0,
               offset_left: float = 0, offset_top: float = 0,
               offset_right: float = 0, offset_bottom: float = 0,
               outfile: str = None, number: int = 0):
    """

    Args:
        number: specific number?
        lat_start: Top-left coordinate to start taking screenshots.
        long_start: Top-left coordinate to start taking screenshots.
        number_rows: Number of rows to take screenshot.
        number_cols: Number of columns to to create screenshot.
        scale: Percent to scale each image to reduce final resolution
            and filesize. Should be a float value between 0 and 1.
            Recommend to leave at 1 for production, and between 0.05
            and 0.2 for testing.
        sleep_time: Seconds to sleep between screenshots.
            Needed because Gmaps has some AJAX queries that will make
            the image better a few seconds after confirming page load.
            Recommend 0 for testing, and 3-5 seconds for production.
        offset_*: Percent of each side to crop from screenshots.
            Each should be a float value between 0 and 1. Offsets should
            account for all unwanted screen elements, including:
            taskbars, windows, multiple displays, and Gmaps UI (minimap,
            search box, compass/zoom buttons). Defaults are set for an
            Ubuntu laptop with left-side taskbar, and will need to be
            tuned to the specific machine and setup where it will be run.
        outfile: If provided, the program will save the final image to
            this filepath. Otherwise, it will be saved in the current
            working directory with name 'testing-<timestamp>.png'
        offset_right: Right offset.
        offset_top: Top offset.
        offset_bottom: Bottom offset.
        offset_left: Left offset.
    """

    # DRIVER Selection
    # Chromedriver should be in the current directory.
    # Modify these commands to find proper driver Chrome or Firefox
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    driver = webdriver.Chrome(executable_path=DRIVER_BIN)

    driver.maximize_window()

    # Calculate amount to shift lat/long each screenshot
    screen_width, screen_height = get_screen_resolution()

    # Shifting values for lat and long
    lat_shift = calc_latitude_shift(screen_height, (offset_top + offset_bottom), zoom) - 0.00021
    long_shift = calc_longitude_shift(screen_width, (offset_left + offset_right), zoom) + 0.000595

    # Giving numbers for map and satellite images
    c_map = number
    c_image = number

    # Writing coordinates to the file
    f = open("coordinates.txt", "w+")

    images = [[None for _ in range(number_cols)]
              for _ in range(number_rows)]

    """
    i = 0 -> Map View
    i = 1 -> Satellite View
    """
    for i in range(1, 2):
        for row in range(number_rows):
            for col in range(number_cols):

                latitude = lat_start + (lat_shift * row)
                longitude = long_start + (long_shift * col)

                url = 'https://www.google.com/maps/'

                # Map URL
                if i == 0:
                    url += '@{lat},{long},{z}z'.format(lat=latitude, long=longitude, z=zoom)
                # Satellite URL
                elif i == 1:
                    url += '@{lat},{long},{z}z/data=!3m1!1e3'.format(lat=latitude, long=longitude, z=zoom)

                driver.get(url)
                time.sleep(5)

                # Remove labels from Satellite view
                if i == 1:
                    js_code_execute(driver, remove_labels[0])
                    time.sleep(3)
                    js_code_execute(driver, remove_labels[1])

                # Remove fields from Map view
                for j in remove_from_view:
                    js_code_execute(driver, j)

                # Let the map load all assets before taking a screenshot
                time.sleep(sleep_time)
                image = screenshot(screen_width, screen_height, offset_left, offset_top, offset_right, offset_bottom)

                # Scale image up or down if desired, then save in memory
                image = scale_image(image, scale)
                if i == 0:
                    # image.save(f"{outfile}-map-{row}-{col}.png")  # To save the row-col position uncomment
                    image.save(f"{outfile}-map-{c_map}.png")
                    f.write(f"{outfile}-{c_map}.png -> Lat: {latitude} Long: {longitude} URL: {url} \n")
                    c_map += 1
                else:
                    # image.save(f"{outfile}-{row}-{col}.png") # To save the row-col position uncomment
                    image.save(f"{outfile}-{c_image}.png")
                    images[row][col] = image
                    c_image += 1

    # Close the browser
    driver.close()
    driver.quit()

    # Combine all the images into one, then save it to disk
    final = combine_images(images)
    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    outfile = 'test.png'

    final.save(outfile)

    f.close()
