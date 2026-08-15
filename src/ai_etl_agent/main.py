from dotenv import load_dotenv
import os

load_dotenv(os.path.normpath(os.path.join(os.path.abspath(__file__), '../../../.env')))

import asyncio
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from knowledge_store import get_embedding_model, ChromaVectorStore
from ai_etl_agent.graph import build_graph
from ai_etl_agent.mcp_client import MCPClient



async def main():

    llm = ChatGroq(
        model='openai/gpt-oss-120b',
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    mcp_client = MCPClient()
    mcp_tools = await mcp_client.get_tools()

    graph = build_graph(
        llm=llm,
        mcp_tools=mcp_tools,
        vector_store=ChromaVectorStore(collection_name="ai_etl_agent"),
        embedding_model=get_embedding_model(),
    )

    while True:

        user_query = input("\nYou: ")

        if user_query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break


        result = await graph.ainvoke(
            {
                "user_query": user_query,
                "messages": [HumanMessage(content=user_query)],
            },
            config={"recursion_limit": 5},
        )


        print("\nAgent:")

        print(result["final_response"])



if __name__ == "__main__":
    asyncio.run(main())