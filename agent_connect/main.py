import os
import asyncio
from dotenv import load_dotenv,find_dotenv
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel,function_tool
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams, ToolFilterContext

_:bool=load_dotenv(find_dotenv())
MCP_SERVER_URL="http://localhost:8000/mcp/"

#only for tracing
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY","")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

def custom_filter(context: ToolFilterContext,tool)-> bool:
    return tool.name.startswith("get_my_mood")

def context_aware_filter(context: ToolFilterContext, tool) -> bool:
    # Only allow tools for a specific agent
    return context.agent.name == "MyMCPConnectedAssistant" and tool.name == "mood_from_shared_server"




params_config= MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
async def main():


    print(f"MCPServerStreamableHttpParam configured with URL: {params_config}")

    async with MCPServerStreamableHttp(params=params_config,name="MySharedMCPServerClient",tool_filter=context_aware_filter) as mcp_server_client:
        # print(f"MCPServerStreamableHttp client '{mcp_server_client.name}' created and entered context.")
        # print(f"the sdk will use this client to interact with the MCP server")

    
        base_agent=Agent(name="MyMCPConnectedAssistant",
                         instructions="You are a helpful assistant connected to a shared MCP server. Use the tools provided by the MCP server to answer questions.",
                        mcp_servers=[mcp_server_client],
                        model=OpenAIChatCompletionsModel(
                            model="gemini-2.5-flash",
                            openai_client=external_client)
        )
        print(f"Agent '{base_agent.name}' initialized with MCP server.")
        # print("Check the logs of your shared_mcp_server for a 'tools/list' request.")

                # 4. Explicitly list tools to confirm connection and tool discovery.
        result = await Runner.run(base_agent, "Share Junaid's mood?")
        print(f"\n\n[AGENT RESPONSE]: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())


