import requests

from chatbot.config import env
from chatbot.chat.models import StudentProfile


def get_student_profile(student_id: str) -> StudentProfile:
    """
    Get the student profile from the database.

    Args:
        student_id (str): The ID of the student to fetch.

    Returns:
        StudentProfile: The student profile.
    """
    response = requests.get(f"{env.BACKEND_URL}/students/{student_id}")

    if response.status_code != 200:
        raise Exception(f"Failed to fetch student profile: {response.status_code}")

    student_data = response.json()

    return StudentProfile(
        student_id=student_data["id"],
        unweighted_gpa=student_data["unweightedGPA"],
        geographic_preferences=student_data["geographicPreferences"],
    )


def update_student_profile(student_id: str, profile: StudentProfile) -> StudentProfile:
    """
    Update the student profile in the database.

    Args:
        student_id (str): The ID of the student to update.
        profile (StudentProfile): The updated student profile.

    Returns:
        StudentProfile: The updated student profile.
    """
    response = requests.put(
        f"{env.BACKEND_URL}/students/{student_id}",
        json={
            "unweightedGPA": profile.unweighted_gpa,
            "geographicPreferences": profile.geographic_preferences,
        },
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        raise Exception(f"Failed to update student profile: {response.status_code}")

    student_data = response.json()

    return StudentProfile(
        student_id=student_data["id"],
        unweighted_gpa=student_data["unweightedGPA"],
        geographic_preferences=student_data["geographicPreferences"],
    )
