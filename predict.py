import sys
import json
import pandas as pd
import pickle

# Load model
with open("full_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

def main():
    try:
        data = json.loads(sys.argv[1])
        
        placement_training_map = {'Yes': 1, 'No': 0}
        gender_map = {'Male': 1, 'Female': 0}

        student_data = {
            'CGPA': [float(data.get('cgpa', 0))],
            'Internship': [int(data.get('internship', 0))],
            'Paid_Internship': [int(data.get('paid_internship', 0))],
            'Projects': [int(data.get('projects', 0))],
            'Aptitude_Score': [float(data.get('aptitude_score', 0))],
            'Skills_Rating': [float(data.get('skills_rating', 0))],
            'Placement_Training': [placement_training_map.get(data.get('placement_training', 'No'), 0)],
            'SSC_Marks': [float(data.get('ssc_marks', 0))],
            'Gender': [gender_map.get(data.get('gender', 'Male'), 1)]
        }

        df = pd.DataFrame(student_data)
        X = df.values

        prediction = model.predict(X)[0]
        prediction_proba = model.predict_proba(X)[0]

        print(prediction_proba[1])

    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
