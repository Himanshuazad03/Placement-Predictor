import sys
import json
import pandas as pd
import pickle
import warnings
warnings.filterwarnings('ignore')

# model load kr liya 
with open("model_with_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

def main():
    try:
        data = json.loads(sys.argv[1])

        # dataframe bana liya 
        columns = ['CGPA', 'Internship', 'Paid_Internship', 'Projects', 
                   'Aptitude_Score', 'Skills_Rating', 'Placement_Training', 
                   'SSC_Marks', 'Gender']
        
        df = pd.DataFrame([[
            float(data.get('cgpa', 0)),
            int(data.get('internship', 0)),
            int(data.get('paid_internship', 0)),
            int(data.get('projects', 0)),
            float(data.get('aptitude_score', 0)),
            float(data.get('skill_rating', 0)),
            data.get('placement_training', 'Not Attended'),
            float(data.get('ssc_marks', 0)),
            data.get('gender', 'Male')
        ]], columns=columns)

        # prediction kra or backend me bhej diya 
        prediction = model.predict(df)
        prediction_proba = model.predict_proba(df) 

        print(prediction_proba[0][1])

    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()