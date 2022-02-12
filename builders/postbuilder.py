from .post import Posts


class PostBuilder:
    def __init__(self):
        self.id = 0
        self.title = ""
        self.body = ""
        self.posted_by = 0

    @staticmethod
    def item():
        return PostBuilder()

    def with_title(self, title):
        self.title = title
        return self

    def with_body(self, body):
        self.body = body
        return self

    def with_posted_by(self, posted_by):
        self.posted_by = posted_by
        return self

    def with_id(self, id):
        self.id = id
        return self

    def build(self):
        return Posts(self.id, self.title, self.body, self.posted_by)
