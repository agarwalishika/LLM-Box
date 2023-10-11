def calculate_embedding(value):
        return len(value)

class VectorDatabase:
    def __init__(self):
        self.vdb_pairs = {}
        self.original_data = {}

    def add_item(self, key, value):
        # Calculate the embedding based on the length of the string
        embedding = calculate_embedding(value)
        self.vdb_pairs[key] = embedding
        self.original_data[key] = value

    def get_embedding(self, key):
        if key in self.vdb_pairs:
            return self.vdb_pairs[key]
        else:
            return None
    
    def get_original_data(self, key):
        return self.original_data[key]
    
    def get_vdb_pairs(self, key):
        return self.vdb_pairs[key]

    def find_nearest(self, query_embedding):
        # Find the key with the closest embedding to the query_embedding
        min_distance = float('inf')
        nearest_key = None
        for key, embedding in self.vdb_pairs.items():
            distance = abs(embedding - query_embedding)
            if distance < min_distance:
                min_distance = distance
                nearest_key = key
        return nearest_key

# Example usage
if __name__ == "__main__":
    db = VectorDatabase()

    # Add items to the database
    db.add_item("item1", "Hello")
    db.add_item("item2", "World")
    db.add_item("item3", "Python")

    # Query for an embedding
    query_embedding = calculate_embedding("Goodbye")

    # Find the nearest item
    nearest_key = db.find_nearest(query_embedding)

    if nearest_key is not None:
        print(f"The nearest item to the query is {nearest_key}")
    else:
        print("No matching item found.")
