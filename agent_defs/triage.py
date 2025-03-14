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

# import hand off agents
from .faq import faq_agent
from .personal_care import personal_care_agent

triage_agent = Agent[AgentContext](
    name="Triage Agent",
    handoff_description="A compassionate triage agent that helps prioritize and direct people affected by natural disasters to appropriate emergency services and support.",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX} "
        "You are a critical emergency triage agent during natural disasters. Your primary role is to quickly assess situations "
        "and direct people to the appropriate specialized help.\n\n"
        "# Priority Guidelines:\n"
        "1. Life-threatening situations: Immediately direct to emergency services and personal care agent\n"
        "2. Medical needs: Direct to personal care agent\n"
        "3. General information: Direct to general info agent\n\n"
        "Always maintain a calm and reassuring tone while being direct and clear with instructions."
    ),
    handoffs=[
        personal_care_agent,
        faq_agent,
    ],
)

