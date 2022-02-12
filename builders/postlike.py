class PostLike:
    def __init__(self, liked_by, post):
        self.liked_by = liked_by
        self.post = post

    def set_liked_by(self, liked_by):
        self.liked_by = liked_by

    def set_post(self, post):
        self.post = post

    def get_liked_by(self):
        return self.liked_by

    def get_post(self):
        return self.post

    def to_dict(self):
        return {
            'user_who_liked': self.liked_by,
            'post': self.post
        }

    def display(self):
        print("\t\t\t Post")
        print("liked_by: ", self.liked_by)
        print("Post: ", self.post)

