# Cat-Dog classification model using Streamlit

CNN model was downloaded from https://github.com/abhaybd/Cat-Dog-CNN-Classifier.    
Dataset with images was downloaded from https://www.kaggle.com/stevenhurwitt/cats-vs-dogs-using-a-keras-convnet

In order to use the app, please do the following:
1. Clone or download this repository
2. In command prompt go to this project directory
3. Run this command <code>streamlit run Classification_app.py</code>
4. Open URL from the previous step in your browser
5. Choose the file in the left side
6. Start predicting the image labels by pressing a button
7. Create a correspondings excel file with predictions
8. See the resulting json
9. Enjoy analyzing the raw excel file

Regarding the excel analysis, there are two issues.    
The first one, the model needs images to be compressed into 64x64 image. As far as I understand, this leads to the many false positive predictions. Moreover, the model is possibly overfitted which results in 100% certainty in the most cases even if the prediction is wrong. 100 percent certainty makes it difficult to have various values at different cutoff ratios. This is why the ROC curve has only two points.    
Secondly, having a dog on the photo does not mean not having a cat and vice versa. That is why it is not a typical TP/TN problem which possibly affects the results as well.