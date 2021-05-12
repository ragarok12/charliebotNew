# -*- coding: utf-8 -*-

import os
import sys
import threading
import time
import argparse
import config

from glob import glob

sys.path.append(os.path.join(sys.path[0], "../../"))
import schedule  # noqa: E402
from instabot import Bot, utils  # noqa: E402

#cool

bot = Bot(
    comments_file=config.COMMENTS_FILE,
    blacklist_file=config.BLACKLIST_FILE,
    whitelist_file=config.WHITELIST_FILE,
    friends_file=config.FRIENDS_FILE,
)

bot.login(username="designspostersbanners",password="Shubh@7397")

bot.logger.info("ULTIMATE script. Safe to run 24/7!")

random_user_file = utils.file(config.USERS_FILE)
random_hashtag_file = utils.file(config.HASHTAGS_FILE)
photo_captions_file = utils.file(config.PHOTO_CAPTIONS_FILE)


def stats():
    bot.save_user_stats(bot.user_id)


def like_hashtags():
    bot.like_hashtag(random_hashtag_file.random(), amount=700 // 24)


def like_timeline():
    bot.like_timeline(amount=300 // 24)


def like_followers_from_random_user_file():
    bot.like_followers(random_user_file.random(), nlikes=3)


def follow_followers():
    bot.follow_followers(
        random_user_file.random(), nfollows=config.NUMBER_OF_FOLLOWERS_TO_FOLLOW
    )


def comment_medias():
    bot.comment_medias(bot.get_timeline_medias())

def unfollow_non_followers():
    bot.unfollow_non_followers(
        n_to_unfollows=config.NUMBER_OF_NON_FOLLOWERS_TO_UNFOLLOW
    )


def follow_users_from_hashtag_file():
    bot.follow_users(bot.get_hashtag_users(random_hashtag_file.random()))


def comment_hashtag():
    hashtag = random_hashtag_file.random()
    bot.logger.info("Commenting on hashtag: " + hashtag)
    bot.comment_hashtag(hashtag)



def put_non_followers_on_blacklist():  # put non followers on blacklist
    try:
        bot.logger.info("Creating non-followers list")
        followings = set(bot.following)
        followers = set(bot.followers)
        friends = bot.friends_file.set  # same whitelist (just user ids)
        non_followers = followings - followers - friends
        for user_id in non_followers:
            bot.blacklist_file.append(user_id, allow_duplicates=False)
        bot.logger.info("Done.")
    except Exception as e:
        bot.logger.error("Couldn't update blacklist")
        bot.logger.error(str(e))


def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(1).hour.do(run_threaded, stats)
print("96")
schedule.every(4).hours.do(run_threaded, like_hashtags)
print("98")
schedule.every(2).hours.do(run_threaded, like_timeline)
print("100")
schedule.every(1).days.at("16:00").do(
    run_threaded, like_followers_from_random_user_file
)
print("104")
schedule.every(2).days.at("11:00").do(run_threaded, follow_followers)
print("106")
schedule.every(7).hours.do(run_threaded, comment_medias)
print("108")
schedule.every(1).days.at("08:00").do(run_threaded, unfollow_non_followers)
print("110")
schedule.every(12).hours.do(run_threaded, follow_users_from_hashtag_file)
print("112")
schedule.every(6).hours.do(run_threaded, comment_hashtag)
print("114")
schedule.every(4).days.at("07:50").do(run_threaded, put_non_followers_on_blacklist)

while True:
    schedule.run_pending()
    time.sleep(1)