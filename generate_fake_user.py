import faker
import random

fake = faker.Faker()
for n in range(4, 500):
    id = n
    username = random.choice(["017", "018", "019", "015"]) + str(
        fake.unique.pydecimal(min_value=10000000, max_value=99999999, right_digits=0, positive=True)
    )
    # password = 123456
    password_hash = "sha256$g0cb3gG1kfuzOslu$6a4b80c5bccbd75065c4de22721149e8305833d0400a5d9f76ee5bcf7bb6db84"
    fullname = fake.unique.name()
    age = "1y"
    sex = random.choice(["M", "F", "O"])
    blood = random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-", "U"])
    reference = fake.unique.name()
    email = (
        fullname.replace(" ", random.choice(["-", ".", "_"])).lower()
        + "@"
        + random.choice(["yahoo.com", "hotmail.com", "gmail.com", "live.com"])
    )
    address = fake.unique.address().replace("\n", ", ")[:128]
    avatar = ""
    analysis = ""
    case_photo_1 = ""
    case_photo_2 = ""
    case_photo_3 = ""
    case_photo_4 = ""
    admin = 0
    active = 1
    author = 1
    created_at = fake.date()
    modified_at = ''
    record = f"{id}\t{username}\t{password_hash}\t{fullname}\t{age}\t{sex}\t{blood}\t{reference}\t{email}\t{address}\t{avatar}\t{analysis}\t{case_photo_1}\t{case_photo_2}\t{case_photo_3}\t{case_photo_4}\t{admin}\t{active}\t{author}\t{created_at}\t{modified_at}"
    print(record)
