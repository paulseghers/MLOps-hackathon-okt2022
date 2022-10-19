# Presenting results

Since this is a short hackathon, we will be using streamlit to show plots. Streamlit supports a variety of python plots and graphical objects, including all the famous ones like [`matplotlib.pyplot`](https://docs.streamlit.io/library/api-reference/charts/st.pyplot)
 We will be closely following these tutorials:<br>
 https://docs.streamlit.io/knowledge-base/tutorials/databases/gcs <br>
 and<br>
 https://medium.com/analytics-vidhya/deploying-streamlit-apps-to-google-app-engine-in-5-simple-steps-5e2e2bd5b172
 <br>
 <br>
 A Hackathon-y solution would be to authenticate with a gcs Bucket in your streamlit app, and write/fetch a pickle or some other blob of your plots there.