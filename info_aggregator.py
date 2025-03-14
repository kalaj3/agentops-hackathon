import heapq
import json
import os
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class EmergencyCase:
    injury_type: str
    caller_name: str
    first_responders_demanded: List[str]
    conversation_id: int
    need_severity: int
    closed: bool
    conversation: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


class EmergencyResponseSystem:
    def __init__(self, data_file="emergency_data.json"):
        self.data_file = data_file
        self.cases = self._load_data()

    def _load_data(self) -> List[EmergencyCase]:
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                return [EmergencyCase.from_dict(case) for case in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self):
        with open(self.data_file, "w") as f:
            json.dump([case.to_dict() for case in self.cases], f, indent=2)

    def add_case(self, case: EmergencyCase):
        self.cases.append(case)
        self._save_data()

        # Save conversation to text file
        file_name = f"conversation_{case.conversation_id}.txt"
        mode = "w" if not os.path.exists(file_name) else "a"

        with open(file_name, mode) as f:
            if mode == "w":
                f.write(f"Caller: {case.caller_name}\n\n")
            f.write(f"{case.conversation}\n\n")

    def update_case(self, conversation_id: int, **kwargs):
        for case in self.cases:
            if case.conversation_id == conversation_id:
                for key, value in kwargs.items():
                    if hasattr(case, key):
                        setattr(case, key, value)
                self._save_data()
                return True
        return False

    def get_open_cases(self) -> List[EmergencyCase]:
        return [case for case in self.cases if not case.closed]

    def get_case_by_id(self, conversation_id: int) -> Optional[EmergencyCase]:
        for case in self.cases:
            if case.conversation_id == conversation_id:
                return case
        return None

    def add_to_conversation(self, conversation_id: int, new_text: str) -> bool:
        """
        Add new text to an existing conversation and update the conversation file

        Args:
            conversation_id: ID of the conversation to update
            new_text: Text to add to the conversation

        Returns:
            bool: True if successful, False if conversation not found
        """
        case = self.get_case_by_id(conversation_id)
        if not case:
            return False

        # Update the case conversation text
        case.conversation += f"\n{new_text}"

        # Save to data file
        self._save_data()

        # Update the conversation text file
        file_name = f"conversation_{conversation_id}.txt"
        with open(file_name, "a") as f:
            f.write(f"{new_text}\n\n")

        return True

    def update_responders(self, conversation_id: int, responders: List[str]) -> bool:
        """
        Update the list of responders demanded for a case

        Args:
            conversation_id: ID of the case to update
            responders: New list of responders

        Returns:
            bool: True if successful, False if case not found
        """
        case = self.get_case_by_id(conversation_id)
        if not case:
            return False

        case.first_responders_demanded = responders
        self._save_data()
        return True

    def update_case_field(self, conversation_id: int, field: str, value) -> bool:
        """
        Update any field in a case by field name

        Args:
            conversation_id: ID of the case to update
            field: Field name to update
            value: New value for the field

        Returns:
            bool: True if successful, False if case not found or field invalid
        """
        case = self.get_case_by_id(conversation_id)
        if not case:
            return False

        if not hasattr(case, field):
            return False

        setattr(case, field, value)
        self._save_data()
        return True

    def count_responders_needed(self) -> Dict[str, int]:
        """Query how many of each responder is needed"""
        responder_counts = {}

        for case in self.get_open_cases():
            for responder in case.first_responders_demanded:
                if responder not in responder_counts:
                    responder_counts[responder] = 0
                responder_counts[responder] += 1

        return responder_counts

    def get_next_conversation_id(self) -> int:
        if not self.cases:
            return 1
        return max(case.conversation_id for case in self.cases) + 1


def test_multiple_conversations():
    """Test adding and updating multiple conversations in the system"""
    # Create a test data file
    test_data_file = "test_emergency_data.json"

    # Delete the test file if it exists
    if os.path.exists(test_data_file):
        os.remove(test_data_file)

    # Delete any test conversation files
    for i in range(1, 5):
        if os.path.exists(f"conversation_{i}.txt"):
            os.remove(f"conversation_{i}.txt")

    # Initialize the system with test data file
    ers = EmergencyResponseSystem(test_data_file)

    # Case 1: Heart attack
    case1 = EmergencyCase(
        injury_type="Heart attack",
        caller_name="John Doe",
        first_responders_demanded=["paramedic"],
        conversation_id=1,
        need_severity=9,
        closed=False,
        conversation="Caller: I think my father is having a heart attack! He's clutching his chest and can't breathe properly.",
    )
    ers.add_case(case1)

    # Case 2: Car accident
    case2 = EmergencyCase(
        injury_type="Car accident",
        caller_name="Jane Smith",
        first_responders_demanded=["paramedic", "police"],
        conversation_id=2,
        need_severity=8,
        closed=False,
        conversation="Caller: There's been a car crash! Two vehicles collided and one person seems trapped.",
    )
    ers.add_case(case2)

    # Case 3: Fire
    case3 = EmergencyCase(
        injury_type="Building fire",
        caller_name="Mike Johnson",
        first_responders_demanded=["firefighter", "paramedic"],
        conversation_id=3,
        need_severity=10,
        closed=False,
        conversation="Caller: There's a fire in an apartment building! People might be trapped inside!",
    )
    ers.add_case(case3)

    # Add updates to conversations
    ers.add_to_conversation(
        1, "Dispatcher: Is the patient conscious? Can you describe their breathing?"
    )
    ers.add_to_conversation(
        1,
        "Caller: Yes, he's conscious but breathing heavily. He's also sweating a lot.",
    )

    ers.add_to_conversation(
        2, "Dispatcher: Are there any injuries? How many people are involved?"
    )
    ers.add_to_conversation(
        2, "Caller: At least two people are injured. One seems unconscious."
    )

    ers.add_to_conversation(
        3, "Dispatcher: Which floors are affected? Is there smoke visible?"
    )
    ers.add_to_conversation(
        3,
        "Caller: It's on the second floor. There's a lot of smoke coming out of the windows.",
    )

    # Update case fields
    ers.update_case_field(1, "need_severity", 10)
    ers.update_responders(2, ["paramedic", "police", "firefighter"])
    ers.update_case_field(3, "closed", True)

    # Verify the data was saved
    new_ers = EmergencyResponseSystem(test_data_file)

    # Check if all cases were loaded
    assert len(new_ers.cases) == 3, f"Expected 3 cases, got {len(new_ers.cases)}"

    # Check if updates were applied
    case1 = new_ers.get_case_by_id(1)
    assert case1.need_severity == 10, f"Expected severity 10, got {case1.need_severity}"

    case2 = new_ers.get_case_by_id(2)
    assert (
        "firefighter" in case2.first_responders_demanded
    ), "Firefighter not found in responders"

    case3 = new_ers.get_case_by_id(3)
    assert case3.closed == True, "Case 3 should be closed"

    # Check if conversation files were created
    for i in range(1, 4):
        assert os.path.exists(
            f"conversation_{i}.txt"
        ), f"Conversation file {i} not found"

    # Check responder counts
    responder_counts = new_ers.count_responders_needed()
    assert (
        responder_counts.get("paramedic", 0) == 2
    ), f"Expected 2 paramedics, got {responder_counts.get('paramedic', 0)}"

    print("All tests passed!")

    # Clean up test files
    if os.path.exists(test_data_file):
        os.remove(test_data_file)
    for i in range(1, 4):
        if os.path.exists(f"conversation_{i}.txt"):
            os.remove(f"conversation_{i}.txt")


def demo_start_conversation():
    """
    Demo function showing how to start a new conversation in the Emergency Response System.
    This is a simple example for AI agents to understand the basic workflow.
    """
    # Initialize the system
    ers = EmergencyResponseSystem()

    # Get a new conversation ID
    new_id = ers.get_next_conversation_id()

    # Create a new emergency case
    new_case = EmergencyCase(
        injury_type="Fall",
        caller_name="AI Agent",
        first_responders_demanded=["paramedic"],
        conversation_id=new_id,
        need_severity=6,
        closed=False,
        conversation="Initial report: Person fell down stairs and cannot move their left leg.",
    )

    # Add the case to the system
    ers.add_case(new_case)

    # Add a follow-up to the conversation
    ers.add_to_conversation(
        new_id, "Update: Person reports pain when attempting to move leg."
    )

    print(f"Started conversation with ID: {new_id}")
    print(f"Case details: {new_case.to_dict()}")

    return new_id


if __name__ == "__main__":
    demo_start_conversation()
