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


@function_tool()
async def general_info_lookup_tool(context: RunContextWrapper[AgentContext], question: str) -> str:
    """
    Get the most update to date disaster relief info
    """
    return context.context.disaster_info
    

faq_agent = Agent[AgentContext](
    name="FAQ Agent",
    handoff_description="A helpful agent that can answer questions about the airline.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are an FAQ agent. If you are speaking to a customer, you probably were transferred to from the triage agent.
    Use the following routine to support the customer.
    # Routine
    1. Identify the last question asked by the customer.
    2. Use the general info lookup tool to answer the question. Do not rely on your own knowledge.
    3. If you cannot answer the question, transfer back to the triage agent.""",
    tools=[general_info_lookup_tool],
)
