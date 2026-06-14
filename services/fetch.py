import arxiv
import requests
import time

from models import ResearchItem
import json

import arxiv
import requests
import time
from datetime import datetime
from models import ResearchItem
import json

def fetch_hackernews(database):
    number_of_items_added = 0
    
    # Get data from hackernews
    url = "https://hacker-news.firebaseio.com/v0/"

    # 1735689600 corresponds to Jan 1, 2025
    params = {
        "query": "AI",
        "tags": "story",
        "numericFilters": "created_at_i>1735689600",
        "hitsPerPage": 100
    }

    print("Querying Hacker News...")

    # Get the data (safely)
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    # Save the data into a variable
    response_data = response.json()
    print("Responses received from HN")
    
    # Get existing items to check duplicates
    existing_items = database.get_all_items()
    existing_urls = [item[2] for item in existing_items]

    important_urls = []

    # Loop through the data
    for hit in response_data["hits"]:
        # Skip items missing a valid destination URL
        if not hit.get('url'):
            continue
            
        hn_url = hit['url']

        # Prevent duplication + flag high importance
        if "arxiv.org" in hn_url:
            print(f"Found arXiv paper trending on HN: {hit['title']}")
            
            # Extract the arXiv ID or clean URL to find it in your database
            clean_arxiv_url = hn_url.split('/pdf/')[-1].split('.pdf')[0]
            
            # Tag as trending
            important_urls.append(clean_arxiv_url)
            continue

        # Breaks the loop once old info starts repeating
        if hn_url in existing_urls:
            print("This item already exists in the database")
            break

        # Returns tags as an array of strings (e.g., ['story', 'author_pg'])
        unique_tags = set(hit.get('_tags', []))
        tags_text = ",".join(sorted(unique_tags))
        
        # Returns 'author' as a single string, not an array of objects
        author_text = hit.get('author', 'Unknown')

        #Parse the string ISO timestamp into a date object
        created_at_str = hit.get('created_at', '')[:10]
        try:
            item_date = datetime.strptime(created_at_str, "%Y-%m-%d").date()
        except ValueError:
            item_date = datetime.today().date()

        # Create the researchitem
        item = ResearchItem(
            title=hit.get('title', 'No Title'),
            url=hn_url,
            date=item_date,
            authors=author_text,
            summary=f"HN Score: {hit.get('points', 0)} | Comments: {hit.get('num_comments', 0)}",
            tags=unique_tags
        )

        database.add_item(item)
        print(f"Added HN item: {item.title}")
        number_of_items_added += 1
        time.sleep(0.001)

    print("Finished fetching from Hacker News")

    # Tag duplicate items as important
    for url in important_urls:
        # We look for any existing row where the URL contains the arXiv ID string
        database.mark_as_trending(url)


    return number_of_items_added



def fetch_arxiv(database):

    number_of_items_added = 0

    client = arxiv.Client()
    search = arxiv.Search(
    query="cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR cat:cs.CL",
    max_results=1000,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
    )
    
    print("fetching from arxiv...")

    existing_items = database.get_all_items()
    existing_urls = []
    for item in existing_items:
        existing_urls.append(item[2])

    for result in client.results(search):
        
        # Breaks the loop once it reaches the point no new info's there
        if result.pdf_url in existing_urls:
            print("this item already exists")
            break

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
        number_of_items_added += 1

        time.sleep(0.0001)

    print("Finished fetching from arxiv")
    return number_of_items_added

def fetch_output():
    pass