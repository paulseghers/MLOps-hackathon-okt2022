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


3. In the Cloud Run menu, find
4. Now, we are ready to interact with it using an API