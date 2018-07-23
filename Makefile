IMAGE_NAME=tf_image_classifier_flask

build:
	docker build -t anupamsapre/$(IMAGE_NAME):latest .

run:
	docker run --rm -p 5000:5000 anupamsapre/$(IMAGE_NAME):latest


