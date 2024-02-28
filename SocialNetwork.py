from Observe import Observer, Observable
class SocialNetwork:
    _instance = None

    def __new__(cls, platform_name):
        if cls._instance is None:
            cls._instance = super(SocialNetwork, cls).__new__(cls)
        return cls._instance

    def __init__(self,name):
        self._platform_name = name
        self._users = []
        print(f"The social network {self._platform_name} has created!")
    def sign_up(self, username, password):
        u = User(username, password)
        self._users.append(u)
        return u

    def log_in(self, username, password):
        for user in self._users:
            if user._username == username and user._password == password:
                print(f"{username} has logged in")
                return user
        print("Invalid username or password")

    def log_out(self, username):
        print(f"{username} has logged out")


class User(Observer, Observable):
    def __init__(self, username, password):
        super().__init__()
        self._username = username
        self._password = password
        self._following = []
        self._followers = []
        self._posts = []
        self._notifications = []

    def follow(self, user):
        self._following.append(user)
        user._followers.append(self)
        print(f"{self._username} started following {user._username}")

    def unfollow(self, user):
        self._following.remove(user)
        user._followers.remove(self)
        print(f"{self._username} unfollowed {user._username}")

    def publish_post(self, post_type, *args):
        factory = PostFactory()
        post = factory.create_post(self, post_type, *args)
        self._posts.append(post)
        self.notify(post)
        if post_type == "Text":
            print(f"{self._username} published a post:\n{args[0]}\n")
        elif post_type == "Image":
            print(f"{self._username} posted a picture\n")
        elif post_type == "Sale":
            print(f"{self._username} posted a product for sale:\nFor sale! {args[0]}, price: {args[1]}, pickup from: {args[2]}\n")
        return post

    def update(self, post):
        notification = f"{self._username} received a notification about a new post"
        self._notifications.append(notification)
        print(f"{self._username} received a notification about a new post")

    def updatelike(self, post, user):
        notification = f"{self._username} received a notification about a new like from {user._username}"
        self._notifications.append(notification)
        print(f"{self._username} received a notification about a new like from {user._username}")

    def updatecomment(self, post, user, text):
        notification = f"{self._username} received a notification about a new comment from {user._username}"
        self._notifications.append(notification)
        print(f"{self._username} received a notification about a new comment from {user._username}")

    def getpassword(self):
        return self._password

    def getusername(self):
        return self._username







class PostType:
    TEXT = "Text"
    IMAGE = "Image"
    SALE = "Sale"

class PostFactory:
    def create_post(self, user, post_type, *args):
        if post_type == PostType.TEXT:
            return TextPost(user, *args)
        elif post_type == PostType.IMAGE:
            return ImagePost(user, *args)
        elif post_type == PostType.SALE:
            return SalePost(user, *args)
        else:
            raise ValueError("Invalid post type")
class TextPost:
    def __init__(self, user, text):
        self._user = user
        self._text = text
        self._likes = []
        self._comments = []

    def like(self, user):
        self._likes.append(user)

    def comment(self, user, text):
        self._comments.append((user, text))



class ImagePost:
    def __init__(self, user,  image):
        self._user = user
        self._image = image
        self._likes = []
        self._comments = []

    def like(self, user):
        self._likes.append(user)

    def comment(self, user, text):
        self._comments.append((user, text))

class SalePost:
    def __init__(self, user, product, price, location):
        self._user = user
        self._product = product
        self._price = price
        self._location = location
        self._likes = []
        self._comments = []
        self._sold = False

    def like(self, user):
        self._likes.append(user)

    def comment(self, user, text):
        self._comments.append((user, text))

    def discount(self, amount, password):
        if password == self._user.getpassword():
            self._price = self._price - (amount/100 * self._price)
            name = self._user.getusername()
            print(f"Discount on {name} product! the new price is: {self._price}\n")

    def sold(self, password):
        if password == self._user.getpassword():
            self._sold = True
            name = self._user.getusername()
            print(f"{name}'s product is sold")

