import praw
import random
import logging

reddit = praw.Reddit(client_id='', client_secret='',
                     password='', user_agent='',
                     username='')


def find_similar_posts(new_post):
    subreddit = reddit.subreddit(new_post.subreddit.display_name)
    for post in subreddit.top(time_filter="all", limit=200):  # adjust limit as needed
        if post.title == new_post.title:
            return post


def get_top_comments(post, num_comments=5):  # set num_comments to how many top comments you want
    post.comment_sort = 'top'
    comments = post.comments.list()
    if len(comments) > num_comments:
        return comments[:num_comments]
    else:
        return comments


def main():
    subreddits_to_monitor = ['funny', 'aww', 'askreddit', 'gonewild', 'music', 'pics', 'music']  # replace with your
    # subreddit

    logging.info(f"Monitoring subreddits: {', '.join(subreddits_to_monitor)}")

    while True:
        for subreddit in subreddits_to_monitor:
            subreddit_instance = reddit.subreddit(subreddit)
            for submission in subreddit_instance.new(limit=500):  # adjust limit as needed
                similar_post = find_similar_posts(submission)
                if similar_post is not None:
                    logging.info(f"Found similar post {similar_post.title}")
                if similar_post is not None:
                    top_comments = get_top_comments(similar_post, num_comments=3)
                    if len(top_comments) > 0:
                        chosen_comment = random.choice(top_comments)
                        submission.reply(chosen_comment.body)
                        logging.info(f"Replied to post {submission.title} with comment {chosen_comment.body}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
