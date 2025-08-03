import pytest
from uuid import uuid4
from datetime import datetime, timezone

from src import models, schemas
from src.decomposition import (
    generate_sub_goals_from_template,
    decompose_goal,
    DECOMPOSITION_TEMPLATES,
)

# ============================
# Unit Tests for Decomposition Logic
# ============================

@pytest.mark.parametrize(
    "keyword, expected_template_key",
    [
        ("learn python", "learn"),
        ("Build a website", "build"),
        ("write a blog post", "write"),
        ("Publish my book", "publish"),
        ("launch the new feature", "launch"),
    ],
)
def test_generate_sub_goals_from_template_keywords(keyword, expected_template_key):
    """
    Test that the template generator correctly identifies keywords.
    """
    sub_goals = generate_sub_goals_from_template(keyword)
    expected_descriptions = DECOMPOSITION_TEMPLATES[expected_template_key]

    assert len(sub_goals) == len(expected_descriptions)
    assert sub_goals[0]["description"] == expected_descriptions[0]

def test_generate_sub_goals_for_no_matching_keyword():
    """
    Test that an empty list is returned when no keyword is found.
    """
    title = "A goal with no decomposition template"
    sub_goals = generate_sub_goals_from_template(title)
    assert sub_goals == []

def test_decompose_goal_service_layer():
    """
    Test the service layer function that wraps the template generator.
    """
    # Create a mock Goal object (no database needed for this unit test)
    mock_goal = models.Goal(
        id=uuid4(),
        title="I want to learn how to play guitar",
        target_date=datetime.now(timezone.utc),
    )

    sub_goal_schemas = decompose_goal(mock_goal)

    assert len(sub_goal_schemas) == len(DECOMPOSITION_TEMPLATES["learn"])
    first_schema = sub_goal_schemas[0]
    assert isinstance(first_schema, schemas.SubGoalCreate)
    assert first_schema.description == DECOMPOSITION_TEMPLATES["learn"][0]
