import praw
import json
import newspaper
from newspaper import Article
import pandas as pd
from sqlalchemy import create_engine

from datetime import datetime

with open('secrets.json') as file:
    secrets = json.load(file)

    client_id = secrets['client_id']
    client_secret = secrets['client_secret']
    user_agent = secrets['user_agent']
    connection_string = secrets['connection_string']

def get_articles():
    reddit = praw.Reddit(client_id=client_id,
                        client_secret=client_secret,
                        user_agent=user_agent)

    posts = {}
    for i, submission in enumerate(reddit.subreddit('worldnews').hot(limit=10)):

        # if i % 10 == 0: print(i)

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

    return posts

def convert_to_dataframe(posts):
    """
    converts a dictionary of posts to a dataframe to be inserted into table
    
    Arguments:
        posts {dict} -- dictionary of posts from reddit
    """
    df = pd.DataFrame(data=posts).transpose().reset_index()
    df = df.rename(columns={'index': 'post_id'})

    return df

def insert_into_db(df):
    """
    inserts a dataframe into the article table
    
    Arguments:
        df {[type]} -- [description]
    """
    db = create_engine(connection_string)

    # remove any records from the dataframe that are already in the database
    ids = pd.read_sql('SELECT DISTINCT post_id FROM NAP.article', con=db)
    ids = ids['post_id'].tolist()

    df = df[~df['post_id'].isin(ids)].reset_index(drop=True)

    # don't try to insert if the dataframe is empty
    if df.empty:
        return

    df.to_sql('article', con=db, if_exists='append', index=False)

def main(event=None, context=None):
    try:
        posts = get_articles()
        df = convert_to_dataframe(posts)
        insert_into_db(df)

        return 'success'
    except:
        return 'failed'

# driver code
start_time = datetime.now()
main()
print(datetime.now() - start_time)