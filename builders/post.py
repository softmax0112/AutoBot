class Posts:
    def __init__(self, id, title, body, posted_by):
        self.id = id
        self.title = title
        self.body = body
        self.posted_by = posted_by
        self.likes = 0

    def set_id(self, id):
        self.id = id

    def set_likes(self):
        self.likes = self.likes + 1

    def set_title(self, title):
        self.title = title

    def set_body(self, body):
        self.body = body

    def get_title(self) -> str:
        return self.title

    def get_body(self) -> str:
        return self.body

    def set_posted_by(self, posted_by):
        self.posted_by = posted_by

    def get_posted_by(self) -> str:
        return self.posted_by

    def get_id(self):
        return self.id

    def to_dict(self):
        return {
            'title': self.title,
            'body': self.body,
            'posted_by': self.posted_by
        }

    def display(self):
        print("\t\t\t Post")
        print("Title: ", self.title)
        print("Body: ", self.body)
        print("Posted By: ", self.posted_by)
