from bs4 import BeautifulSoup
import requests
import random

AIRBNB_BASE_URL = 'https://www.airbnb.com'

ROOM_LINK_ROUTE = '/rooms/'
ROOM_PHOTOS_ROUTE = '/photos/'
ROOM_IMAGE_PATTERN = r'(https?:\/\/.*\.(?:png|jpg))'

def get_random_room():
    soup = get_soup(f'{AIRBNB_BASE_URL}/s/homes?rank_mode=top_rated&title_type=TOP_REVIEWED_HOMES&items_offset={random.randint(0, 5000)}')

    room_links = [link.get('href') for link in soup.find_all('a')]
    room_links = [link for link in room_links if link.startswith(ROOM_LINK_ROUTE)]
    room_links = [remove_query_parameters(link) for link in room_links]

    room_url = f'{AIRBNB_BASE_URL}{random.choice(room_links)}'

    return room_url

def get_room_images(room_url):
    soup = get_soup(f'{room_url}{ROOM_PHOTOS_ROUTE}')

    room_images = [image.get('src') for image in soup.find_all('img')]
    room_images = [remove_query_parameters(image) for image in room_images]

    return room_images

def get_room_info(room_url):
    soup = get_soup(room_url)

    # TODO: Determine a better way to get room information. This is very fragile.
    title = soup.find_all('h1', {'class': '_fecoyn4'})[0].text
    location = soup.find_all('span', {'class': '_pbq7fmm'})[0].text
    size = soup.find_all('ol', {'class': '_194e2vt2'})[0].text

    description = soup.find_all('div', {'data-section-id': 'DESCRIPTION_DEFAULT'})[0].text
    description = description.replace('Show more', '')

    return {
        'title': title,
        'location': location,
        'space': size,
        'description': description
    }

def remove_query_parameters(string):
    return string.split('?')[0]

def get_soup(url):
    print(f'Getting URL: {url}')
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')

if __name__ == '__main__':
    random_room_url = get_random_room()
    room_images     = get_room_images(random_room_url)
    room_info       = get_room_info(random_room_url)

    room_info['url'] = random_room_url
    room_info['images'] = room_images

    print(room_info)