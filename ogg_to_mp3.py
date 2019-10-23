from pydub import AudioSegment
import os

DATA_PATH = os.path.join(os.curdir, 'data')

list_of_oggs = [file for file in os.listdir(DATA_PATH) if file.endswith('.ogg')]

export_kw = {'format': 'mp3', 'tags': {'artist': 'Wayi', 'album': 'Elysium'}}

for file in list_of_oggs:
    filename = file.split('.')[0]
    AudioSegment.from_ogg(os.path.join(DATA_PATH, file)).export(os.path.join(DATA_PATH, '{}.mp3'.format(filename)), **export_kw)
    print('{} conversion complete'.format(filename))

print('All conversion complete')
