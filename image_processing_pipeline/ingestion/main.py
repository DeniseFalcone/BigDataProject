import logging, time
import consumer, producer, fake_realtime_stream
        
def main():
    tasks = [
        consumer.Consumer(),
        producer.Producer(),
        fake_realtime_stream.RealTimeDataSimulator()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)  # Let the threads run

    for t in tasks:
        t.join()  # Ensure threads complete execution
        
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()

