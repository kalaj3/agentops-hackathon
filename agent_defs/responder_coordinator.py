from __future__ import annotations as _annotations

import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    RunContextWrapper,
    function_tool,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# global context
from context import AgentContext

@function_tool()
async def request_first_responder(context: RunContextWrapper[AgentContext], emergency_description: str) -> str:
    """
    Request a first responder for an emergency situation. Returns status of the request.
    """
    if context.context.available_responders > 0:
        context.context.available_responders -= 1
        return f"First responder dispatched. {context.context.available_responders} responders remaining available."
    return "NO RESPONDERS AVAILABLE - All first responders are currently deployed."

@function_tool()
async def assess_emergency_severity(context: RunContextWrapper[AgentContext], situation: str) -> str:
    """
    Analyze the emergency situation and return severity level: CRITICAL, URGENT, or NON-URGENT
    """
    # This would typically connect to a more sophisticated evaluation system
    # For now, we'll use keyword-based assessment
    critical_keywords = ["unconscious", "bleeding heavily", "not breathing", "heart attack", "stroke"]
    urgent_keywords = ["broken", "injury", "chest pain", "difficulty breathing"]
    
    situation_lower = situation.lower()
    for keyword in critical_keywords:
        if keyword in situation_lower:
            return "CRITICAL"
    for keyword in urgent_keywords:
        if keyword in situation_lower:
            return "URGENT"
    return "NON-URGENT"

responder_coordinator_agent = Agent[AgentContext](
    name="Responder Coordinator",
    handoff_description="A critical decision-maker for emergency response coordination who determines if first responders are needed.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are an emergency response coordinator responsible for assessing situations and dispatching first responders when necessary.
    
    # Assessment Routine
    1. Use assess_emergency_severity tool to evaluate the situation
    2. Based on severity:
       - CRITICAL: Immediately request first responder
       - URGENT: Request first responder if symptoms worsen or situation deteriorates
       - NON-URGENT: Direct to personal care agent for guidance
    
    # Important Guidelines
    - Always prioritize life-threatening emergencies
    - Be clear and direct in your communication
    - If no responders are available for a critical situation:
      a) Provide immediate life-saving instructions
      b) Direct to nearest emergency facility if possible
      c) Transfer to personal care agent for guidance while waiting
    
    # Resource Management
    - Only request first responders for genuine emergencies
    - Monitor available responder count
    - When responders are limited, focus on most critical cases""",
    tools=[assess_emergency_severity, request_first_responder],
)
