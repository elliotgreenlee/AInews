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

### Building your news search query

- Last X Days/Time
  - not supported yet
- After Date
- Before Date
- News Site
  - Only bbc is supported currently

### Building your AI query

Add your csv file. 

https://chatgpt.com/share/676c824a-bfcc-800f-aab8-a0a75ba5cbdb

## Resources
I started here
https://www.reddit.com/r/sheets/comments/dkgmyp/pulling_data_from_google_news_to_google_sheet_how/
and ended up here
https://github.com/SSujitX/google-news-url-decoder

## Scraping
Complies with Reuters robots.txt https://www.reuters.com/robots.txt