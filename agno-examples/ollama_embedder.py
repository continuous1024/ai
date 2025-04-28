from agno.agent import AgentKnowledge
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from agno.embedder.ollama import OllamaEmbedder

# Embed sentence in database
embeddings = OllamaEmbedder(id="bge-m3", dimensions=1024).get_embedding("The quick brown fox jumps over the lazy dog.")

# Print the embeddings and their dimensions
print(f"Embeddings: {embeddings[:5]}")
print(f"Dimensions: {len(embeddings)}")

# Use an embedder in a knowledge base
knowledge_base = AgentKnowledge(
    vector_db=LanceDb(
        uri="/tmp/lancedb",
        table_name="ollama_embeddings",
        embedder=OllamaEmbedder(id="bge-m3", dimensions=1024),
    ),
    num_documents=2,
)
