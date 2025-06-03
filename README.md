# emotional_intelligence Using Logistic Regression

This project implements a emotional analysis pipeline to classify text into four emotions: happy, sad, anger, and neutral. It's built using scikit-learn and standard NLP techniques for clean and reproducible experimentation.

## Dataset

The dataset used was sourced from **Kaggle**:

**Dataset Name:** *[Emotion Dataset for Emotion Recognition Tasks](https://www.kaggle.com/datasets/parulpandey/emotion-dataset?resource=download)*  


Each entry in the dataset contains:
- `text`: A sentence or short user-generated content.
- `label`: A manually tagged sentiment label (`happy`, `sad`, `anger`, or `neutral`).

Before training, the data was filtered to include only these four categories and cleaned to remove empty or irrelevant entries.

## Approach

1. **Preprocessing**
   - Dropped rows with missing or empty text.
   - Removed whitespace-only entries and stop-word-only content.

2. **Feature Extraction**
   - Applied TF-IDF vectorization with English stop word removal.
   - Limited feature space to the top 5000 most relevant tokens.

3. **Model Training**
   - Trained a Logistic Regression classifier with `max_iter=1000`.
   - Used an 80/20 train-test split.

4. **Evaluation**
   - Reported performance using accuracy, classification report, and confusion matrix.
   - Plotted a confusion matrix heatmap for visual understanding.

5. **Model Saving**
   - Persisted the trained model and vectorizer using `joblib` for reuse.

## Dependencies

To run this project, ensure the following Python libraries are installed:

'''bash
pip install pandas scikit-learn matplotlib seaborn joblib

## Used Libraries

- **pandas** – for data loading and cleaning  
- **scikit-learn** – for vectorization, model training, and evaluation  
- **matplotlib**, **seaborn** – for visualizations  
- **joblib** – for model persistence

## Potential Improvements

- Expand to more emotion classes (e.g., fear, disgust, surprise)  
- Use advanced models like SVM, XGBoost, or transformer-based architectures  
- Deploy with a web interface using Flask or Streamlit

