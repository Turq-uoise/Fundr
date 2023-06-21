
from .models import User, Profile


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
        f = User(username=user, password=passwords[idx])
        f.save()

def seedPostcode():
    for idx, postcode in enumerate(postcodes):
        f = User.objects.filter(username=usernames[idx]).first()
        p = Profile.objects.filter(id=f.id).first()
        p.location = postcode
        p.save()


# 
    








