import sys, json
# Example: you would load a real pre-trained model instead
# model = joblib.load('placement_model.pkl')

# Dummy example model
def predict(data):
    # Simple formula for demonstration
    
    cgpa = float(data.get("cgpa", 0))
    internship = float(data.get("internship", 0))
    projects = float(data.get("projects", 0))
    aptitude_score = float(data.get("aptitude_score", 0))
    ssc_marks = float(data.get("ssc_marks", 0))

    
    score = (cgpa/10)*30 + (internship/5)*20 + (projects/5)*20 + (aptitude_score/100)*20 + (ssc_marks/100)*10
    return round(score,2)

if __name__ == "__main__":
    # Get JSON input from Node
    input_data = json.loads(sys.argv[1])
    result = predict(input_data)
    print(result)
