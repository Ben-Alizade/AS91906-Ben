import arxiv
import requests
import time

from models import ResearchItem
import json

def fetch_hackernews(database):

    return 0

"""    # 1. This is the correct data URL your script needs
    url = "https://algolia.com"

    params = {
        "query": "AI",
        "tags": "story",
        "numericFilters": "created_at_i>1735689600"
    }

    print("params established")

    # 2. Get the data safely
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    # 3. Save the data into a variable
    response_data = response.json()
    print("responses received")
    
    existing_items = database.get_all_items()
    existing_urls = []
    for item in existing_items:
        existing_urls.append(item[2])

    # 4. Loop through the data we just saved
    for hit in response_data["hits"]:
        print("It worked!!! YYAY")


        # Breaks the loop once it reaches the point no new info's there
        if hit['url'] in existing_urls:
            print("this item already exists")
            break

        # Extract all tags, strip 'cs.', and keep only unique values
        unique_tags = set()
        for category in hit['tags']:
            clean_tag = category.replace("cs.", "")
            unique_tags.add(clean_tag)
        
        # Extract all authors as clean string names and ensure uniqueness
        unique_authors = set()
        for author in hit['authors']:
            unique_authors.add(author.name)

        # Convert both sets to a sorted, comma-separated text string
        tags_text = ",".join(sorted(unique_tags))
        authors_text = ",".join(sorted(unique_authors))
        print(tags_text)
        print(authors_text)

        item = ResearchItem(
            title=hit['title'],
            url=hit['url'],
            date=hit['title']
            authors=authors_text,
            summary=result.summary,
            tags=unique_tags
        )

        print(item)

        database.add_item(item)
        print(f"Item to the database")
        number_of_items_added += 1

        time.sleep(0.001)

    print("Finished fetching from arxiv")
    return number_of_items_added"""


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

        time.sleep(0.001)

    print("Finished fetching from arxiv")
    return number_of_items_added

def fetch_output():
    pass