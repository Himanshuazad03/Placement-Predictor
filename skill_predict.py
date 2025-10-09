import sys
import json
import pandas as pd
import pickle
import warnings
warnings.filterwarnings('ignore')

# Load the skill rating model
with open("skills_rating_with_pipe.pkl", "rb") as f:
    skill_model = pickle.load(f)

def prepare_skill_features(data):
    try:
        # Extract skills (checkboxes) - create binary features
        skills = data.get('skills', [])
        if isinstance(skills, str):
            skills = [skills]
        
        # Create binary features for each skill
        skill_features = {
            'C_Cpp': 1 if 'C_Cpp' in skills else 0,
            'Java': 1 if 'Java' in skills else 0,
            'Python': 1 if 'Python' in skills else 0,
            'HTML_CSS': 1 if 'HTML_CSS' in skills else 0,
            'UI_UX': 1 if 'UI_UX' in skills else 0,
            'Javascript': 1 if 'Javascript' in skills else 0,
            'Numpy_Pandas': 1 if 'Numpy_Pandas' in skills else 0,
            'Scikit_learn': 1 if 'Scikit_learn' in skills else 0,
            'MERN': 1 if 'MERN' in skills else 0,
            'Linux': 1 if 'Linux' in skills else 0,
            'Cloud_Platforms': 1 if 'Cloud_Platforms' in skills else 0,
            'App_development': 1 if 'App_development' in skills else 0
        }
        
        # Extract contest performance metrics
        contest_features = {
            'Number_of_Contest_attempted': int(data.get('Number_of_Contest_attempted', 0)),
            'LC_Contest_rating': int(data.get('LC_Contest_rating', 0)),
            'Leetcode_Medium_problems': int(data.get('Leetcode_Medium_problems', 0))
        }
        
        # Combine all features
        all_features = {**skill_features, **contest_features}
        
        return all_features
        
    except Exception as e:
        raise Exception(f"Error preparing features: {str(e)}")

def main():
    try:
        # Read JSON data from command line argument
        data = json.loads(sys.argv[1])
        
        # Prepare features
        features = prepare_skill_features(data)
        
        # Define column order (must match training data)
        columns = [
            'C_Cpp', 'Java', 'Python', 'HTML_CSS', 'UI_UX', 'Javascript',
            'Numpy_Pandas', 'Scikit_learn', 'MERN', 'Linux', 'Cloud_Platforms',
            'App_development', 'Number_of_Contest_attempted', 'LC_Contest_rating',
            'Leetcode_Medium_problems'
        ]
        
        # Create DataFrame with correct column order
        df = pd.DataFrame([[features[col] for col in columns]], columns=columns)
        
        # Make prediction using the model
        prediction = skill_model.predict(df)
        
        # If model returns probability, use predict_proba
        # prediction_proba = skill_model.predict_proba(df)
        # print(prediction_proba[0][1])
        
        # Output the predicted skill rating
        print(prediction[0])
        
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()