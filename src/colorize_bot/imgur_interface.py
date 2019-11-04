import pyimgur
from image_paths import imgPath
from imgur_credentials import client_id


# IMGUR-credentials should also be in separate file
imgur = pyimgur.Imgur(client_id)

# Uploads the image to Imgur to be able to link to from reply, returns link
def upload_image(colorized_img_path):
    uploaded_image = imgur.upload_image(colorized_img_path, title="Colorized B&W photo")
    if uploaded_image is None: 
        print('Upload to imgur failed')
        return None
    else:
        return uploaded_image.link
