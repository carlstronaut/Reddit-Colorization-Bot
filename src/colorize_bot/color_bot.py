#!/usr/bin/env python
import os
import sys
import argparse
import cassandra_interface as db
import reddit_interface as reddit
import imgur_interface as imgur
import color_model as net
from image_paths import imgPath

# TODO:
#1) Make it possible to see uploads on imgur
#2) Throw exception if bot is triggered on a non-image post 
#3) If some API-call fails, try to redo it a set amount of times
#   before giving up. Or redo after set amount of time.
#4) Split up functions into seperate modules, and use this solely as a driver.

# Creating flags for driver program, possible to type python <module_name> -h
# for module docs
def parse_args():
    parser = argparse.ArgumentParser(description='Driver program for reddt colorization bot')
    parser.add_argument('-comment_id',dest='comment_id',
            help='Unique ID for comment, needed for upload', type=str)
    parser.add_argument('-post_id',dest='post_id',
            help='Unique ID for the post that the comment belong to, needed for download', type=str)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    comment_id = args.comment_id
    post_id = args.post_id 
    # For debugging 
    allow_duplicates = True
    if db.query_is_empty(db.get_post_with_ID(post_id)) or allow_duplicates:
        print("Downloading")
        reddit.download_image(post_id) 
        print('Loading Net')
        net.colorize_image('%s/in/%s.jpg' % (imgPath, post_id), '%s/out/%s.png' % (imgPath, post_id))
        print("Uploading")
        imgur_link = imgur.upload_image('%s/out/%s.png' % (imgPath, post_id))
        print("Replying")
        reddit.reply(comment_id, imgur_link)
        db.add_post_value(post_id, imgur_link)
    else:
        print("Already colorized, aborting")
