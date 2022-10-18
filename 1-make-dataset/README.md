# Making a data set of new articles off of Reddit and Twitter

Let's make the data set your model will train on.

## 1- Running it locally.
First let's build the dataset locally, so one team member can already train a model or do data exploration while the others are still setting up gcp.<br><br>
You will need twitter and reddit credentials, refer to [this guide](not.yet.done.sdfghjhgfdgh) to acquire them.
For this part, download this folder and create at the root of part 1 a file called `secrets.yaml`, where you throw in your (or your group's) reddit and twitter API keys and secrets, as so:
```
twitter:
    API_key:
    API_secret:
    access_token:
    access_secret:
reddit:
    client_id:
    client_secret:
```

## 2- Running it in the Cloud
1. BigQuery
2. Create cloud store
3. create a service account with the following roles:
    - `BigQuery Data Owner`
    - `BigQuery Job User`
    - `Storage Object Admin`



