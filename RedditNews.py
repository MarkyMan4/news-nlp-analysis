import praw
import json
import newspaper
from newspaper import Article
from datetime import datetime

with open('secrets.json') as file:
    secrets = json.load(file)

    client_id = secrets['client_id']
    client_secret = secrets['client_secret']
    user_agent = secrets['user_agent']

reddit = praw.Reddit(client_id=client_id,
                        client_secret=client_secret,
                        user_agent=user_agent)

posts = {}
start = datetime.now()
for i, submission in enumerate(reddit.subreddit('worldnews').hot(limit=10)):
    # track progress and save dictionary to file every 10 iterations to save progress
    # in case it error out part way through
    if i % 10 == 0: 
        print(i)
        with open('posts.json', 'w') as f:
            json.dump(posts, f)

    # skip over the first item since it's just a discussion thread on the subreddit
    if i > 0:
        post_title = submission.title
        url = submission.url
        score = submission.score
        sub_id = submission.id

        paper = newspaper.build(url)
        publisher = paper.brand

        # put a try/except here because parsing the article will sometimes return a 403 error
        try: 
            article = Article(url)
            article.download()
            article.parse()

            headline = article.title
            date_published = article.publish_date

            if date_published:
                date_published = date_published.strftime('%Y-%m-%d %H:%M:%S')

            content = str(article.text).replace('\n', ' ').replace('  ', ' ')

            posts.update({
                sub_id: {
                    'post_title': post_title,
                    'url': url,
                    'score': score,
                    'publisher': publisher,
                    'headline': headline,
                    'date_published': date_published,
                    'content': content
                }
            })
        except Exception as e:
            print(e)
            print(url)

end = datetime.now()

print(end - start)

with open('posts.json', 'w') as f:
    json.dump(posts, f)
