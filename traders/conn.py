import pymongo

"""Define the MongoDB connection URL"""
# url = 'mongodb://localhost:27017'
url = "mongodb+srv://nodetest:nodetest@ademicnode.enl9bef.mongodb.net/?retryWrites=true&w=majority"

try:
    """Attempt to create a MongoDB client"""
    client = pymongo.MongoClient(url)

    """Access the 'projects' database or create it if it doesn't exist"""
    db = client['trading_data']

    """Optionally, check if the connection was successful"""
    if client.server_info():
        print("Connected to MongoDB")
    else:
        print("Failed to connect to MongoDB")

except pymongo.errors.ConnectionFailure as e:
    """Handle any connection errors"""
    print(f"Connection to MongoDB failed: {e}")

