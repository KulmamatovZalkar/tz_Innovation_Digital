# Flask Image Recognition Microservice

A simple Flask web application that uses YOLOv5 for object detection in images.

## Installation

Before starting, make sure you have Docker and Docker Compose installed.

1. Clone the repository:

-- git clone https://github.com/yourusername/image_recognition_microservice.git

-- cd image_recognition_microservice

2. Build the Docker image:

-- docker-compose build


## Running

Run the application using Docker Compose:

-- docker-compose up

After starting, the application will be available at `http://localhost:5000`.

## Usage

1. Open the web interface at `http://localhost:5000`.
2. Upload an image on which you want to detect objects using the upload form.
3. After uploading the image, the YOLOv5 model will process it and display the results on the page.

## Technologies

- **Flask:** A web framework for creating web applications.
- **YOLOv5:** A deep learning model for object detection.
- **OpenCV:** A library for image processing.
- **Docker:** A platform for deploying applications in containers.

## License

[MIT](LICENSE)
