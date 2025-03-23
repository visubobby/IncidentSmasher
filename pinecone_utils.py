

# Function to insert data into Pinecone
def insert_data_to_pinecone(df, embeddings):
    vectors = []
    for _, row in df.iterrows():
        # Combine relevant fields into a single text for embedding
        text = f"Title: {row['title']}\nDescription: {row['description']}\nResolution: {row['resolution_notes']}"
        # Generate embedding
        embedding = embeddings.embed_query(text)
        # Store metadata
        metadata = {
            "incident_id": row["incident_id"],
            "title": row["title"],
            "description": row["description"],
            "priority": row["priority"],
            "status": row["status"],
            "affected_app": row["affected_app"],
            "affected_microservice": row["affected_microservice"],
        }
        # Append to vectors
        vectors.append((row["incident_id"], embedding, metadata))
    # Upsert vectors into Pinecone
    index.upsert(vectors)