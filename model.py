def predict_health(glucose, haemoglobin, cholesterol):

    if glucose > 140 and cholesterol > 240:
        return "High Diabetes Risk"

    elif glucose > 110 or cholesterol > 200:
        return "Moderate Risk"

    else:
        return "Low Risk"