
# output to stdout
python cli.py reddit - news
python cli.py twitter - BBCBreaking

# output to file
python cli.py twitter output.csv BBCBreaking washingtonpost



# TODOs
# service account, BigQuery Data Owner + Bigu
# create BigQuery dataset

runner_sa=<email of the service acc you created with permissions>
newsreader_svc=<ID of the news reader cloud run service>
newsreader_img=gcr.io/<your gcp project>/<docker image name>

gcloud builds submit . -t <image name>
gcloud run deploy <cloud run service name> \
    --image=$newsreader_img \
    --no-allow-unauthenticated \
    --service-account=$runner_sa \
    --memory=1Gi \
    --region=us-central1 \
    --project=<project ID>

api="https://paul-mlops-newsreader-25hmciganq-uc.a.run.app" #example for mine
# aussumes you are owner, or have cloud run invoker role
token=$(gcloud auth print-identity-token)

curl $api/reddit \
    -XPOST -H 'content-type: application/json' \
    -H "Authorization: Bearer $token" \
    -d '{"dest": "paul_mlops.reddit2", "subreddits": ["news", "worldnews"]}'

curl $api/twitter \
    -XPOST -H 'content-type: application/json' \
    -H "Authorization: Bearer $token" \
    -d '{"dest": "paul_mlops.twitter2", "accounts": ["BBCBreaking", "washingtonpost"]}'
