from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("C:\\Users\\NISHTHA GUPTA\\OneDrive\\Desktop\\Sleep Disorder\\sleep_disorder_model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
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
            prediction = sleep_disorder_mapping[prediction]
        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template("index.html", prediction=prediction)


@app.route('/submit_journal', methods=['POST'])
def submit_journal():
    symptoms = request.form['symptoms']
    mood = request.form['mood']

    # Open journals.txt file to save the journal entry
    with open('journals.txt', 'a') as file:
        file.write(f"Symptoms: {symptoms}\nMood: {mood}\n\n")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
