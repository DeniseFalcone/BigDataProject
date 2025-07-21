from realtime_data_simulation import RealTimeDataSimulator
from path_ingestion_producer import NewImagePathProducer
from image_processing_consumer import ImageProcessingConsumer
import logging, time
        
def main():
    tasks = [
        RealTimeDataSimulator(),
        NewImagePathProducer(),
        ImageProcessingConsumer()
    ]

    for t in tasks:
        t.start()

    # Wait for all tasks to complete
    time.sleep(10) 

    for t in tasks:
        t.join()  
        
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO,
        handlers=[logging.StreamHandler()],
        force=True
    )
    main()

