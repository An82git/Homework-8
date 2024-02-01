from models import Authors, Quotes
import json
import connect


authors_path = "json-file/authors.json"
quotes_path = "json-file/qoutes.json"


def load_json(path) -> None:
    with open(path, "br") as file:
        rezult = json.load(file)
    return rezult

def create_authors(data: dict) -> Authors:
    return Authors(
        fullname = data["fullname"],
        born_date = data["born_date"],
        born_location = data["born_location"],
        description = data["description"]
        )

def create_quotes(data: dict, author: Authors) -> Quotes:
    return Quotes(
        tags = data["tags"],
        author = author,
        quote = data["quote"]
        )

if __name__ == "__main__":
    authors = load_json(authors_path)
    quotes = load_json(quotes_path)

    for author in authors:
        create_authors(author).save()

    for quote in quotes:
        author = Authors.objects(fullname = quote["author"]).first()
        create_quotes(quote, author).save()
