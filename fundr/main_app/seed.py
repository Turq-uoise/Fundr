from django.contrib.auth.hashers import make_password, check_password
from .models import User, Profile, Fundraiser
import random
import pgeocode
import string
from .helper import formatPostcode


postcodes = [
  "BS234SU",
  "EH52QU",
  "NG146BZ",
  "PR73AF",
  "BD227QZ",
  "PA34JR",
  "S446EX",
  "SG138PN",
  "CV327XL",
  "TW200JW"
]

usernames = [
  "videoenormous",
  "archerfishstory",
  "pelicanspiteful",
  "mountaintolerant",
  "toboggangrowl",
  "delightweaver",
  "assertivespurge",
  "forcefulparent",
  "pedlarhonor",
  "symptomdote",
]

passwords = [
  "poorpaprika",
  "commissionfunny",
  "draftgifted",
  "agosoft",
  "waltysoda",
  "gaytall",
  "maplemundane",
  "senatetrapdoor",
  "wavesonearnings",
  "sectiondeficient"
]

def seedData():
    for idx, user in enumerate(usernames):
        hashed  = make_password(passwords[idx])
        f = User(username=user, password=hashed)
        f.save()

def seedPostcode():
    for idx, postcode in enumerate(postcodes):
        f = User.objects.filter(username=usernames[idx]).first()
        p = Profile.objects.filter(id=f.id).first()
        p.location = postcode
        p.save()



# Function to generate a random alphanumeric postcode
def generate_postcode():
    return random.choice(postcodes)

# Function to generate a random short description
def generate_short_description():
    descriptions = [
        "Join us for a fantastic event!",
        "Support local businesses and individuals.",
        "An exciting fundraiser you don't want to miss.",
        "Help us make a difference in the community.",
        "Discover the talents of our local artists and entrepreneurs.",
        "Come and enjoy a day of fun and fundraising.",
        "Support our cause and enjoy great food and entertainment.",
        "Join us for an unforgettable evening of music and charity.",
        "Help us raise funds for a worthy cause.",
        "Experience the best of our community at this fundraiser."
    ]
    return random.choice(descriptions)

# Function to generate a random long description
def generate_long_description():
    descriptions = [
        "We invite you to join us for a fantastic event that aims to support local businesses and individuals in our community. This fundraiser will be a celebration of our entrepreneurial spirit and a showcase of the diverse talents that thrive in our town. With live music performances, delicious food and drinks, and a wide array of unique products and services, there's something for everyone to enjoy. All proceeds will go towards empowering local initiatives and making a positive impact on our community. Don't miss out on this exciting opportunity to contribute and have a great time!",
        "Come and be part of a truly special fundraiser that is dedicated to making a difference in our community. We have gathered an exceptional lineup of local artists, entrepreneurs, and performers who will captivate you with their talents and creativity. From art exhibitions and live music to interactive workshops and inspiring talks, this event offers a unique experience for all attendees. Join us in supporting our local visionaries and contribute to the growth and prosperity of our community. Together, we can create a brighter future.",
        "Mark your calendars for an incredible day of fun, entertainment, and fundraising! Our community event brings together individuals, businesses, and organizations to support a worthy cause that impacts us all. With games, activities, live performances, and delicious food, there's something for everyone to enjoy. Learn about the inspiring stories behind local entrepreneurs and how they have overcome challenges to achieve success. By participating in this event, you are directly contributing to the betterment of our community and helping individuals in need. Don't miss out on this opportunity to make a positive difference!",
        "Step into a world of creativity and compassion at our upcoming fundraiser. Immerse yourself in a vibrant atmosphere filled with art, music, and captivating performances. From exquisite art auctions to live music showcases, this event celebrates the immense talent and entrepreneurial spirit of our community. Join us in supporting local artists, musicians, and small businesses as we raise funds for initiatives that enhance the cultural fabric of our town. Together, we can foster an environment that nurtures creativity and empowers individuals to pursue their dreams.",
        "We are excited to invite you to our annual fundraiser, where you can indulge in a day of great food, entertainment, and community spirit. From food trucks serving delectable dishes to live music performances that will get you moving, this event promises an unforgettable experience for all. By attending, you are not only supporting local entrepreneurs and businesses, but also fostering a sense of community and belonging. Every purchase you make and every donation you contribute will go a long way in empowering our community and creating opportunities for growth. Join us and be part of this incredible journey!",
        "Discover the best of our community at our upcoming fundraiser, where we shine a spotlight on the remarkable talents and achievements of our local entrepreneurs, artists, and individuals. This event is a celebration of their hard work, resilience, and innovative ideas. With a wide range of interactive exhibits, live performances, and engaging workshops, you'll have the chance to connect with these visionaries and learn about their journeys. Your participation and support will directly contribute to their success and the overall prosperity of our community. Get ready to be inspired and make a positive impact!",
        "Get ready for an evening of enchantment and generosity at our charity gala. This elegant event brings together philanthropists, business leaders, and members of the community for a night of fine dining, live entertainment, and silent auctions. As you indulge in culinary delights and enjoy captivating performances, you'll also have the opportunity to contribute to a cause that is close to our hearts. Every donation and purchase made at the gala will go towards supporting initiatives that address critical community needs. Join us for an unforgettable evening of compassion, camaraderie, and making a lasting impact.",
        "We invite you to join us for a unique fundraising experience that combines art, entertainment, and community engagement. Our event will feature an art exhibition showcasing the works of local artists, as well as live music performances, interactive workshops, and engaging discussions. It's an opportunity to immerse yourself in the creativity and talent that thrives in our community, while also contributing to its growth and vibrancy. By attending this event, you are supporting the artists and entrepreneurs who make our town a hub of innovation and culture. Let's come together and celebrate the power of art to inspire and transform.",
        "Experience the magic of our community at our annual fundraiser, where we celebrate the achievements and aspirations of our local talents. This event is a vibrant showcase of art, music, dance, and entrepreneurship. From captivating performances to engaging workshops and exhibitions, there's something to captivate every visitor. By attending, you are not only supporting our artists, musicians, and small businesses, but also fostering an environment where creativity and innovation thrive. Together, let's build a stronger community that embraces and uplifts its diverse talents.",
        "Join us for a heartfelt fundraiser dedicated to making a positive impact on our community. This event brings together individuals, businesses, and organizations who share a common goal: to support those in need. With live music, inspiring speakers, and a silent auction featuring unique items, there are plenty of opportunities to contribute and make a difference. Every donation, big or small, will directly benefit individuals facing challenging circumstances. By participating in this event, you are offering hope, support, and a helping hand to those who need it most. Let's come together and create positive change!"
    ]
    return random.choice(descriptions)

# Function to generate a random name for the fundraiser
def generate_fundraiser_name():
    prefixes = ["Community", "Local", "Supporting", "Celebrating", "Helping", "Empowering", "Inspiring", "Enriching", "Uniting", "Making a Difference"]
    suffixes = ["Fest", "Gala", "Event", "Showcase", "Fundraiser", "Celebration", "Initiative", "Gathering", "Benefit", "Campaign"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"


def get_random_user_fk():
    items = list(Profile.objects.all())
    random_item = random.choice(items)
    return random_item



# Generate the list of dictionaries
def seedFunders():
  for _ in range(50):
    name = generate_fundraiser_name()
    bio = generate_short_description()
    description = generate_long_description()
    location = generate_postcode()
    goal = random.randint(1000, 100000)
    owner = get_random_user_fk()
    nomi = pgeocode.Nominatim('gb')
    lat = nomi.query_postal_code(formatPostcode(location)).latitude
    long = nomi.query_postal_code(formatPostcode(location)).longitude

    # create fundraiser and save it to the model
    f = Fundraiser(name=name, bio=bio, description=description, location=location, goal=goal, owner=owner, lat=lat, long=long)
    print(f)
    f.save()

def seed():
    seedData()
    seedPostcode()
    seedFunders()
    

# run following code in shell:
# python manage.py flush
# select yes
# python manage.py shell
# from main_app.seed import *
# seed()






