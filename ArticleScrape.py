import newspaper
from newspaper import Article, Config

# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
# config = Config()
# config.browser_user_agent = user_agent

url = 'https://www.cbc.ca/news/politics/sophie-trudeau-feeling-great-covid-19-1.5513731'
article = Article(url)
article.download()
article.parse()
# print(article.title)
# print(article.publish_date)
# print(str(article.text).replace('\n', ' ').replace('  ', ' '))

paper = newspaper.build(url)
print(paper.brand)

# import pandas as pd

# df = pd.read_json('posts.json')
# df = df.transpose()
# df.to_csv('posts.csv')
