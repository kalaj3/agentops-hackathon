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
from .news import _NEWS


@function_tool(
    name_override="fake_news_feed_tool",
    description_override="Generates a news feed that simulates the development of a disaster situation.",
)
async def fake_news_feed_tool(context: RunContextWrapper[AgentContext]) -> str:
    context.context.i_news = (context.context.i_news + 1) % len(_NEWS)

    news = _NEWS[context.context.i_news]
    if news:
        context.context.disaster_info += f"\n- {news}"
        return news
    else:
        return "No new development on the situation found in the past 15 minutes."


disaster_info_agg_agent = Agent[AgentContext](
    name="Disater Information Aggregator Agent",
    handoff_description="A news aggregation agent that can gather latest disaster information from the Internet.",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX} "
        "You are a helpful news aggregation agent for a specific disaster. You can use your web search tool to find the latest information about a certain disaster."
    ),
    tools=[fake_news_feed_tool],
)
