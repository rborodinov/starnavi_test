
import grequests
import requests
import loremipsum
from urllib.parse import urljoin
from typing import Generator
import random, string, argparse, json

PASSWORD = "string"
CONFIG_FILE_NAME = 'bot_config.json'


def random_email():
    """Generates random email from"""
    def random_char(char_num):
        return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))
    return (random_char(7) + "@email.com")


class Bot:
    def __init__(self, number_of_users:int, max_posts_per_user:int,
                 max_likes_per_user:int, domain:str, **kwargs):

        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.domain = domain

    def create_user_url(self):
        path = "/api/users/"
        params = {
          "email": random_email(),
          "password": PASSWORD
        }
        return (urljoin(base=self.domain, url=path), params)

    def create_user_url_pull(self):
        for _ in range(self.number_of_users):
            yield self.create_user_url()

    def get_access_tokens_urls(self, result_user_signup):
        path = "/api/token"
        for user_response in grequests.imap(result_user_signup):
            if user_response.status_code == 200:
                email = user_response.json().get("email")
                param = {"grant_type": "password",  "username": email, "password": PASSWORD}
                yield (urljoin(base=self.domain, url=path), param)

    def create_post_urls_pull(self):
        path ="/api/posts/"
        for _ in range(random.randint(1, self.max_posts_per_user)):
            data = {
                "title": loremipsum.get_sentence(),
                "description": loremipsum.get_paragraph()
            }
            yield (urljoin(base=self.domain, url=path), data)

    def create_likes_urls_pull(self, post_id_list):
        for _ in range(random.randint(1, self.max_likes_per_user)):
            post_id = random.choice(post_id_list)
            path = f"/api/posts/{post_id}/likes"
            data = {}
            yield (urljoin(base=self.domain, url=path), data)


    def __call__(self):
        """ Main method controls evaluation process"""
        # Generator that registers new users
        result_user_signup: Generator = (grequests.post(url, json=data)
                                         for url, data in self.create_user_url_pull())
        # Generator that gaing access_tokens for new registered users
        result_accesing_tokens: Generator = (grequests.post(url, data=data)
                                             for url, data in self.get_access_tokens_urls(result_user_signup))
        user_authorization_headers = []
        for token_response in grequests.imap(result_accesing_tokens):
            if token_response.status_code == 200:
                # Working with single user through access_token
                token_data: dict = token_response.json()
                headers: dict = {"Authorization": f"{token_data['token_type']} {token_data['access_token']}"}
                user_authorization_headers.append(headers)

                # Generator creating posts
                result_creating_posts: Generator = (grequests.post(url, json=data, headers=headers)
                                                    for url, data in self.create_post_urls_pull())
                grequests.map(result_creating_posts)

        # ids of all posts already published
        response = requests.get(urljoin(base=self.domain, url="/api/feed/"))
        post_id_list = [post['id'] for post in response.json()]
        for headers in user_authorization_headers:
            # Generator adding likes to random post
            result_likes: Generator = (grequests.post(url, json=data, headers=headers)
                            for url, data in self.create_likes_urls_pull(post_id_list))
            # evaluate likes generator
            grequests.map(result_likes)


def parse_command_line_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--number_of_users')
    parser.add_argument('--max_posts_per_user')
    parser.add_argument('--max_likes_per_user')
    parser.add_argument('--domain')
    args = parser.parse_args()
    args = args.__dict__
    domain = args.pop('domain', None)
    data = {}
    for key, value in args.items():
        if value:
            data[key] = int(value)
    if domain:
        data['domain'] = domain
    return data


def parse_config_file():
    # Opening JSON file
    with open('bot_config.json') as f:
        return json.load(f)


if __name__ == '__main__':

    domain = "http://127.0.0.1:8000/"
    data = {"domain": domain}
    data.update(**parse_config_file())
    data.update(**parse_command_line_config())
    print(f"Bot started. using {data['domain']}")

    bot = Bot(**data)
    bot()
    print("Work is finished")