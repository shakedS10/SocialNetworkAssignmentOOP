from Observe import Observer, Observable
from PIL import Image
import matplotlib.pyplot as plt

class SocialNetwork:
    # The social network class implements the singleton design patterns,
    # we don't want multiple instances of our social network and singleton helps with this need,
    # we have only one instance (_instance) that makes sure everytime the user will call this class
    # he will get only one instance and won't create another social network, with that said, this single instance
    # can be called from anywhere the user needs

    _instance = None  # Social network single instance

    def __new__(cls, platform_name):
        # this method makes sure no new instance of the social network is being created, and when one trying to
        # be created, returns the original instance that already been created
        if cls._instance is None:
            cls._instance = super(SocialNetwork, cls).__new__(cls)
        return cls._instance

    def __init__(self, name):
        # initiator the gets the name of the social network and initialized it, list of users also being initialized
        self._platform_name = name
        self._users = []
        print(f"The social network {self._platform_name} was created!")  # creation message

    def sign_up(self, username, password):
        # method that enters new user to the social network's users list and returns the user created
        # if the user's password and username meet the requirements, else returns None

        if len(password) not in range(4, 8):
            print(f"password has to be between 4-8 letters")
            return None

        for user in self._users:
            if user.getusername == username:
                print(f"username already taken")
                return None
        u = User(username, password)
        self._users.append(u)
        return u

    def log_in(self, username, password):
        # method that logs a user into the social network if the specified username and password exist
        # in the social network

        for user in self._users:
            if user.getusername() == username and user.getpassword() == password:
                print(f"{username} connected")
                return user
        print("Invalid username or password")

    def log_out(self, username):
        # method the prints that the specified user logged out
        print(f"{username} disconnected")

    def __str__(self):
        # a method that returns textual description about the social network
        description = f"{self._platform_name} social network:\n"
        for user in self._users:
            user_description = f"{user}\n"
            description += user_description

        return description


class User(Observer, Observable):
    # user class that implements the observer design pattern, every user created can be getting notifications about
    # likes on posts, comments on posts and posts uploads of the users he follows,
    # the user cant check every moment if someone liked his posts or commented on his post, and with that said
    # we need to notify the user about the things related to him in the social network, thus,
    # every user is an observer and an observable, can be notified and can notify others,
    # and that's why the observer design pattern can help with it

    def __init__(self, username, password):
        # initialization of a username given a username and a password

        super().__init__()
        self._username = username
        self._password = password
        self._following = []  # list of the users that this certain user follows
        self._posts = []  # list of all the posts this certain user has uploaded
        self._notifications = []  # list of all the notifications this certain user received

    def follow(self, user):
        # a method that gets a user and follows that user
        # if the user tried to follow himself, nothing happens

        if self.getusername() != user.getusername:
            self._following.append(user)
            user.addfollower(self)
            uname = user.getusername()
            print(f"{self._username} started following {uname}")

    def addfollower(self, user):
        # method that adds a follower to the observers list of this user
        self.attach(user)

    def removefollower(self, user):
        # method that removes a follower from the observers list of this user
        self.detach(user)

    def unfollow(self, user):
        # method that gets a user and unfollows that user
        self._following.remove(user)
        user.removefollower(self)
        uname = user.getusername()
        print(f"{self._username} unfollowed {uname}")

    def publish_post(self, post_type, *args):
        # a method that gets a post type and the contents of this post and publish it to the social network
        factory = PostFactory()  # factory instance
        post = factory.create_post(self, post_type, *args)  # post creation using factory
        self._posts.append(post)  # insertion of the post to the uploading user's posts list
        self.notify(post)  # notifies the user's followers about the post upload
        if post_type == "Text":
            print(f"{self.getusername()} published a post:\n\"{args[0]}\"\n")
        elif post_type == "Image":
            print(f"{self.getusername()} posted a picture\n")
        elif post_type == "Sale":
            print(
                f"{self.getusername()} posted a product for sale:\nFor sale! {args[0]}, price: {args[1]}, pickup from: {args[2]}\n")
        return post

    def update(self, post):
        # method that updates the followers notifications list with a new notification about a post
        uname = post.getUser().getusername()
        notification = f"{uname} has a new post"
        self._notifications.append(notification)

    def updatelike(self, post, user):
        # method that notifies the user uploaded the post about a new like from another user
        uname = user.getusername()
        notification = f"{uname} liked your post"  # like message
        self._notifications.append(notification)  # insertion to the user's notifications list
        print(f"notification to {self.getusername()}: {notification}")

    def updatecomment(self, post, user, text):
        # method that notifies the user uploaded the post about a new comment from another user
        uname = user.getusername()
        notification = f"{uname} commented on your post"  # comment message
        self._notifications.append(notification)  # insertion to the user's notifications list
        print(f"notification to {self.getusername()}: {notification}: {text}")

    def getpassword(self):
        # method that returns the user's password
        return self._password

    def getusername(self):
        # method that returns the user's username
        return self._username

    def print_notifications(self):
        # method that prints all the notifications of this user in the order of their occurrence
        print(f"{self._username}'s notifications:")
        for notification in self._notifications:
            print(f"{notification}")

    def __str__(self):
        # method that returns a textual description about this user public details
        return f"User name: {self._username}, Number of posts: {len(self._posts)}, Number of followers: {len(self.getSet())}"


class PostType:
    # a help class that contains all the possible post types in the social network
    TEXT = "Text"
    IMAGE = "Image"
    SALE = "Sale"


class PostFactory:
    # post factory class that implements the factory design pattern, there are multiple post type
    # and maybe in the future there will be even more, we want a simple instance producer that
    # when specifying post type and it's details, will create for us an instance to this post he made
    # for this scenario, when having few subclasses, we want to use the factory design pattern fot instances creation
    def create_post(self, user, post_type, *args):
        # the factory method that with given post details, returns an instance of this specific post's subclass
        if post_type == PostType.TEXT:
            return TextPost(user, *args)
        elif post_type == PostType.IMAGE:
            return ImagePost(user, *args)
        elif post_type == PostType.SALE:
            return SalePost(user, *args)
        else:
            raise ValueError("Invalid post type")


class TextPost:
    # post subclass that describe a text-only post
    def __init__(self, user, text):
        self._user = user
        self._text = f"{user.getusername()} published a post:\n\"{text}\"\n"
        self._likes = []  # list of all the users liked this post
        self._comments = []  # list of all the users and the comments commented on this post

    def like(self, user):
        # method that notifies the user uploaded this post that he got a new like
        self._likes.append(user)
        self._user.notifylike(self, user)

    def comment(self, user, text):
        # method that notifies the user uploaded this post that he got a new comment
        self._comments.append((user, text))
        self._user.notifycomment(self, user, text)

    def getUser(self):
        # method that returns the user uploaded this post
        return self._user

    def __str__(self):
        # method that returns the text contents of this post
        return self._text


class ImagePost:
    # post subclass that describe an image post
    def __init__(self, user, image):
        self._user = user
        self._image = image
        self._likes = []  # list of all the users liked this post
        self._comments = []  # list of all the users and the comments commented on this post

    def like(self, user):
        # method that notifies the user uploaded this post that he got a new like
        self._likes.append(user)
        if self._user.getusername != user.getusername:
            self._user.notifylike(self, user)

    def comment(self, user, text):
        # method that notifies the user uploaded this post that he got a new comment
        self._comments.append((user, text))
        self._user.notifycomment(self, user, text)

    def display(self):
        # method that displays the image uploaded in this post
        print(f"Shows picture")
        imag = Image.open(self._image)
        plt.imshow(imag)
        plt.show()

    def getUser(self):
        # method that returns the user uploaded this image
        return self._user

    def __str__(self):
        # method that returns a text describes who posted this picture
        return f"{self._user.getusername()} posted a picture\n"


class SalePost:
    # post subclass that describe a sale post
    def __init__(self, user, product, price, location):
        self._user = user
        self._product = product
        self._price = price
        self._location = location
        self._likes = []  # list of all the users liked this post
        self._comments = []  # list of all the users and the comments commented on this post
        self._sold = False  # false if not sold yet and true if already got sold
        self._text = f"{user.getusername()} posted a product for sale:\nFor sale! {product}, price: {price}, pickup from: {location}"

    def like(self, user):
        # method that notifies the user uploaded this post that he got a new like
        self._likes.append(user)
        self._user.notifylike(self, user)

    def comment(self, user, text):
        # method that notifies the user uploaded this post that he got a new comment
        self._comments.append((user, text))
        self._user.notifycomment(self, user, text)

    def discount(self, amount, password):
        # method that updates this sale post with a percentage discount on the price of this product
        # the method makes sure that the discount is made by the owner of the sale by asking him to enter his password
        if password == self._user.getpassword():
            self._price = self._price - (amount / 100 * self._price)
            name = self._user.getusername()
            print(f"Discount on {name} product! the new price is: {self._price}")

    def sold(self, password):
        # method that updates the post with a 'sold' state
        if password == self._user.getpassword():
            self._sold = True
            name = self._user.getusername()
            print(f"{name}'s product is sold")
            self._text = (f"{self._user.getusername()} posted a product for sale:\nSold! {self._product},"
                          f" price: {self._price}, pickup from: {self._location}\n")

    def getUser(self):
        # method that returns the user uploaded this sale
        return self._user

    def __str__(self):
        # method that returns the textual description of this sale post
        return self._text
