export BACKEND=${BACKEND:-localhost}
siege -v -c 8 -t60S --content-type "application/x-www-form-urlencoded" "http://$BACKEND:8000/store_data POST < test_data.json"
