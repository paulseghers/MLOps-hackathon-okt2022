# run locally
python local.py


# run des nuaj
runner_sa=paul-mlops@m4h-info.iam.gserviceaccount.com
model_svc=paul-mlops-model
model_img=gcr.io/m4h-info/paul-mlops-model

# on peut run ca dans cloud shell pour pas avoir a setup trop de trucs
gcloud builds submit . -t $model_img
gcloud run deploy $model_svc \
    --image=$model_img \
    --no-allow-unauthenticated \
    --service-account=$runner_sa \
    --memory=1Gi \
    --region=us-central1 \
    --project=m4h-info


api=$(gcloud run services describe $model_svc --region us-central1 --format 'value(status.url)')
# aussumes you are owner, or have cloud run invoker role
token=$(gcloud auth print-identity-token)

dataset="gs://paul-mlops/iris.csv"
model="gs://paul-mlops/clf.pkl"

train_payload=$(cat <<EOF
{
    "dataset": "$dataset",
    "model": "$model",
    "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
    "target": "species"
}
EOF
)

curl $api/train \
    -XPOST -H 'content-type: application/json' \
    -H "Authorization: Bearer $token" \
    -d "$train_payload"


predict_payload=$(cat <<EOF
{
    "model": "$model",
    "samples": [{
        "sepal_length": 1.0,
        "sepal_width": 2.0,
        "petal_length": 3.0,
        "petal_width": 4.0
    }]
}
EOF
)

curl $api/predict \
    -XPOST -H 'content-type: application/json' \
    -H "Authorization: Bearer $token" \
    -d "$predict_payload"


