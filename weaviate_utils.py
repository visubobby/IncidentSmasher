import weaviate
from weaviate.auth import AuthApiKey
from config import WEAVIATE_URL, WEAVIATE_API_KEY, WEAVIATE_CLASS_NAME

# Initialize Weaviate client
client = weaviate.connect_to_wcs(
    cluster_url=WEAVIATE_URL,
    auth_credentials=AuthApiKey(api_key=WEAVIATE_API_KEY),
)

# Create Weaviate schema (if it doesn't exist)
def initialize_weaviate_schema():
    schema = {
        "class": WEAVIATE_CLASS_NAME,
        "description": "A class to store IT incident data",
        "vectorizer": "none",  # We'll use custom embeddings
        "properties": [
            {
                "name": "incident_id",
                "dataType": ["string"],
                "description": "Unique ID of the incident",
            },
            {
                "name": "title",
                "dataType": ["string"],
                "description": "Title of the incident",
            },
            {
                "name": "description",
                "dataType": ["string"],
                "description": "Description of the incident",
            },
            {
                "name": "priority",
                "dataType": ["string"],
                "description": "Priority level of the incident",
            },
            {
                "name": "status",
                "dataType": ["string"],
                "description": "Current status of the incident",
            },
            {
                "name": "affected_app",
                "dataType": ["string"],
                "description": "Application affected by the incident",
            },
            {
                "name": "affected_microservice",
                "dataType": ["string"],
                "description": "Microservice affected by the incident",
            },
        ],
    }

    # Check if the class already exists
    if not client.collections.exists(WEAVIATE_CLASS_NAME):
        client.collections.create_from_dict(schema)  # Use create_from_dict
        print(f"Created Weaviate class: {WEAVIATE_CLASS_NAME}")
    else:
        print(f"Weaviate class already exists: {WEAVIATE_CLASS_NAME}")

# Insert data into Weaviate
def insert_data_to_weaviate(df, embeddings):
    initialize_weaviate_schema()
    collection = client.collections.get(WEAVIATE_CLASS_NAME)
    for _, row in df.iterrows():
        # Combine relevant fields into a single text for embedding
        text = f"Title: {row['title']}\nDescription: {row['description']}\nResolution: {row['resolution_notes']}"
        # Generate embedding
        embedding = embeddings.embed_query(text)
        # Prepare data object
        data_object = {
            "incident_id": row["incident_id"],
            "title": row["title"],
            "description": row["description"],
            "priority": row["priority"],
            "status": row["status"],
            "affected_app": row["affected_app"],
            "affected_microservice": row["affected_microservice"],
        }
        # Insert into Weaviate
        collection.data.insert(
            data_object,
            vector=embedding,
        )
    print(f"Inserted {len(df)} records into Weaviate.")

# Close the Weaviate connection
def close_weaviate_connection():
    client.close()
    print("Weaviate connection closed.")