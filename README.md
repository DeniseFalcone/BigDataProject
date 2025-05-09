data = contiene i dati iniziali
  |
  |--> dataset = ha le foto
  |--> imageserver = arrivano le foto in dataset andando a fingere il realtime
docker = docker setup
  |
  |-->Dockerfile
  |-->docker-compose.yaml
kafka = kafka setup files
web_app = files per la web_app
  |
  |--> back_end = backend sito (riceve i risultati del test)
  |--> front_end = ui con analytics e test 
image_processing_pipeline = file per prendere dati in real time, processarli, applicare dl alg. e salvare i risultati
  |
  |--> ingestion = file per prendere dati dalla cartella e darli a kafka
  |--> processing = files per processare i dati tramite diversi workers
  |--> db = files per il db e lo storage dei dati
.env = salva variabili d'ambiente
.gitignore = files da ignorare
fake_realtime_stream.py = script per far finta di avere dati in realtime
README.md = questo file: spiega come importare ed usare il progetto

docker-compose.yaml 
  services that can be removed:
    - mongo-express: ui for mongodb
    - rest-proxy: rest api kafka interactions, check if needed
    - ui (Kafka UI): ui for kafka 

TODO:
- consumer per processing (prende filepaths da file.txt in /data, li passa a yolo e salva i risultati su un'altra collection in mongodb)
- cartella data deve essere accessibile da web_app