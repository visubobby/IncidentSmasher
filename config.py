# Weaviate configuration
WEAVIATE_URL = "https://jiytwosttck1styws1aea.c0.asia-southeast1.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "7mZkRaDKCViXxbxd1Ej66ZtRXR2MFsVBqbbp"
WEAVIATE_CLASS_NAME = "Incident"                   # Weaviate class name for incidents

# Google Cloud configuration
GOOGLE_GEMINI_API_KEY = "AIzaSyBjtVo6LPQB6NYbKChyaJ_u7381bTvOnJ4"      # Your Gemini API key
GOOGLE_LLM_MODEL = "gemini-pro"        
GOOGLE_EMBEDDING_MODEL = "text-embedding-004"

# Hugging Face configuration
HUGGINGFACE_EMBEDDING_MODEL = "multi-qa-mpnet-base-dot-v1"  # Embedding model
HUGGINGFACE_LLM_MODEL = "google/flan-t5-large"                           # Text generation model

# Other settings
DATA_FILE_PATH = "data/realistic_incident_data_1000.csv"  # Path to the dataset file
LOG_DIR = "logs"  # Directory for storing logs