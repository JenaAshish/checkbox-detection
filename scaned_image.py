# This code is to extract checkbox data from image

import os
import cv2 as cv
import numpy as np
import pytesseract as tess
from boxdetect.pipelines import get_checkboxes
from boxdetect import config

# This line is to connect with tesseract.
# Change the path
tess.pytesseract.tesseract_cmd = r"C:\Users\sharpcoder\AppData\Local\Tesseract-OCR\tesseract.exe"
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)


def box_checker(pix_matrix):
    # This function takes a pixel matrix of box
    # Checks if significant amount of mark present inside the box.
    # Returns True or False
    # Two rows and columns are skipped assuming boundary

    row_check = [any(i) for i in pix_matrix[2:-2, 2:-2]]
    col_check = [any(i) for i in pix_matrix.transpose()[2:-2, 2:-2]]
    row, col = pix_matrix.shape
    pix_row_presence = sum(row_check)/(row - 4)
    pix_col_presence = sum(col_check)/(col - 4)

    return max(pix_col_presence, pix_row_presence) >= 0.8 and min(pix_row_presence, pix_col_presence) >= 0.4


def get_checkbox_data_from_file(path):
    ig = cv.imread(path)
    data = []

    try:
        img_gry = cv.cvtColor(ig, cv.COLOR_BGR2GRAY)  # Gray scaling the image
    except Exception:
        name = path.split("\\")[-1]
        print(f" {name} is not a Image file.")
        return
    height, width = img_gry.shape       # To get the height and width of the image

    # Configuration for get_checkboxes
    cfg = config.PipelinesConfig()
    cfg.width_range = (15, 35)
    cfg.height_range = (15, 40)
    cfg.scaling_factors = [0.7]
    cfg.wh_ratio_range = (0.5, 1.7)

    # Checkboxes will contain data about all checkboxes in the image
    checkboxes = get_checkboxes(img_gry, cfg=cfg)
    print(f"{len(checkboxes)} checkbox found.")         # This will print total no of checkboxes found

    for checkbox in checkboxes:
        # checkbox[2] contains the pixel matrix of the current checkbox
        if box_checker(checkbox[2]):
            x, y, w, h = checkbox[0]
            # Crop out of image 80px in y direction
            # Here +80 is a kind of hard code, assuming 80 px from the top of box contains all data.
            cp = img_gry[y:y + 80, x:x + width]
            # This code will give desired data, but high chance of getting garbage value along with the data.
            text = tess.image_to_string(cp)
            data.append(text)
    if not data:
        print("No checkbox is checked")
    return data


if __name__ == "__main__":
    # Dir location that contains image files
    # Only keep image files.
    ROOT_PATH = r"C:\Users\sharpcoder\PycharmProjects\PDF Reader\New folder"
    count = 0
    for dir_path, subdirList, file_list in os.walk(ROOT_PATH):
        print(f'Found directory: {dir_path}')
        for file_name in file_list:
            count += 1
            print(f'\tHandling {count} - {dir_path}  {file_name}')
            file_path = dir_path + "/" + file_name
            file_data = get_checkbox_data_from_file(file_path)
            print(f"\t{file_name}")
            # All checked checkbox data in current file.
            if file_data:
                print(file_data)
    if count:
        print(f"TOTAL OF {count} files PROCESSED")
    else:
        print("No PDF file found.")
