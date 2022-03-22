#! /bin/bash

docker build -t gcr.io/$DEVSHELL_PROJECT_ID/perfable . 
docker push gcr.io/$DEVSHELL_PROJECT_ID/perfable
gcloud run deploy perfable \
    --project $DEVSHELL_PROJECT_ID \
    --image gcr.io/$DEVSHELL_PROJECT_ID/perfable \
    --set-env-vars DB_HOST=${_DB_HOST} \
    --set-env-vars DB_PORT=${_DB_PORT} \
    --set-env-vars DB_USER=${_DB_USER} \
    --set-env-vars DB_PASS=${_DB_PASS} \
    --set-env-vars DB_NAME=${_DB_NAME} \
    --set-env-vars DB_CNST=postgresql+psycopg2://${_DB_USER}:${_DB_PASS}@${_DB_HOST}:${_DB_PORT}/${_DB_NAME} \
    --timeout 10m \
    --no-cpu-throttling \
    --vpc-connector ${_VPC_CON} \
    --region us-central1 \
    --platform managed \
    --min-instances 0 \
    --max-instances 3 \
    --allow-unauthenticated

# docker run --rm -e PORT=6969 gcr.io/holy-diver-297719/dfcx-usps
# docker run -it --rm -e PORT=6969 gcr.io/holy-diver-297719/dfcx-usps /bin/bash