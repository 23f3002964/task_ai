from typing import List, Dict, Any
from . import models, schemas

# A simple dictionary to store our decomposition templates.
# The keys are keywords to look for in a goal's title.
# The values are lists of sub-goal descriptions.
# This provides a basic "rule-based" decomposition for the MVP.
DECOMPOSITION_TEMPLATES: Dict[str, List[str]] = {
    "learn": [
        "Research and gather learning resources (books, courses, articles).",
        "Create a structured study plan and schedule.",
        "Dedicate time to study and practice regularly.",
        "Apply knowledge by working on a small project.",
        "Review progress and identify areas for improvement.",
    ],
    "build": [
        "Define the project scope and requirements.",
        "Create a technical design and architecture plan.",
        "Set up the development environment.",
        "Develop the core features sprint by sprint.",
        "Test the application thoroughly.",
        "Deploy the application.",
    ],
    "write": [
        "Brainstorm and outline the main ideas and structure.",
        "Conduct research and gather necessary information.",
        "Write the first draft.",
        "Revise and edit for clarity, grammar, and style.",
        "Get feedback from peers or editors.",
        "Finalize and publish the content.",
    ],
    "publish": [
        "Finalize content and formatting.",
        "Choose a publishing platform.",
        "Create a launch plan and marketing materials.",
        "Publish the work.",
        "Promote and share with the target audience.",
    ],
    "launch": [
        "Finalize the product or service.",
        "Create a marketing and communications plan.",
        "Prepare the launch-day activities.",
        "Execute the launch.",
        "Monitor feedback and initial performance metrics.",
    ],
}

def generate_sub_goals_from_template(goal_title: str) -> List[Dict[str, Any]]:
    """
    Generates a list of sub-goals based on keywords in the goal's title.

    Args:
        goal_title: The title of the parent goal.

    Returns:
        A list of dictionaries, where each dictionary represents a sub-goal
        to be created (matching the SubGoalCreate schema).
    """
    sub_goals_to_create: List[Dict[str, Any]] = []
    normalized_title = goal_title.lower()

    for keyword, template in DECOMPOSITION_TEMPLATES.items():
        if keyword in normalized_title:
            for description in template:
                sub_goals_to_create.append({"description": description})
            # For the MVP, we stop after finding the first matching keyword.
            # A more advanced version could combine templates.
            return sub_goals_to_create

    # If no keyword is found, return an empty list.
    return []


def decompose_goal(goal: models.Goal) -> List[schemas.SubGoalCreate]:
    """
    Takes a Goal object, generates sub-goal data using the template engine,
    and returns a list of SubGoalCreate schemas ready for insertion.
    """
    sub_goal_data = generate_sub_goals_from_template(goal.title)
    return [schemas.SubGoalCreate(**data) for data in sub_goal_data]
