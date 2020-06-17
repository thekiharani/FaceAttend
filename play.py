import os
from FaceAttend import settings
image = '/media/joe.py'
name = image.split('/')[2]
print(os.path.join(settings.BASE_DIR, 'media/'+name))