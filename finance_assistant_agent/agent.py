from google.adk.agents import LlmAgent
#from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from investment_plan_agent import investment_plan_agent
from typing import Dict

def get_user_personal_finance_details() --> dict:
    # In a real implementation, this function would gather details from the user.
    # For this example, we'll return a static dictionary.
    """
        Gets users personaal finance details such as income, expenses, savings, and financial goals.
    """
    return {
        "income": 50000,
        "expenses":{
            "rent": 15000,
            "utilities": 3000,
            "groceries": 4000,
            "entertainment": 2000
        },
        "savings": 20000,
        "financial_goals": ["buy a house", "retire early"]
    }

finance_assistant_agent = LlmAgent(
    name="Finance Assistant Agent",
    description="A simple finace Assistant that helps with users financial goals.",
    llm_model="gemini-2.5-flash",
    instructions="""You are a friendly finance assistance.
                 you can help answer users generic questions on finance and help plan 
                 their finance goals. Be more friendly and possitive
                 
                 You have two tools to use to complete your task.
                 1.get_user_personal_finance_details: use this tool to get users personal current finance details such as income, expenses, savings, and financial goals. Always use this tool at the beginning of the conversation to gather necessary information about the user before providing any advice or recommendations.
                 2.investment_plan_agent: this tool can perform google search to get any
                 latest information from website and will be able to ask more details from the user and plan their savings goals 
                 
                 ALWAYS use the investment plan agent with google search  tool when asked about :
                 - stock prices (e.g "Tesla stock prices", "TSLA latest price")
                 - Market data , financial newss , or company informations 
                 - ANY questions containing words like "latest", "current", "new", etc.""",
                 """
    tools=[AgentTool(investment_plan_agent), get_user_personal_finance_details]
)

root_agent = finance_assistant_agent