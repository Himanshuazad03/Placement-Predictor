import sys
import json

# Define weights for each skill
SKILL_WEIGHTS = {
    "C_Cpp": 0.5,
    "Java": 1.0,
    "Python": 1.5,
    "HTML_CSS": 0.3,
    "UI_UX": 0.5,
    "Javascript": 1.0,
    "Numpy_Pandas": 1.2,
    "Scikit_learn": 1.5,
    "MERN": 1.5,
    "Linux": 0.3,
    "Cloud_Platforms": 1.2,
    "App_development": 1.0
}

def calculate_skill_rating(data):
    # Get selected skills
    skills = data.get("skills", [])
    if isinstance(skills, str):
        skills = [skills]

    # Sum weighted points for selected skills
    skill_points = sum(SKILL_WEIGHTS.get(skill, 0) for skill in skills)

    # Contest performance contribution
    contests = float(data.get("Number_of_Contest_attempted", 0))
    leetcode_rating = float(data.get("LC_Contest_rating", 0))
    leetcode_medium = float(data.get("Leetcode_Medium_problems", 0))

    # Normalize contest contributions
    contest_points = min(contests/20, 2)  # Max 2 points
    rating_points = min(leetcode_rating/1000, 3)  # Max 3 points
    medium_points = min(leetcode_medium/50, 2.5)  # Max 2.5 points

    total_points = skill_points + contest_points + rating_points + medium_points

    # Cap at 10
    return round(min(total_points, 10), 2)

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])
    rating = calculate_skill_rating(input_data)
    print(rating)
