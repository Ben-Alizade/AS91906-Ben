import arxiv
import requests
from models import ResearchItem
import json
import time


def fetch_hackernews():

    url = "https://algolia.com"

    params = {
    "query": "arxiv AI",
    "tags": "story",        # Only fetch main links/posts, not comments
    "numericFilters": "created_at_i>1735689600" # Post-Jan 1, 2025
    }

    print("params established")
    response = requests.get(url, params=params).json()
    print("responses received")

    for hit in response["hits"]:
        print(f"Title: {hit['title']}")
        print(f"URL: {hit['url']}")
        print(f"Points: {hit['points']} | Comments: {hit['num_comments']}")
        print("-" * 40)

def fetch_arxiv(database):
    client = arxiv.Client()
    search = arxiv.Search(
    query="cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR cat:cs.CL",
    max_results=100,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
    )
    
    for result in client.results(search):

        # Extract all tags, strip 'cs.', and keep only unique values
        unique_tags = set()
        for category in result.categories:
            clean_tag = category.replace("cs.", "")
            unique_tags.add(clean_tag)
        
        # Extract all authors as clean string names and ensure uniqueness
        unique_authors = set()
        for author in result.authors:
            unique_authors.add(author.name)

        # Convert both sets to a sorted, comma-separated text string
        tags_text = ",".join(sorted(unique_tags))
        authors_text = ",".join(sorted(unique_authors))
        print(tags_text)
        print(authors_text)

        item = ResearchItem(
            title=result.title,
            url=result.pdf_url,
            date=result.published.date(),
            authors=authors_text,
            summary=result.summary,
            tags=unique_tags
        )

        print(item)

        database.add_item(item)
        print(f"Item to the database")

        time.sleep(0.05)

def fetch_output():
    pass