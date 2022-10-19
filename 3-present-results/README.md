# Presenting results

Since this is a short hackathon, we will be using streamlit to show plots. Streamlit supports a variety of python plots and graphical objects, including all the famous ones like [`matplotlib.pyplot`](https://docs.streamlit.io/library/api-reference/charts/st.pyplot)
 We will be closely following the tutorial:<br>
 https://medium.com/analytics-vidhya/deploying-streamlit-apps-to-google-app-engine-in-5-simple-steps-5e2e2bd5b172
 <br>
 Simply run
 ```
 gcloud app deploy app.yaml
 ```
 in this directory, to deploy a siple streamlit app to the google app engine.<br>
 Streamlit apps are quit simple to use. They are normal python scripts, where multiline/string comments are rendered as text on the webpage, and plots can be rendered with interactivity. Check the file `minimal_streamlit_app.py` for a basic, easy-to-understand example.<br>
 You could in theory run all your models and work in the app engine that the streamlit app runs in, but app engines are much more expensive by the minute and by computation ressource than things like Cloud Run.<br>
 A Hackathon-y solution would be to authenticate with a gcs Bucket in your streamlit app, and write/fetch a pickle or some other blob of your plots there.
