import requests
from bs4 import BeautifulSoup


def search_django_site(query):
    """
    Make a request to the Django documentation site, passing the given query. Return the results 
    displayed on the page.
    """
    DJANGO_ENDPOINT = 'https://docs.djangoproject.com/en/3.0/search/'
    final_results = []
    
    response = requests.get(DJANGO_ENDPOINT, params={'q': query})

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find('dl', class_='search-links').findAll('dt')
        for result in results:
            title_anchor = result.find('h2', class_='result-title').find('a')
            title = title_anchor.text.strip()
            url = title_anchor['href']
            
            breadcrumbs = []
            for crumb in result.find('span', class_='meta breadcrumbs').findAll('a'):
                breadcrumbs.append(crumb.text.strip())

            final_results.append({
                'title': title,
                'url': url,
                'breadcrumbs': ' > '.join(breadcrumbs)
            })

    return final_results
