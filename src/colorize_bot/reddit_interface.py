import praw
import requests
from image_paths import imgPath

# Credentials collected from praw.ini
r = praw.Reddit('colorize_bot')

# Downloads the image from the specified post_id passed as argument from Spark
def download_image(post_id):
    submission = r.submission(id=post_id)
    url = submission.url
    with open('%s/in/%s.jpg' % (imgPath, post_id), 'wb') as f:
        f.write(requests.get(url).content)
    f.close()
    #img = Image.open('%s/in/%s.jpg' % (imgPath, post_id)).convert('L')
    #img.save('%s/in/%s.jpg' % (imgPath, post_id))

# Post a reply to the comment that triggered the bot.
def reply(comment_id, imgur_link):
    comment = r.comment(comment_id)
    reply = "Here is your [colorized image](%s) :^ )  \n(This is a bot colorizing images, using [this](https://richzhang.github.io/colorization/) Deep Learning model)" % imgur_link
    try: 
        c = comment.reply(reply)
    except: 
        print("Failure :(")
        return None
    print("Success! URL: https://www.reddit.com%s" % (c.permalink))
