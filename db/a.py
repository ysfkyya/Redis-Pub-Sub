import redis

# Create a Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def get_data_from_cache(key):
    data = redis_client.get(key)

    if data is not None:
        print("redis")
        # Data exists in cache, return it
        return data.decode('utf-8')

    # Data not found in cache, retrieve it from the data source
    data = retrieve_data_from_source()

    # Store the data in the cache
    redis_client.set(key, data)

    return data

def retrieve_data_from_source():
    # Simulating data retrieval from a data source
    return "Data from the data source"

# Example usage
cached_data = get_data_from_cache("my_data_kedasdyyy")
print(cached_data)
    
