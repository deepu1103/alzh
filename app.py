from flask import Flask, render_template, request, redirect, url_for, flash
import os
from preprocess import load_preprocess_and_predict

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Recommendations for predictions
RECOMMENDATIONS = {
    "Alzheimers Disease (AD)": [
        "Consult a neurologist immediately for an in-depth assessment.",
        "Engage in memory training exercises and therapies.",
        "Follow a balanced diet rich in antioxidants and omega-3 fatty acids.",
        "Involve family members for support and monitoring."
    ],
    "Cognitive Normal (CN)": [
        "Maintain regular physical activity to keep your brain healthy.",
        "Follow a diet low in sugar and processed foods.",
        "Have regular health check-ups to monitor cognitive health."
    ],
    "Mild Cognitive Impairment (MCI)": [
        "Schedule a follow-up with a neurologist to monitor progression.",
        "Engage in regular brain-stimulating activities like puzzles.",
        "Adopt stress-management practices such as yoga or meditation."
    ],
    "Early Mild Cognitive Impairment (EMCI)": [
        "Start cognitive exercises to slow the progression of symptoms.",
        "Ensure regular health monitoring by a healthcare professional.",
        "Stay socially active to maintain cognitive function."
    ]
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/upload_pet')
def upload_pet():
    return render_template('upload_pet.html')

@app.route('/upload', methods=['POST'])
def handle_upload():
    pet_scan = request.files.get('pet-scan')
    patient_id = request.form.get('patient-id')
    scan_date = request.form.get('scan-date')
    comments = request.form.get('comments')

    if pet_scan:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], pet_scan.filename)
        pet_scan.save(file_path)
        prediction_result = load_preprocess_and_predict(file_path)
        os.remove(file_path)
        recommendations = RECOMMENDATIONS.get(prediction_result, ["No specific recommendations available."])
        return render_template(
            'result.html',
            prediction=prediction_result,
            recommendations=recommendations,
            patient_id=patient_id
        )

    flash('File upload failed. Please try again.')
    return redirect(url_for('upload_pet'))

@app.route('/upload_mri')
def upload_mri():
    return render_template('upload_mri.html')

@app.route('/upload1', methods=['POST'])
def handle_upload1():
    mri_scan = request.files.get('mri-scan')
    patient_id = request.form.get('patient-id')
    scan_date = request.form.get('scan-date')
    comments = request.form.get('comments')

    if mri_scan:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], mri_scan.filename)
        mri_scan.save(file_path)
        prediction_result = load_preprocess_and_predict(file_path)
        os.remove(file_path)
        recommendations = RECOMMENDATIONS.get(prediction_result, ["No specific recommendations available."])
        return render_template(
            'result.html',
            prediction=prediction_result,
            recommendations=recommendations,
            patient_id=patient_id
        )

    flash('File upload failed. Please try again.')
    return redirect(url_for('upload_mri'))

@app.route('/result')
def result():
    prediction = request.args.get('prediction')
    patient_id = request.args.get('patient_id')
    recommendations = RECOMMENDATIONS.get(prediction, ["No specific recommendations available."])
    return render_template(
        'result.html',
        prediction=prediction,
        recommendations=recommendations,
        patient_id=patient_id
    )

if __name__ == '__main__':
    app.run(debug=True)

