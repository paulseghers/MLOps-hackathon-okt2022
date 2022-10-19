# Deploying a model to the cloud

This section will show you the basics of getting a model built with pytorch to run in a Google Cloud Run, and setting up an API to trigger the training/testing/evaluation of the model.

You will need a service account with roles:
    - `BigQuery Data Owner`
    - `BigQuery Job User`
    - `Storage Object Admin`
As well as a Cloud Storage Bucket set-up
1. As before, build the Docker image and push it to a container/artifact registry.
```
gcloud builds submit . -t gcr.io/<your gcp project name>/<name you want the image to have>
```
2. Run
```
gcloud run deploy <name you want your cloud Run service to have> \
    --image=<url of the gcr repo you made just earlier> \
    --no-allow-unauthenticated \
    --service-account=<service account ID> \
    --memory=1Gi \
    --region=us-central1 \
    --project=<your gcp project name>
```

<!---
my own one when testing looks like this
gcloud run deploy model-v1 \
    --image=gcr.io/hackathon-instance-paul/model-v1 \
    --no-allow-unauthenticated \
    --service-account=mlops-paul-io@hackathon-instance-paul.iam.gserviceaccount.com  \
    --memory=1Gi \
    --region=us-central1 \
    --project=hackathon-instance-paul
-->


3. In the Cloud Run menu, find the api endpoint (url) for the cloud Run you just created. Now, we are ready to interact with it using an API.
4. Again, get your identity token, api, etc:
```
export api=$(gcloud run services describe <model service name> --region us-central1 --format 'value(status.url)')
export token=$(gcloud auth print-identity-token)
```
Here, we also need to define locations for saving the model to and loading the datatset from. To build our API call, we can do the following
```
export dataset=<URI of your datatset file>
export model=<uri of your model>
```
I tested with the example dataset: `gs://mlops-hackathon-paul/iris.csv`. You can get the URIs for your objects inside Cloud Store by right clicking the three dots at the end of the line an object is on.

**DISCLAIMER**: I'm not very good at writing APIs for Machine Learning models...so in the example I gave we need to pass a payload of the features we want to train on. This is done as follows (for this example):
```
export train_payload=$(cat <<EOF
{
    "dataset": "$dataset",
    "model": "$model",
    "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
    "target": "species"
}
EOF
)
```
5. Now we can call:
```
curl $api/train \
    -XPOST -H 'content-type: application/json' \
    -H "Authorization: Bearer $token" \
    -d "$train_payload"
```
And check that the file `model.plk` in our Cloud Storage has in fact been populated by a blob of our model.<br>
If it didn't happen, check instead the logs of
<br>
The functions `load_model` and `save_model` from `run_api.py` will be of particular interest. Take a look at the functions from the `google.cloud.storage` python module. Here we put a blob of the model in a Cloud Storage object, but this could also be done with a plot, the output of the model, a dump of hyperparameters, etc.

### Can also be done using cloud functions. These have a shorter feedback loop in development than Cloud run, but they have the disadvantage that for larger pieces of code, development can be a pain, as code that runs in Cloud Run can be run locally in a Docker container with the same environment.

Try making a cloud function which also authenticates with an object in Cloud store using the same functions.