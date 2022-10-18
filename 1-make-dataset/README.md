# Making a data set of new articles off of Reddit and Twitter

Let's make the data set your model will train on.<br>
All commands on this page should be run at the root of the `1-make-dataset/` folder.
## 1- Running it locally and understanding how the dataset is built.
First let's build the dataset locally, so one team member can already train a model or do data exploration while the others are still setting up gcp.<br><br>
You will need twitter and reddit credentials, refer to [this guide](not.yet.done.sdfghjhgfdgh) to acquire them.
For this part, download this folder and create at the root of part 1 a file called `secrets.yaml`, where you throw in your (or your group's) reddit and twitter API keys and secrets, as such:
```
twitter:
    API_key: y0uRaPikeY
    API_secret:
    access_token:
    access_secret:
reddit:
    client_id:
    client_secret:
```
Then, you can run it by doing
```
python cli.py <source website> <output filepath> <options> --limit <n>
```
Where `<source website>` is the string `twitter` or `reddit`, and `<output filepath>` is the path to a `.csv` file relative to where you run the script from. `<options>` can be the names of the twitter accounts and subreddits you want to pull headlines from. `<--limit>` is a flag you pass as an int which will be the max number of articles to fetch. By default it is set to `100` For example:
```
python cli.py twitter output.csv BBCBreaking washingtonpost
```
will take news headlines from the twitter accounts [BBC Breaking News](https://twitter.com/bbcbreaking) and [Washingtonpost](https://twitter.com/washingtonpost). Choosing what news sources to build your dataset from is part of your task. We used those two as they cover wide ranges of topics so NLP models would be less sensitive to specific types of words or place names, etc<br>

*Note: make sure you have tweepy version 4.10.1 or later*
## 2- Running it in the Cloud
We will deploy a cloud run service which can do the above and put the results in places where other services can access them.
1. Create a BigQuery ressource, and a dataset in it. (use some location `eu-west-` or `eu-north-` for least latency).
2. Create a Cloud Store Bucket
3. create a service account with the following roles:
    - `BigQuery Data Owner`
    - `BigQuery Job User`
    - `Storage Object Admin`
A service account is like a user that a service can impersonate which has the permissions to do certain things the service will need to do. In real production environments you usually would try to get the permitions as "tight" as possible.
4. Now, take a deep breath. We are going to create a Docker image which will be able to spawn containers that the code we deploy to the cloud can run within. To let our cloud run utilise the se containers, we need to have the image they're creatde from pushed to the Google Artifact registry. This is a fancy name for a repository that contains resources that Cloud Run can, well, run things in. In a "real world" scenario, you can setup services which build docker images in the cloud as well, but to save time we will build the image locally and push it. If you have a google cloud CLI authenticated with your project, the following command will do all this:
```
gcloud builds submit . -t gcr.io/<your gcp project name>/<name you want the image to have>
```
Then go to the Google artifacts registry tab. check that your image is there
and copy the name it got.
5. Actually creating the Cloud Run. You can head over to the cloud run tab on the console if you want to see what the different options look like, but we will do it programatically like so
```
gcloud run deploy <name you want your cloud Run service to have> \
    --image=<link to gcr repo> \
    --no-allow-unauthenticated \
    --service-account=<service account ID> \
    --memory=1Gi \
    --region=us-central1 \
    --project=<your project name>
```

gcloud run deploy newsreader-service \
    --image=gcr.io/hackathon-instance-paul/paul-mlops-newsreader \
    --no-allow-unauthenticated \
    --service-account= \
    --memory=1Gi \
    --region=us-central1 \
    --project=<your project name>

