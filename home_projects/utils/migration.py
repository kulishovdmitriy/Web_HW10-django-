import os
import django

from pymongo import MongoClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home_projects.settings')
django.setup()

from quotes.models import Quote, Tag, Author

client = MongoClient(
    'mongodb+srv://dmitriyykulishov:<password>@mongodb.dtj8cur.mongodb.net/?retryWrites=true&w=majority&appName=mongoDB'
)
db = client.mongodb

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))

    if not exist_quote:
        author = db.authors.find_one({'_id': quote['author']})
        author_name = quote['author']
        a = Author.objects.filter(fullname=author_name).first()
        if a is not None:
            q = Quote.objects.create(
                quote=quote['quote'],
                author=a
            )
            for tag in tags:
                q.tags.add(tag)
        else:
            print(f"Author '{author_name}' not found.")
