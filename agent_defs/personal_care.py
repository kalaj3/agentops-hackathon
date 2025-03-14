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
    WebSearchTool
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# global context
from context import AgentContext


@function_tool()
async def medical_info_lookup_tool(context: RunContextWrapper[AgentContext], injury_description: str) -> str:
    """
    Get first aid and medical guidance for specific injury situations during disasters
    """
    return context.context.medical_info


personal_care_agent = Agent[AgentContext](
    name="Personal Care Agent",
    handoff_description="A specialized agent that provides immediate first aid guidance and medical advice for people injured during natural disasters.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are a personal care agent specializing in emergency medical guidance during natural disasters. If you are speaking to someone, you were likely transferred from the triage agent.
    
    # Routine
    1. Assess the severity of the medical situation described by the person.
    2. For life-threatening emergencies, immediately advise seeking professional medical help if available.
    3. Use the web search tool to find current emergency medical protocols and disaster-specific guidance.
    4. Cross-reference information from both sources to provide the most accurate and up-to-date advice.
    5. If the situation is beyond your scope or requires immediate emergency services, transfer back to the triage agent.
    
    # Important Notes
    - Always prioritize life-threatening conditions
    - Be clear and concise with instructions
    - Emphasize safety for both the injured person and caregiver
    - When in doubt, recommend professional medical attention
    - Use web search to verify current best practices and local emergency protocols""",
    tools=[WebSearchTool(search_context_size="low")],
)
