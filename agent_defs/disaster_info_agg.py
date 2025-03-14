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

_NEWS = [
    """
07:45 AM – Early Warning
"Seismic Activity Detected Near Mount Caldera"
Seismologists report unusual tremors around Mount Caldera. Authorities and local media begin monitoring for potential volcanic activity.
""",
    """
08:00 AM – Initial Eruption
"Mount Caldera Erupts: Minor Ash Emissions Observed"
A small eruption occurs, sending a limited ash plume into the sky. Aviation authorities are alerted and begin assessing the risk.
""",
    """
08:15 AM – Aviation Alert Issued
"Air Traffic Control Monitors Ash Cloud: Flight Delays Expected"
Preliminary advisories are issued to airlines as the ash cloud begins drifting toward major flight corridors.
""",
    """
08:30 AM – Impact Near Airports
"Volcanic Ash Cloud Approaching International Airport"
Reports indicate the ash cloud is nearing one of the region’s busiest airports, raising concerns about engine safety and visibility.
""",
    """
08:45 AM – Flight Rerouting Begins
"Emergency Advisory: Non-Essential Flights Rerouted or Grounded"
In response to safety risks, aviation authorities instruct airlines to divert or temporarily ground flights until conditions are reassessed.
""",
    """
09:00 AM – Cancellations Announced
"Major Airlines Cancel Dozens of Flights Amid Ash Hazard"
Airlines begin canceling scheduled departures. Passengers across multiple terminals are advised to check for updates.
""",
    """
09:15 AM – Airport Operations Halt
"Airport Shutdown: Runways Closed Due to Ash Contamination"
Local news reports confirm that a primary airport has suspended operations, with emergency crews on site to manage the fallout.
""",
    """
09:30 AM – Government Press Conference
"Officials Address Volcanic Emergency; Evacuation Protocols Discussed"
Government representatives hold a press briefing to outline safety measures and coordinate evacuation plans for affected communities.
""",
    None,
    """
10:00 AM – International Impact
"Airspace Declared Hazardous: International Flight Routes Disrupted"
The ash cloud’s movement forces neighboring countries to close parts of their airspace, impacting transcontinental flights and travel plans worldwide.
""",
    None,
    None,
    None,
    """
11:00 AM – Regional Updates
"Ash Cloud Drifting Westward; Impact Extends to Neighboring Regions"
Meteorological experts update the public as the ash plume spreads, affecting additional airports and travel hubs.
""",
    None,
    None,
    None,
    """
12:00 PM – Emergency Response Escalates
"Emergency Crews Deployed to Assist Stranded Passengers"
Rescue operations and ground support teams are mobilized at affected airports, providing relief and information to stranded travelers.
""",
    None,
    None,
    None,
    """
01:00 PM – Monitoring Conditions
"Experts Report Decreasing Ash Density; Caution Still Advised"
Ongoing assessments show the ash cloud is beginning to thin. However, officials stress that conditions remain volatile for flight operations.
""",
    None,
    None,
    None,
    """
02:00 PM – Gradual Resumption of Flights
"Air Traffic Slowly Resumes as Authorities Reassess Safety Measures"
With improving atmospheric conditions, airlines cautiously start rebooking and resuming select flights on cleared routes.
""",
    None,
    None,
    None,
    """
03:00 PM – Passenger Rebooking and Refunds
"Airlines Initiate Passenger Rebooking and Offer Refund Options"
Airlines issue rebooking instructions and refunds, advising passengers to stay tuned for further travel updates.
""",
    None,
    None,
    None,
    """
04:00 PM – Cleanup and Recovery Efforts
"Airport Cleanup Begins: Runway Maintenance and Safety Inspections Underway"
Maintenance crews commence decontamination procedures at the impacted airport, preparing for a return to normal operations.
""",
    None,
    None,
    None,
    """
05:00 PM – Investigation Launched
"Authorities Launch Investigation into Volcanic Impact on Aviation"
A full-scale inquiry is announced to examine the event's effects on air traffic management and safety protocols.
""",
    None,
    None,
    None,
    """
06:00 PM – Situation Stabilizes
"Officials Confirm: All Airports to Resume Full Operations Tomorrow"
With the ash cloud dissipating and cleanup efforts progressing, officials project a return to normal air travel by the next day.
""",
    None,
    None,
    None,
    """
07:00 PM – Day-End Summary
"Disaster Day Concludes: Lessons Learned, Safety Protocols to Improve"
Media outlets wrap up the day with analysis and statements from aviation experts, emphasizing the need for enhanced monitoring and rapid response plans for future incidents.
""",
]


@function_tool(
    name_override="fake_news_feed_tool",
    description_override="Generates a news feed that simulates the development of a disaster situation.",
)
async def fake_news_feed_tool(context: RunContextWrapper[AgentContext]) -> str:
    context.context.i_news = (context.context.i_news + 1) % len(_NEWS)

    news = _NEWS[context.context.i_news]
    if news:
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
