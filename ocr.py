import requests, json

api_key = ' ...'

def ocr_space_file(filename, overlay=False, api_key=api_key, language='eng'):
    remov = []
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        try:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename: f},
                              data=payload,
                              )
        except Exception as err:
            print(err)
        else:
            remov.append(filename)
            
    results = json.loads(r.content.decode())
    text = results.get('ParsedResults')[0]['ParsedText'].replace('\n', '').replace('\r', ' ').strip()
    return text

print(result)

#GOOGLE

'''
import os, io, pandas
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'..\serviceAccountToken.json'

client = vision.ImageAnnotatorClient()

img = r'...'

def detectText(img):
    with io.open(img, 'rb') as img_file:
        content = img_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    df = pandas.DataFrame(columns=['locale', 'description'])
    for text in texts:
        df = df.append(
            dict(
                locale=text.locale,
                description=text.description
            ),
            ignore_index=True
        )
    return df

i = detectText(img)
print(i)

'''
