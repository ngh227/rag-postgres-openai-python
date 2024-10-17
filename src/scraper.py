import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_peacock_hill():
    url = "https://www.peacockhillproductions.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    data = []
    for section in soup.find_all('section', class_='content-section'):
        title = section.find('h2').text if section.find('h2') else ''
        content = section.find('div', class_='content').text if section.find('div', class_='content') else ''
        data.append({'title': title, 'content': content})
    
    return pd.DataFrame(data)

def process_data(df):
    df['content'] = df['content'].replace('<.*?>', '', regex=True)
    df['content'] = df['content'].str.strip()
    return df

def get_processed_data():
    df = scrape_peacock_hill()
    return process_data(df)

if __name__ == "__main__":
    processed_df = get_processed_data()
    print(processed_df)