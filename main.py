from __future__ import annotations as _annotations

import asyncio
import random
import uuid

from pydantic import BaseModel

from dotenv import load_dotenv
import os
import agentops

from agents import (
    Agent,
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    RunContextWrapper,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    TResponseInputItem,
    function_tool,
    handoff,
    trace,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# global context
from context import AgentContext

# import agents
from agent_defs.triage import triage_agent
from agent_defs.faq import faq_agent
from agent_defs.personal_care import personal_care_agent
from agent_defs.responder_coordinator import responder_coordinator_agent

# Load the environment variables for the script
load_dotenv()

# Initialize the agentops module
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
agentops.init(api_key=AGENTOPS_API_KEY)

# Update agent instructions with handoff guidelines
faq_agent.instructions = f"""{faq_agent.instructions}
    # Additional Handoff Guidelines
    - If user mentions any injuries or medical concerns, transfer to personal_care_agent
    - If situation seems critical or life-threatening, transfer to responder_coordinator_agent
    - For complex disaster coordination needs, transfer to triage_agent"""

personal_care_agent.instructions = f"""{personal_care_agent.instructions}
    # Additional Handoff Guidelines
    - If situation is life-threatening or requires immediate response, transfer to responder_coordinator_agent
    - For general disaster information, transfer to faq_agent
    - For complex coordination needs, transfer to triage_agent"""

responder_coordinator_agent.instructions = f"""{responder_coordinator_agent.instructions}
    # Additional Handoff Guidelines
    - When no responders are available, transfer to personal_care_agent for first aid guidance
    - For non-urgent situations, transfer to faq_agent
    - For complex coordination or when situation changes, transfer to triage_agent"""

triage_agent.instructions = f"""{triage_agent.instructions}
    # Detailed Handoff Guidelines
    1. Life-threatening emergencies: Transfer to responder_coordinator_agent
    2. Medical needs and injuries: Transfer to personal_care_agent
    3. General disaster information: Transfer to faq_agent
    
    Always assess severity first and prioritize immediate threats to life."""

# init agent handoffs here to avoid circular imports
faq_agent.handoffs = [personal_care_agent, responder_coordinator_agent, triage_agent]
personal_care_agent.handoffs = [responder_coordinator_agent, faq_agent, triage_agent]
responder_coordinator_agent.handoffs = [personal_care_agent, faq_agent, triage_agent]
triage_agent.handoffs = [responder_coordinator_agent, personal_care_agent, faq_agent]

### RUN


async def main():
    current_agent: Agent[AgentContext] = triage_agent
    input_items: list[TResponseInputItem] = []
    context = AgentContext()

    # Normally, each input from the user would be an API request to your app, and you can wrap the request in a trace()
    # Here, we'll just use a random UUID for the conversation ID
    conversation_id = uuid.uuid4().hex[:16]

    while True:
        user_input = input("Enter your message: ")
        with trace("Disaster Relief", group_id=conversation_id):
            input_items.append({"content": user_input, "role": "user"})
            result = await Runner.run(current_agent, input_items, context=context)

            for new_item in result.new_items:
                agent_name = new_item.agent.name
                if isinstance(new_item, MessageOutputItem):
                    print(f"{agent_name}: {ItemHelpers.text_message_output(new_item)}")
                elif isinstance(new_item, HandoffOutputItem):
                    print(f"Handed off from {new_item.source_agent.name} to {new_item.target_agent.name}")
                elif isinstance(new_item, ToolCallItem):
                    print(f"{agent_name}: Calling a tool")
                elif isinstance(new_item, ToolCallOutputItem):
                    print(f"{agent_name}: Tool call output: {new_item.output}")
                else:
                    print(f"{agent_name}: Skipping item: {new_item.__class__.__name__}")
            input_items = result.to_input_list()
            current_agent = result.last_agent


if __name__ == "__main__":
    asyncio.run(main())
