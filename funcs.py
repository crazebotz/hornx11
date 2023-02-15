
import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup

def get_links(url):
    # Send a GET request to the URL and store the response
    response = requests.get(url)

    # Parse the response with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the element with the id attribute of "tracking-url"
    element = soup.find("a", {"id": "tracking-url"})

    # Get the href link of the element
    href_link = element.get("href")

    # Send a POST request to the href link and store the response
    try:response = requests.post(href_link)
    except ConnectTimeout: return False

    # Parse the response with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the element with the class attribute of "col-sm-8 col-sm-offset-2 well view-well"
    div = soup.find("div", {"class": "col-sm-8 col-sm-offset-2 well view-well"})

    # Find all the links within the div element and store them in a list
    try:
        links = [link.get("href") for link in div.find_all("a")]
    except AttributeError:
        as_str = "No Links Found Or Invalid Link You sent"
        return as_str


    # Return the list of links
    as_str='\n'.join(links)

    return as_str


def extract_first_three_words(input_string):
    words = input_string.split("-")
    first_three = "+".join(words[:3])
    words = first_three.split("/")[-1]
    return words




def extract_multi_posts(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all('div', {'class': 'slide loop-video'})
    indx = 1
    post_dict = ''
    empty = []
    for post in posts:
        title = post.a['title']
        post_url = post.a['href']
        data = title+"\n"+post_url+'\n\n'
        empty.append(data)
        post_dict += f'{title}\n{post_url}\n'
        # post_dict[f'{title}'] = post_url
        indx += 1

    return empty


def search_one_post(url, query):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('article', {'class': 'thumb-block'})
    for post in posts:
        post_url = post.a['href']
        title = post.a['title']           
        image_url = post.img['data-src']
        post_url = post.a['href']
        dl_links = get_links(post_url)
        if dl_links == False:
            return False

        if query == post_url:
            return title, image_url, post_url, dl_links


    return title, image_url, post_url


def search_multi_posts(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all('article', {'class': 'thumb-block'})

    indx = 1
    post_dict = ''
    empty = []
    for post in posts:

        title = post.a['title']
        post_url = post.a['href']
        data = title+"\n"+post_url+'\n\n'

        empty.append(data)
        post_dict += f'{title}\n{post_url}\n'
        indx += 1

    return empty


s_url = "https://pornx11.com/?s="
# search_multi_posts(s_url)


def group_names(names):
    all_list = []
    for i in range(0, len(names), 5):
        group = names[i:i+5]
        if len(group) < 5:
            group.extend([''] * (5 - len(group)))
        data = (' '.join(group))
        all_list.append(data)

    return all_list

