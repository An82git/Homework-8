from models import Authors, Quotes

from redis_lru import RedisLRU
import redis
import connect


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

def search_tag(values: list) -> list:
    rezult = Quotes.objects(tags__all=values).all()
        
    if not rezult:
        tags = []
        tags_set = []
        tags_list = [ob.tags for ob in Quotes.objects().all()]
        for l in tags_list:
            for ob in l:
                tags_set.append(ob)
        
        tags_set = set(tags_set)
        for tag in tags_set:
            for value in values:
                if value in tag:
                    tags.append(tag)
        
        rezult = Quotes.objects(tags__in=tags).all()
    return rezult

def search_name(values: list) -> list:
    authors = [ob.id for ob in Authors.objects(fullname__icontains=values[0])]
    return Quotes.objects(author__in=authors).all()

@cache
def data_search(request: str):
    print(True)
    request = [ob.strip() for ob in request.split(":")]
    values = [ob.strip() for ob in request[1].split(",")] if len(request) > 1 else []
    command = request[0].lower()
    
    if command == "tag":
        return data_pars(search_tag(values))
    elif command == "name":
        return data_pars(search_name(values))
    elif command == "exit":
        return "False"
    else:
        return "There is no such team."

def data_pars(data) -> str:
    data_list = [ob.to_mongo().to_dict() for ob in data]
    string_data = "\n"

    for dic in data_list:
        string_dic = "{\n"

        for key in dic:
            string_dic += f"{key}: {dic[key]}\n"
        string_data += f"{string_dic}{'}'}\n"

    return string_data
   

if __name__ == "__main__":
    while True:
        request = input("Enter the 'command: value': ")
        data = data_search(request)
        
        if data == "False":
            break
        else:
            print(data)
                    