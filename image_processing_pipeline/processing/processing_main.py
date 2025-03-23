import logging, time
import processing_producer, processing_consumer
        
def main():
    tasks = [
        processing_producer.BatchFileProducer(),
        processing_consumer.BatchFileConsumer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)  # Let the threads run

    for t in tasks:
        t.join()  # Ensure threads complete execution
        
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO,
        handlers=[logging.StreamHandler()],
        force=True
    )
    main()

