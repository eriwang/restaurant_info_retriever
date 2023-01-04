gcloud functions deploy python-http-function \
  --gen2 \
  --runtime=python38 \
  --region=us-central1 \
  --source=. \
  --entry-point=get_rating_info \
  --trigger-http
