import random

import yaml
from builders.postlike import PostLike
from builders.userbuilder import UserBuilder
from builders.postbuilder import PostBuilder
from faker import Faker
from builders.restClient import SocialNetworkClient
from itertools import groupby

configuration_file = 'configuration.yaml'
BASE_URL = 'http://localhost:8009'

registered_users = []


def random_posts_to_like(posts):
    posts_list = []
    for post in posts:
        posts_list.append(post['id'])
    indexes = []
    if len(posts_list) >= 1:
        random_number = random.randint(1, len(posts_list))
        for i in range(random_number):
            indexes.append(posts_list[(random.randrange(len(posts_list)))])

        return list(set(indexes))


class AutomationBot:
    user_builders = []
    post_builders = []
    posts_likes = []

    def __init__(self):
        self._number_of_users = 0
        self._max_posts_per_user = 0
        self._max_likes_per_user = 0

    def read_file(self):
        config_data = yaml.load(open(configuration_file, 'r'), Loader=yaml.FullLoader)
        self._number_of_users = config_data['number_of_users']
        self._max_posts_per_user = config_data['max_posts_per_user']
        self._max_likes_per_user = config_data['max_likes_per_user']

    def create_test_users(self):
        fake = Faker()
        api_client = SocialNetworkClient(None, None)
        user_builders = [UserBuilder() for i in range(self._number_of_users)]
        print(f'\t\t\tRegister {self._number_of_users} new users.')
        for user in user_builders:
            name = str(fake.name()).split(' ')
            firstname = name[0]
            lastname = name[1]
            username = name[0] + name[1]
            email = username + "@gmail.com"
            password = fake.password()
            data = user.item().with_username(username).with_first_name(firstname).with_last_name(lastname).\
                with_email(email).with_password(password).build()
            self.user_builders.append(data)
            response = api_client.register_dumy_users(data.__dict__)
            data.set_id(response['id'])
            print('Successfully Registered :', response)

    def create_fake_post_data(self):
        for reg_user in self.user_builders:
            reg_user_data = reg_user.__dict__
            print(f'\n\n\t\t\tAuthenticating {reg_user_data["username"]}.')
            with SocialNetworkClient(reg_user_data['username'], reg_user_data['password']) as client:
                num_of_posts = random.randint(1, self._max_posts_per_user)
                print(f'\t\t{reg_user_data["username"]} creating {num_of_posts} posts:')
                posts = [PostBuilder() for i in range(num_of_posts)]
                for post in posts:
                    fake = Faker()
                    title = fake.word()
                    body = fake.sentence()
                    data = post.item().with_title(title).with_body(body).with_posted_by(reg_user_data['id']).build()
                    self.post_builders.append(data)
                    response = client.create_dumy_post(data.__dict__)
                    data.set_id(response['id'])
                    print('Post Created: ', response)

    # Users with their total posts count
    def users_with_posts_counts(self):
        posts = [posts.__dict__ for posts in self.post_builders]
        grouped = [list(result) for key, result in groupby(
            posts, key=lambda post: post['posted_by'])]
        user_posts_count = []
        for data in grouped:
            user_posts_count.append({'user': data[0]['posted_by'], 'total_posts': len(data), 'likes': 0})

        sorted_user_posts_count = sorted(user_posts_count, key=lambda user_post: user_post['total_posts'], reverse=True)
        return sorted_user_posts_count

    def search_user(self, id):
        users = [users.__dict__ for users in self.user_builders]
        for user in users:
            if user['id'] == id:
                return user

    def increase_likes(self, post_id):
        for post in self.post_builders:
            if post.__dict__['id'] == post_id:
                post.set_likes()
                break

    def user_with_no_likes_post(self, post_to_be_liked_by):
        posts = [post.__dict__ for post in self.post_builders]
        posts_by = [post['posted_by'] for post in posts if post['likes'] == 0 and post['posted_by'] is not post_to_be_liked_by]
        return list(set(posts_by))

    # Return all posts by a given user
    def get_all_posts_of_user(self, user_id):
        posts = [post.__dict__ for post in self.post_builders]
        user_posts = [post for post in posts if post['posted_by'] == user_id]
        return user_posts

    def like_posts(self):
        sorted_user_posts_count = self.users_with_posts_counts()
        for user in sorted_user_posts_count:
            print(f'\n\n\t\t\tStart Liking Post with {user["user"]}')
            like_from_user = self.search_user(user['user'])
            with SocialNetworkClient(like_from_user['username'], like_from_user['password']) as client:
                try:
                    no_likes_post_users = self.user_with_no_likes_post(user['user'])
                    if not no_likes_post_users:
                        return False
                except Exception as e:
                    pass
                for no_likes_post_user in no_likes_post_users:
                    no_likes_post_user_list = self.get_all_posts_of_user(no_likes_post_user)
                    posts_to_like = random_posts_to_like(no_likes_post_user_list)
                    if posts_to_like is None:
                        return False
                    for like in posts_to_like:
                        response = client.like_post({'post_liked': like})
                        if response != 'Already Liked':
                            self.posts_likes.append(PostLike(like_from_user['id'], like))
                            self.increase_likes(like)

                        print('Post Liked: ', response)

        return True

    def start_likes(self):
        result = True
        while result is True:
            result = self.like_posts()
        print("End Automation")


if __name__ == "__main__":
    bot = AutomationBot()
    bot.read_file()
    bot.create_test_users()
    bot.create_fake_post_data()
    bot.start_likes()
