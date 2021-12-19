from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import random

AIRBNB_BASE_URL = 'https://www.airbnb.com'

ROOM_LINK_ROUTE = '/rooms/'
ROOM_PHOTOS_ROUTE = '/photos/'
ROOM_IMAGE_PATTERN = r'(https?:\/\/.*\.(?:png|jpg))'

session = HTMLSession()

# https://www.airbnb.com/s/homes?rank_mode=top_rated&title_type=TOP_REVIEWED_HOMES&search_type=section_navigation&items_offset=5125
# https://www.airbnb.com/s/homes?items_offset=5125

def get_random_room():
    r = session.get(f'{AIRBNB_BASE_URL}/s/homes \
                    ?rank_mode=top_rated \
                    &title_type=TOP_REVIEWED_HOMES \
                    &items_offset={random.randint(0, 5000)}')

    room_links = [link for link in r.html.links if link.startswith(ROOM_LINK_ROUTE)]
    room_links = [remove_query_parameters(link) for link in room_links]

    room_url = random.choice(room_links)

    return {
        'url': room_url,
        'title': '',
        'size': '',
        'location': '',
        'summary': '',
    }

def get_room_images(room_url):
    r = session.get(f'{room_url}{ROOM_PHOTOS_ROUTE}')

    room_images = [image.attrs['src'] for image in r.html.find('img')]
    room_images = [remove_query_parameters(image) for image in room_images]

def get_room_info(room_url):
    # r = session.get(room_url)
    # # r.html.render()


    # content = r.html.find('#site-content')[0]
    # title_bar = content.find('.plmw1e5')[0]
    # title_bar = title_bar.find('.mq5rv0q')[0]

    r = requests.get(room_url)
    soup = BeautifulSoup(r.text, "html.parser") # fallback to a more fully featured HTML parser

    print(title_bar.html) # Location

def remove_query_parameters(string):
    return string.split('?')[0]

if __name__ == '__main__':
    # random_room = get_random_room()
    # room_images = get_room_images(random_room)

    random_room = 'https://www.airbnb.com.au/rooms/27310899'
    get_room_info(random_room)

