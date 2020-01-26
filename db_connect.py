from pymongo import MongoClient

def get_list_of_urls(domain_name):
    mappings = []
    try:
        client = MongoClient("116.203.177.107", 27017)
        db = client["samsung_scraping"]
        mapping_collection = db["mapping"]
        mappings = mapping_collection.find(
            {
                domain_name : {
                    "$exists" : True
                }
            },
            {
                domain_name : 1,
                "_id" : 0
            }
        )
        mappings = [x[domain_name] for x in mappings if x[domain_name].upper().strip() not in ["NA","MA", ""]]
        mappings = list(set(mappings))

    except Exception as e:
        print(e)
    finally:
        if client:
            client.close()
        return mappings

def get_collection(domain_name, host):
    try:
        client = MongoClient(host, 27017)
        return client
    except:
        if client:
            client.close()
