#! /bin/bash

docker build -t gcr.io/holy-diver-297719/perfable . 
docker push gcr.io/holy-diver-297719/perfable
gcloud run deploy perfable \
    --project holy-diver-297719 \
    --image gcr.io/holy-diver-297719/perfable \
    --timeout 10m \
    --region us-east4 \
    --platform managed \
    --min-instances 0 \
    --max-instances 3 \
    --allow-unauthenticated

# docker run --rm -e PORT=6969 gcr.io/holy-diver-297719/dfcx-usps
# docker run -it --rm -e PORT=6969 gcr.io/holy-diver-297719/dfcx-usps /bin/bash