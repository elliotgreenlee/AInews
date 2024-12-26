# AI News Filter

News sucks now. Of course, there are exceptional articles 
written every day: live breaking stories, investigative research, and critical follow up.
Unfortunately, it's impossible to follow these stories and remain sane because of the soup of
garbage coverage. "People on twitter are saying", "Some such person said some such thing", 
feel good stories, fluff pieces, and incremental coverage without anything new crowd the space.

This code: 
- helps build a query to search Google News
- retrieves the returned articles as an XML rss feed
- parses the feed to find the articles
- writes out the content to a csv so that chatgpt can read and summarize

## How To

### Build your news search query
Searches can be tested at https://news.google.com/home?hl=en-US&gl=US&ceid=US:en and the url
found at the top.

- Last X Days/Time - :7d
  - not supported yet
- After Date - after:2020-01-01
- Before Date - before:2021-12-31
- News Site - site:bbc.com
  - Only bbc is supported currently
- Random search text - trans rights

### Build your AI query

https://chatgpt.com/share/676d8019-903c-800f-9e7a-30ead60c66ed
As with most large-effort AI conversations, breaking up the task into pieces
seems to be the right way to proceed. 

1. Prime with instructions about what will happen.
2. Give the csv of articles.
3. Give a detailed explanation of each of the scores 1-10. You can have the AI write this separately based on your rough explanation.
4. Explain how the task will be broken up into sets of 10 articles.
5. Give each piece of the task
6. Aggregate pieces and re-score
7. Finish with any summary tasks 

## Resources
I started here
https://www.reddit.com/r/sheets/comments/dkgmyp/pulling_data_from_google_news_to_google_sheet_how/
and ended up here
https://github.com/SSujitX/google-news-url-decoder

## Scraping
Complies with Reuters robots.txt https://www.reuters.com/robots.txt