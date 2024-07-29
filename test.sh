# curl -X POST "http://localhost:8000/store_data" \
#      -H "accept: application/json" \
#      -H "Content-Type: multipart/form-data" \
#      -F "data={\"name\": \"test\", \"description\": \"test description\"};type=application/json" \
#      -F "file=@test.jpg"
curl -X POST "http://localhost:8000/store_data" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "data={\"name\": \"test\", \"description\": \"test description\", \"image\": \"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\"};type=application/json"
