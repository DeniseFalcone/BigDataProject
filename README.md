<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://www.unicam.it/">
    <img src="https://www.unicam.it/sites/default/files/inline-images/logoUNICAM-full.jpg" alt="LogoUnicam" width="300">
  </a>

<br>
<h1 align="center">End-to-End Image Classification System for Big Data Environments</h1>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#project-context">Project Context</a>
      <ul>
        <li><a href="#description">Description</a></li>
        <li><a href="#project-structure">Project Structure</a></li>
        <li><a href="#softwares-and-libraries">Softwares and Libraries</a></li>         
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#customizing-the-model">Customizing the Model</a></li>
        <li><a href="#real-time-data-simulation">Real Time data simulation</a></li>
        <li><a href="#parallelism-in-kafka-consumer">Parallelism in Kafka Consumer</a></li>
      </ul>
    </li>
    <li><a href="#result-preview">Result Preview</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Project Context

### Description
This project is a simplified object detection and classification pipeline designed for Big Data environments.

While the architecture is generic and supports various object detection or image classification tasks, for testing and demonstration purposes we used a deep learning model that performs binary classification on breast histopathological images to determine the presence (1) or absence (0) of a tumor. 

The system mimics a scalable image processing pipeline where images are ingested, classified, and the results are made available through a web-based interface.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Project Structure
The repository is organized into modular components:
```sh
   .
├── data/          
│   ├── dataset/ # contains all images
│   ├── imageserver/ # use to simulate real time data         
│   ├── processed_images/ # stores classified images
│   ├── to_process_images/ # images ready to be classified
│
├── image_processing/          
│   ├── model/ # contains the deep learning model 
│   ├── utils/ # contains utility functions
│
├── web_app/ # contains files related to web interface                    
│
├── docker-compose.yaml 
├── LICENSE
├── README.md
└── .gitignore
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Softwares and Libraries
* [![Kafka][Kafka-img]][Kafka-url]
* [![Python][Python-img]][Python-url]
* [![Docker][Docker-img]][Docker-url]
* [![MongoDB][MongoDB-img]][MongoDB-url]
* [![Tensorflow][Tensorflow-img]][Tensorflow-url]
* [![Streamlit][Streamlit-img]][Streamlit-url]
* [![Keras][Keras-img]][Keras-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Setup & Run Instruction

### Prerequisites

* Docker installed and running
(either <a href= "https://www.docker.com/products/docker-desktop/">Docker Desktop </a> or <a href="https://docs.docker.com/engine/install/">Docker Engine</a> + <a href="https://docs.docker.com/compose/install/">Compose CLI</a>)
* <a href="https://git-scm.com/downloads">git</a> installed (optional but reccomended)


### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/DeniseFalcone/BigDataProject.git

   cd BigDataProject
   ```

2. Prepare required folders
    * After cloning, you need to manually create these three folders inside the `data/` folder:
        * `to_process_images`
        * `imageserver`
        * `processed_images`
  
      You can create them via command line:
    ```sh
    mkdir -p data/to_process_images data/imageserver data/processed_images
    ```

3. Start Docker:
    * If you are using Docker Desktop (GUI): open Docker Desktop app and wait until it shows that Docker is running.
    * If you are using Docker from the command line: make sure your Docker daemon is running (depends on your OS, e.g., sudo systemctl start docker on Linux).

4. Run the containers
    * Open the project forlder in your terminal (if not done already)
    * Run this command to build and start the containers:

    ```sh
    docker compose up --build
    ```
    
5. Open your browser and go to:
   ```sh
   http://localhost:8501
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Customizing the Model   

By default, this project uses a binary classification deep learning model for demonstration purposes.

If you'd like to use your own model :
1. Replace the model file in the `image_processing/model` folder with your custom model.
2. Replace the `image_processing/utils/data_preprocessing.py` with your own data preprocessing script. Keep the original name of the file.
3. In the `image_processing/image_processing_consumer.py` script, replace line 103
 ( `self.prediction_model = tf.keras.models.load_model('model/binary_classification_model_0505.keras')`) by passing the new model.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Real Time data simulation

The project is designed to operate on real-time data streams. Since no live data source is available, a real-time data simulator has been implemented to emulate this behavior.

The `RealTimeDataSimulator class` is responsible for copying images from a static dataset folder (`DATASET_FOLDER`) to a target folder (`FOLDER_TO_WATCH`), which is continuously monitored by the data processing pipeline. This simulates the arrival of new files in a real-time.

If real-time simulation is not needed, it is sufficient to remove the `RealTimeDataSimulator()` from the `image_processing/main.py`. When running the system via docker-compose, make sure to set the correct `FOLDER_TO_WATCH` path in the `docker-compose.yml` file according to your use case.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Parallelism in Kafka Consumer

This system leverages Kafka's native parallelism using:
* A shared consumer group (`get-images-paths-group`).
* A multi-partition topic (`get_path_topic`, currently with 2 partitions).
* Multiple consumer instances (`ImageProcessingConsumer()`), each running in parallel via Python’s multiprocessing.

To increase the degree of parallelism, follow these steps:
1. Increase the number of partitions (e.g. from 3 to 4) in the Kafka topic (`docker-compose.yaml`):
```sh
   KAFKA_NUM_PARTITIONS: 4
   ```
2. Start more `ImageProcessingConsumer()` processes in your `image_processing/main.py`:
```sh
  ImageProcessingConsumer(),
  ImageProcessingConsumer(),
  ImageProcessingConsumer(),
  ImageProcessingConsumer()
   ```    

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Result Preview -->
## Result Preview

Example of the processed output displayed in the web interface. 
The images are updated each time a new one is processed. By clicking on an image, it can be enlarged, and by clicking the "Processed" button, the image can be hidden.

![Demo](assets/demo.gif)
<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Denise Falcone - denise.falcone@studenti.unicam.it

Chiara Cintioni - chiara.cintioni@studenti.unicam.it

Project Link: [https://github.com/DeniseFalcone/BigDataProject.git](https://github.com/DeniseFalcone/BigDataProject.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>








<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->


[Docker-img]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/

[Streamlit-img]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/

[Kafka-img]: https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white
[Kafka-url]: https://kafka.apache.org/

[Tensorflow-img]: https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white
[Tensorflow-url]: https://www.tensorflow.org/

[Python-img]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[MongoDB-img]: https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white
[MongoDB-url]: https://www.mongodb.com/

[Keras-img]: https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white
[Keras-url]: https://keras.io/


