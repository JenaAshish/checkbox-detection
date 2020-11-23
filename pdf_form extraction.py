# This code is for selectable PDF files
# Not for the scanned PDF

import re
import os
import pdfplumber

# Only find checkboxes this size
# tolerance is to provide range for both height and width
RECT_WIDTH = 9.3
RECT_HEIGHT = 9.3
RECT_TOLERANCE = 2


def filter_rects(rects):
    # Just get the rects that are the right size to be a checkboxes
    rects_found = []
    for rect in rects:
        if (rect['height'] > (RECT_HEIGHT - RECT_TOLERANCE)
                and (rect['height'] < RECT_HEIGHT + RECT_TOLERANCE)
                and (rect['width'] < RECT_WIDTH + RECT_TOLERANCE)
                and (rect['width'] > RECT_WIDTH - RECT_TOLERANCE)):
            rects_found.append(rect)

    return rects_found


def determine_if_checked(checkbox, curve_list, page):
    # This takes list of rects of desired size.
    # Checks if any element is present inside the checkbox
    for curve in curve_list:
        xmatch = False
        ymatch = False

        if max(checkbox['x0'], curve['x0']) <= min(checkbox['x1'], curve['x1']):
            xmatch = True
        if max(checkbox['y0'], curve['y0']) <= min(checkbox['y1'], curve['y1']):
            ymatch = True
        if xmatch and ymatch:
            # If both xmathch and ymatch are true get a croped img
            # From the box position to 30 px down
            cp = page.crop((checkbox['x0'], checkbox['top'], page.width, float(checkbox['bottom'])+30))

            # Extract_text extracts all string character from source
            line = cp.extract_text()
            if '\n' not in line:
                str_re = re.compile(r'(.*)')           # If contains single line text
            else:
                str_re = re.compile(r'([\w\s,/]*?(?= \n ))')     # For multi line data

            data = str_re.search(line).group(1)

            return data


def get_checkbox_data_from_file(file_path):
    file_data = []

    # get a pdfplumber obj for this file.
    this_pdf = pdfplumber.open(file_path)
    for page in this_pdf.pages:
        try:
            curves = page.objects["curve"]          # Gets all line touching multiple points
            rects = page.objects["rect"]            # Gets all rectangles
        except KeyError:
            continue

        rects = filter_rects(rects)
        # for each checkbox we found figure out if it is checked and returns data.
        for rect in rects:
            data = determine_if_checked(rect, curves, page)
            if data and data[0] != 'None':
                file_data.append(data)

    return file_data        # Returns all the extracted data for a single file


if __name__ == "__main__":
    # Dir location that contains pdf files
    ROOT_PATH = r"D:\test\nf"
    count = 0
    for dir_path, subdirList, file_list in os.walk(ROOT_PATH):
        print(f'Found directory: {dir_path}')
        for file_name in file_list:

            if file_name.endswith('.pdf'):
                count += 1

                print(f'\tHandling {count} - {dir_path}  {file_name}')
                file_path = dir_path + "/" + file_name

                file_data = get_checkbox_data_from_file(file_path)
                print(f"\t{file_name}")
                # All checked checkbox data in current file.
                print(f'{file_data}')
    if count:
        print(f"TOTAL OF {count} files PROCESSED")
    else:
        print("No PDF file found.")
