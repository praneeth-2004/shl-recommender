# SHL Assessment Recommender

This is a conversational AI system that recommends SHL assessments based on user queries.

## API Endpoints

### GET /health
Returns API status

### POST /chat
Request:
{
  "query": "data analyst test"
}

Response:
{
  "type": "recommendation",
  "recommendations": [...]
}