from openai import BaseModel


class AgentContext(BaseModel):
    """Global state of the system"""

    disaster_info: str = """
    ### Disaster Timeline: Volcanic Ash Crisis

    - **07:45 AM – Early Warning**  
    _"Seismic Activity Detected Near Mount Caldera"_  
    Seismologists report unusual tremors around Mount Caldera. Authorities and local media begin monitoring for potential volcanic activity.

    - **08:00 AM – Initial Eruption**  
    _"Mount Caldera Erupts: Minor Ash Emissions Observed"_  
    A small eruption occurs, sending a limited ash plume into the sky. Aviation authorities are alerted and begin assessing the risk.

    - **08:15 AM – Aviation Alert Issued**  
    _"Air Traffic Control Monitors Ash Cloud: Flight Delays Expected"_  
    Preliminary advisories are issued to airlines as the ash cloud begins drifting toward major flight corridors.

    - **08:30 AM – Impact Near Airports**  
    _"Volcanic Ash Cloud Approaching International Airport"_  
    Reports indicate the ash cloud is nearing one of the region’s busiest airports, raising concerns about engine safety and visibility.

    - **08:45 AM – Flight Rerouting Begins**  
    _"Emergency Advisory: Non-Essential Flights Rerouted or Grounded"_  
    In response to safety risks, aviation authorities instruct airlines to divert or temporarily ground flights until conditions are reassessed.

    - **09:00 AM – Cancellations Announced**  
    _"Major Airlines Cancel Dozens of Flights Amid Ash Hazard"_  
    Airlines begin canceling scheduled departures. Passengers across multiple terminals are advised to check for updates.

    - **09:15 AM – Airport Operations Halt**  
    _"Airport Shutdown: Runways Closed Due to Ash Contamination"_  
    Local news reports confirm that a primary airport has suspended operations, with emergency crews on site to manage the fallout.

    - **09:30 AM – Government Press Conference**  
    _"Officials Address Volcanic Emergency; Evacuation Protocols Discussed"_  
    Government representatives hold a press briefing to outline safety measures and coordinate evacuation plans for affected communities.

    - **10:00 AM – International Impact**  
    _"Airspace Declared Hazardous: International Flight Routes Disrupted"_  
    The ash cloud’s movement forces neighboring countries to close parts of their airspace, impacting transcontinental flights and travel plans worldwide.

    - **11:00 AM – Regional Updates**  
    _"Ash Cloud Drifting Westward; Impact Extends to Neighboring Regions"_  
    Meteorological experts update the public as the ash plume spreads, affecting additional airports and travel hubs.

    - **12:00 PM – Emergency Response Escalates**  
    _"Emergency Crews Deployed to Assist Stranded Passengers"_  
    Rescue operations and ground support teams are mobilized at affected airports, providing relief and information to stranded travelers.

    - **01:00 PM – Monitoring Conditions**  
    _"Experts Report Decreasing Ash Density; Caution Still Advised"_  
    Ongoing assessments show the ash cloud is beginning to thin. However, officials stress that conditions remain volatile for flight operations.

    - **02:00 PM – Gradual Resumption of Flights**  
    _"Air Traffic Slowly Resumes as Authorities Reassess Safety Measures"_  
    With improving atmospheric conditions, airlines cautiously start rebooking and resuming select flights on cleared routes.

    - **03:00 PM – Passenger Rebooking and Refunds**  
    _"Airlines Initiate Passenger Rebooking and Offer Refund Options"_  
    Airlines issue rebooking instructions and refunds, advising passengers to stay tuned for further travel updates.

    - **04:00 PM – Cleanup and Recovery Efforts**  
    _"Airport Cleanup Begins: Runway Maintenance and Safety Inspections Underway"_  
    Maintenance crews commence decontamination procedures at the impacted airport, preparing for a return to normal operations.

    - **05:00 PM – Investigation Launched**  
    _"Authorities Launch Investigation into Volcanic Impact on Aviation"_  
    A full-scale inquiry is announced to examine the event's effects on air traffic management and safety protocols.

    - **06:00 PM – Situation Stabilizes**  
    _"Officials Confirm: All Airports to Resume Full Operations Tomorrow"_  
    With the ash cloud dissipating and cleanup efforts progressing, officials project a return to normal air travel by the next day.

    - **07:00 PM – Day-End Summary**  
    _"Disaster Day Concludes: Lessons Learned, Safety Protocols to Improve"_  
    Media outlets wrap up the day with analysis and statements from aviation experts, emphasizing the need for enhanced monitoring and rapid response plans for future incidents.
    """

    i_news: int = 0

