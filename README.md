<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
</div>

<div id="badges" align="center">
  <a href="your-linkedin-URL">
    <img src="https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge"/>
  </a>
  <a href="your-youtube-URL">
    <img src="https://img.shields.io/badge/YouTube-red?style=for-the-badge&logo=youtube&logoColor=white" alt="Youtube Badge"/>
  </a>
  <a href="your-twitter-URL">
    <img src="https://img.shields.io/badge/Twitter-blue?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter Badge"/>
  </a>
</div>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=SuyashUtekar&style=flat-square&color=blue" alt=""/>
</p>

<h1 align="center">
  hey there
  <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="30px"/>
</h1>

# PE_Malicious_File_Detection_Using-ML
---
### :man_technologist: Overview :
This repository contains a sophisticated solution for detecting malicious files using Machine Learning (ML) techniques. The project leverages various algorithms to identify potentially harmful files and improve cybersecurity measures.

### :telescope: Feature Selection Methods:

-  Extra Trees Classifier
- Correlation Analysis
- SelectKBest
- Principal Component Analysis (PCA)

### :seedling: Machine Learning Algorithms:

- Decision Tree
- Random Forest
- AdaBoost
- Gradient Boosting
- Gaussian Naive Bayes (GNB)
- K-Nearest Neighbors (KNN)
- XGBoost
- Logistic Regression

## :hammer_and_wrench: Languages and Tools :
<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/tensorflow/tensorflow-original-wordmark.svg" title="TensorFlow" alt="TensorFlow" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/keras/keras-original.svg" title="Keras" alt="Keras" width="40" height="40"/>&nbsp;
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d0/Google_Colaboratory_SVG_Logo.svg" title="Google Colab" alt="Google Colab" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/scikitlearn/scikitlearn-original.svg" title="Scikit-learn" alt="Scikit-learn" width="40" height="40"/>&nbsp;
</div>

---

## :fire: My Stats :
[![GitHub Streak](http://github-readme-streak-stats.herokuapp.com?user=SuyashUtekar&theme=dark&background=000000)](https://git.io/streak-stats)

---

## 🚀 Implementation :

To execute the implementation of this project, follow these steps:

1. **Run All Cells in `main_implementation.ipynb`:**
   - This Jupyter Notebook contains the complete workflow for the project, including:
     - **Data Preprocessing:** Prepare the data for analysis by cleaning and normalizing it.
     - **Feature Selection:** Evaluate and apply the feature selection methods listed above (Extra Trees Classifier, Correlation Analysis, SelectKBest, PCA).
     - **Model Training:** Train all the ML models mentioned above (Decision Tree, Random Forest, etc.) using each feature selection method.
     - **Performance Evaluation:** Determine which feature selection method allows each model to perform the best.

2. **Save the Results:**
   - After determining the best-performing feature selection method for each model, create a dataset with those features.
   - Save the dataset to a file named `features.pkl`.
   - Save the best-performing model to a file named `model.pkl`.

3. **Final Implementation:**
   - In the last cell of the Notebook, you can test the system by providing a file to the model.
   - The model will predict whether the given file is malicious or not, based on the trained models and selected features.

These steps ensure that the model is accurately trained and can effectively predict malicious files, thus contributing to enhanced cybersecurity measures.

---

## 📊 Results:

### Accuracy Score Graph: 

- **Best Feature Selection Method:** The Extra Trees Classifier method was found to be the most effective for feature selection.
  - **Selected Features:** A total of 13 features were selected by the Extra Trees Classifier.
  
<img src="https://github.com/user-attachments/assets/9069b8b0-4cca-4184-90a5-884d14aaabcc" width="600" height="400"/>

- **Top-Performing Model:** Using the features selected by the Extra Trees Classifier, the Random Forest model achieved the best performance among all the machine learning models tested.
  - **Accuracy:** The Random Forest model achieved an accuracy of **0.9945**.
  - **Cross-Validation:** The model was also validated using cross-validation, yielding a Mean Cross-Validation Score of **0.9841**.
  
These results underscore the effectiveness of the Extra Trees Classifier for feature selection and demonstrate the high accuracy and reliability of the Random Forest model in detecting malicious files.

## 📝 Conclusion

This project focused on detecting malicious files using advanced Machine Learning (ML) techniques. The primary objectives were to:

1. **Optimize Feature Selection:** The Extra Trees Classifier emerged as the most effective feature selection method, successfully identifying 13 key features that significantly enhance model performance.

2. **Model Performance:** Among the various models tested, the Random Forest model, when trained on the features selected by the Extra Trees Classifier, demonstrated the highest accuracy. The Random Forest achieved an impressive accuracy of **0.9945** and a Mean Cross-Validation Score of **0.9841**.

3. **Implementation:** The project successfully implemented a comprehensive workflow that includes data preprocessing, feature selection, model training, and final predictions. The final implementation enables accurate detection of malicious files, contributing to enhanced cybersecurity measures.

Overall, the integration of effective feature selection and robust machine learning models has led to a highly accurate and reliable system for malicious file detection. The results underline the importance of selecting the right features and models to achieve high performance in cybersecurity applications.

## 🚀 Future Work

- **Enhanced Feature Selection:** Explore additional feature selection techniques and their impact on model performance.
- **Model Optimization:** Investigate more advanced models and hyperparameter tuning to further improve accuracy.
- **Deployment:** Consider deploying the model into a production environment for real-time malicious file detection.
- **User Interface:** Develop a user-friendly interface for easier interaction and file submission.

## 🙏 Acknowledgments

- **Libraries and Tools:** Acknowledgment of libraries and tools used, such as TensorFlow, Keras, and scikit-learn.

