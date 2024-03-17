import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()
all_items=[]
book_data = []
api_key = os.getenv("API_KEY")
query = 'india'
base_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"

def fetch_all_pages(url):
    all_items = []
    startIndex = 0
    maxResults=10
    while True:
        url = f"{base_url}&startIndex={startIndex}&maxResults={maxResults}&printType=books"
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            all_items.extend(items)
            total_items = data.get('totalItems', 0)
            if total_items <= startIndex + maxResults:
                break  # Break the loop if we've reached the end of the results
                
            startIndex += maxResults
        else:
            print(f"Error: {response.status_code} - {response.content}")
            return None
    return all_items


all_items = fetch_all_pages(base_url)
if all_items is not None:
    print(f"Total items retrieved: {len(all_items)}")
    """ for i in range(len(all_items)):
        title = all_items[i]['volumeInfo']['title']
        authors = all_items[i]['volumeInfo']['authors'] """
else:
    print("An error occurred while fetching the pages.") 

for item in all_items:
    title = item.get('volumeInfo',{}).get('title','')
    authors = item.get('volumeInfo',{}).get('authors',[])
    book_data.append({'Title':title,'Authors':authors})

df = pd.DataFrame(book_data)
df.to_csv('googlebooks.csv',index=False)

print('CSV has been generated')




