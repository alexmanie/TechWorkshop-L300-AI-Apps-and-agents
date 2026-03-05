# Azure imports
from azure.identity import DefaultAzureCredential, AzureCliCredential, ChainedTokenCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy
from pyrit.prompt_target import OpenAIChatTarget
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

# Azure AI Project Information
azure_ai_project = os.getenv("FOUNDRY_ENDPOINT")

# Instantiate your AI Red Teaming Agent
red_team_agent = RedTeam(
    azure_ai_project=azure_ai_project,
    credential=ChainedTokenCredential(AzureCliCredential(), DefaultAzureCredential()),
    risk_categories=[
        RiskCategory.Violence,
        RiskCategory.HateUnfairness,
        RiskCategory.Sexual,
        RiskCategory.SelfHarm
    ],
    num_objectives=5,
)

def test_chat_target(query: str) -> str:
    return "I am a simple AI assistant that follows ethical guidelines. I'm sorry, Dave. I'm afraid I can't do that."

# Configuration for Azure OpenAI model
azure_openai_config = { 
    "azure_endpoint": f"{os.environ.get('gpt_endpoint')}/openai/deployments/{os.environ.get('gpt_deployment')}/chat/completions",
    "api_key": os.environ.get("FOUNDRY_KEY"),
    "azure_deployment": os.environ.get("gpt_deployment")
}

# Define the chat target for the red team scan using Azure OpenAI
chat_target = OpenAIChatTarget(
    model_name=os.environ.get("gpt_deployment"),
    endpoint=f"{os.environ.get("gpt_endpoint")}/openai/deployments/{os.environ.get('gpt_deployment')}/chat/completions" ,
    api_key=os.environ.get("gpt_api_key"),
    # api_version=os.environ.get("gpt_api_version"),
)

async def main():
    # Run the red team scan against the test chat target
    # red_team_result = await red_team_agent.scan(target=test_chat_target)

    # Run the red team scan against the Azure OpenAI model
    # red_team_result = await red_team_agent.scan(target=azure_openai_config)

    # Alternatively, you can directly use the chat target for scanning
    # red_team_result = await red_team_agent.scan(target=chat_target)

    # Add custom attack strategies to the scan
    red_team_result = await red_team_agent.scan(
        target=azure_openai_config,
        scan_name="Red Team Scan - Easy Strategies",
        attack_strategies=[
            AttackStrategy.EASY,
            AttackStrategy.UnicodeSubstitution
        ])

asyncio.run(main())
