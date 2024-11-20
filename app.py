from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the model
model = joblib.load("C:\\Users\\NISHTHA GUPTA\\Downloads\\sleep_disorder_model.pkl")

# Route for the homepage
@app.route("/")
def index():
    return render_template("index.html")

# Route for prediction

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Fetch input data from form
        gender = int(request.form["gender"])
        age = int(request.form["age"])
        occupation = int(request.form["occupation"])
        sleep_duration = float(request.form["sleep_duration"])
        quality_of_sleep = int(request.form["quality_of_sleep"])
        physical_activity = int(request.form["physical_activity"])
        stress_level = int(request.form["stress_level"])
        bmi = int(request.form["bmi"])
        heart_rate = int(request.form["heart_rate"])
        daily_steps = int(request.form["daily_steps"])
        systolic_bp = int(request.form["systolic_bp"])
        diastolic_bp = int(request.form["diastolic_bp"])

        # Prepare input for prediction
        input_data = np.array([[gender, age, occupation, sleep_duration, quality_of_sleep,
                                physical_activity, stress_level, bmi, heart_rate, daily_steps,
                                systolic_bp, diastolic_bp]])

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Map encoded prediction back to sleep disorder categories
        sleep_disorder_mapping = {
            0: "None",
            1: "Insomnia",
            2: "Sleep Apnea",
            3: "Narcolepsy"
        }
        result = sleep_disorder_mapping[prediction]

        # Return prediction
        return jsonify({"Prediction": f"The predicted sleep disorder is: {result}"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
