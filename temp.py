from src.knowledge_store import ChromaVectorStore, get_embedding_model, ingest_file

#ingest_file('D:\\Workspace\\AI.ETL.Agent\\src\\knowledge_store\\content\\dummies-databricks.pdf')

embedding_model = get_embedding_model()

embedding = embedding_model.embed_query("databricks")

vector_store = ChromaVectorStore(
    collection_name="ai_etl_agent"
)

print(vector_store.query_vector(embedding, top_k=5))