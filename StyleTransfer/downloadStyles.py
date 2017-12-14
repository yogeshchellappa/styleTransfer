import time
import sys
import os
import urllib3
import glob
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from PIL import Image
import urllib.request

NUM_IMAGE_BUFFER = 5


def downloadPage(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(str(e))


def getNextImageItem(page, extension):
    start_line = page.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = page.find('"class="rg_meta"')
        start_content = page.find('"ou"', start_line + 1)
        end_content = page.find(',"ow"', start_content + 1)
        content_raw = str(page[start_content + 6:end_content - 1])
        if extension in content_raw:
            return content_raw, end_content
        else:
            return 'skip', end_content


def getAllImageItems(page, extension, numberOfImages):
    items = []
    while len(items) <= numberOfImages:
        item, end_content = getNextImageItem(page, extension)
        if item == "no_links":
            break
        elif item == 'skip':
            page = page[end_content:]
            continue
        else:
            items.append(item)
            time.sleep(0.1)
            page = page[end_content:]
    return items


def downloadImages(theme, extension, numberOfImages=5, height=300, width=400):
    # Get some buffer images, incase images are corrupted
    numImagesToGet = numberOfImages + NUM_IMAGE_BUFFER
    imagePath = "Images/"
    keywords = ['HD']
    items = []
    print('Theme: ' + str(theme))
    print('Fetching styles .', end='')
    sys.stdout.flush()
    search = theme.replace(' ', '%20')

    j = 0
    while j < len(keywords):
        pure_keyword = keywords[j].replace(' ', '%20')
        url = 'https://www.google.com/search?q=' + search + pure_keyword + '&tbm=isch'
        raw_html = downloadPage(url)
        time.sleep(0.1)
        items = items + (getAllImageItems(raw_html, extension, numImagesToGet))
        j = j + 1

    numOfSavedImages = 0
    index = 0
    while numOfSavedImages < numberOfImages and index < numImagesToGet:
        print(" .", end='')
        sys.stdout.flush()
        http = urllib3.PoolManager()
        req = http.request('GET', items[index], headers={
                           "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
        response = req.data
        imageName = imagePath + "style" + str(numOfSavedImages + 1) + "." + extension
        with open(imageName, 'wb') as file:
            file.write(response)
            file.flush()
            file.close()
            time.sleep(0.5)
        try:
            Image.open(imageName)
            numOfSavedImages += 1
        except:
            print(" ..", end='')
            sys.stdout.flush()
        index += 1

    # exit gracefully in case of error
    if numOfSavedImages < numberOfImages:
        print("\nError: Not able to download required number of style theme images")
        sys.exit(1)

    # Resize images
    for imageName in glob.glob("Images/style*.jpg"):
        if os.path.getsize(imageName) == 0:
            os.remove(imageName)
            continue
        im = Image.open(imageName)
        resizedImage = im.resize((height, width), Image.ANTIALIAS)
        resizedImage.save(imageName, 'JPEG', quality=100)
    print("\nCompleted ====> " + str(numOfSavedImages))
    print('Success')
