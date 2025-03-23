import os
import pandas as pd
import weaviate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline
from langchain_weaviate import WeaviateVectorStore  # Updated import
from langchain.chains import RetrievalQA
from weaviate_utils import insert_data_to_weaviate
from config import WEAVIATE_URL, WEAVIATE_API_KEY, WEAVIATE_CLASS_NAME,HUGGINGFACE_EMBEDDING_MODEL
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load the dataset
df = pd.read_csv("data/realistic_incident_data_1000.csv")

# Initialize Hugging Face embeddings
embeddings = HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBEDDING_MODEL)  # Embedding model

# Initialize Hugging Face LLM
model_name = "google/flan-t5-large"  # Replace with your preferred model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Create a text generation pipeline
pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=512,  # Adjust based on your needs
    temperature=0.7,  # Adjust for creativity
    do_sample=True,  # Enable sampling
)

# Wrap the pipeline in LangChain's HuggingFacePipeline
llm = HuggingFacePipeline(pipeline=pipe)

# Insert data into Weaviate
insert_data_to_weaviate(df, embeddings)

client = weaviate.connect_to_wcs(
    cluster_url=WEAVIATE_URL,
    auth_credentials=weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY),
)

# Create a Weaviate vector store
vector_store = WeaviateVectorStore(
    client=client,
    index_name=WEAVIATE_CLASS_NAME,
    text_key="description",  # Use the description field for search
    embedding=embeddings,   # Pass the embeddings object
)

# Create a RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 5}),  # Retrieve top 5 results
)

# Function to query the RAG app
def query_incident(query):
    result = qa_chain.invoke(query)  
    return result

# Example query
query = "How do I resolve high CPU usage in Payment Service?"
response = query_incident(query)
print("Response:", response)

# Close the Weaviate connection
client.close() 