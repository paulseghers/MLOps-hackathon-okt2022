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
We will deploy a Cloud Run service which can do the above and be accessed through a basic API server. Basically, we want a service we can send requests to in order to return the datasets.
1. Create a BigQuery ressource, and a dataset in it. When prompted with the location, pick `eu-west-something` or `eu-north-something` if you want your own waiting time when looking at the data to be short, But `us-central-1` if you want the code to have low latency (the code will be run in that region because it's the cheapest datacenter), though this doesn't really matter that much.
3. create a service account with the following roles, and note down its name: (In `Credentials`)
    - `BigQuery Data Owner`
    - `BigQuery Job User`
    - `Storage Object Admin`
    (for this part we _technically_ only need the first two, but this way you can re-use the same service account for the next section)
A service account is like a user that a service can impersonate which has the permissions to do certain things the service will need to do. In real production environments you usually would try to get the permitions as "tight" as possible ("Admin" over a whole GCP service is not), but this is a hackathon, so these will do.
4. Now, take a deep breath. We are going to create a Docker image which will be able to spawn containers that the code we deploy to the cloud can run within. To let our cloud run utilise these containers, we need to have the image they're created from pushed to the Google Artifact registry. This is a fancy name for a repository that contains resources that Cloud Run can, well, run things in. In a "real world" scenario, you can setup services which build docker images in the cloud as well, but to save time we will initiate the build of the image locally and push, that way we don't have to mess around with uploading all the files it depends on. If you have a google cloud CLI authenticated with your project, the following command will do all this:
```
gcloud builds submit . -t gcr.io/<your gcp project name>/<name you want the image to have>
```
Then go to the Google artifacts registry tab. check that your image is there
and copy the name it got.

5. Actually creating the Cloud Run: You can head over to the cloud run tab on the console if you want to see what the different options look like, but we will do it programatically like so
```
gcloud run deploy <name you want your cloud Run service to have> \
    --image=<url of gcr repo you made just earlier> \
    --no-allow-unauthenticated \
    --service-account=<service account ID> \
    --memory=1Gi \
    --region=us-central1 \
    --project=<your GCP project name>
```
If this command runs to completion, you've successfully deployed the cloud Run. Now let's look into using the API we've built-in to call the functions in the code from earlier.<br>_Note: we run in us-central-1 by habit because it's the cheapest data center, but you can pick another region if you want_
<br>
If you look into the Dockerfile, you'll see we're running a `uvicorn` server as our final command. This is a python web server engine on top of which we run a python API server which we can build with modules such as Flask or FastAPI. They both work quite similarly, but we used FastAPI here. The API endpoints are defined in `run_main.py`. You really do not need to worry about this too much, but you *do* need to know how to call the functions in the cloud run through this API. This is commonly done using the `curl` command.
<br>
In the console, go to the Cloud Run service, and copy its url, it ends with `.run.app`.<br>
To be able to authenticate the requests you will make to it, you will also need the google cloud identity token of an account that has the right to invoke the cloud run. You can create a service account specifically for this (with the cloud invoke role), though an easier but also hacky (this is a hackathon after all) way of getting a token is to grab the identity token of your own GCP account, by running
```
gcloud auth print-identity-token
```
To get the results of a reddit query for example, we can then run
```
curl <api url>/reddit \
    -XPOST -H 'content-type: application/json' \
    -H "Authorization: Bearer <your gcloud token>" \
    -d '{"dest": "<your BigQuery bucket dataset ID>.<a table ID>", "subreddits": ["news", "worldnews"]}'
```
the `dest` argument is currently required, though you can change its behavior by changing code which describes what is done when the server receives a request, in the `run_main.py` file.<br>
 **Tip**: save the api url, token, and possibly other variables you use a lot as _environment variables_ in the shell session you are calling the gcloud cli from. For example:
```
export api="https://newsreader-service-edtzmec2da-uc.a.run.app"
export gcptoken=$(gcloud auth print-identity-token)
```
then
```
curl $api/reddit \
    -XPOST -H 'content-type: application/json' \
    -H "Authorization: Bearer $gcptoken" \
    -d '{"dest": "news_articles_1.reddit_1", "subreddits": ["news", "worldnews"]}'
```
similarly, for twitter:
```
curl $api/twitter \
    -XPOST -H 'content-type: application/json' \
    -H "Authorization: Bearer $token" \
    -d '{"dest": "news_articles_1.twitter_1", "accounts": ["BBCBreaking", "washingtonpost"]}'
```
You can see how the beavior upon reaching an endpoint is defined in the file `run_main.py`.<br>
It is purposefully still very vanilla, as the idea is that you can modify the way pandas dataframe functions are used to suit your MLOps needs: for example, do you want to have a single table, or create a new one with each run to train the model? Do you want different datasets for different sets of accounts? How do you want to organise your data? This will all depend on your choice of models in the next part. _Remember:_ run `gcloud builds submit... ` again when you modify the code, as this is where the "upload" of sorts takes place.
<!---
my own one when testing looks like this
gcloud run deploy newsreader-service \
    --image=gcr.io/hackathon-instance-paul/paul-mlops-newsreader \
    --no-allow-unauthenticated \
    --service-account=mlops-paul-io@hackathon-instance-paul.iam.gserviceaccount.com  \
    --memory=1Gi \
    --region=us-central1 \
    --project=hackathon-instance-paul
-->



