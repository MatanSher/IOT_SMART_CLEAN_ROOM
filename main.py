import publisher
import subscriber
import concurrent.futures

def main():
    # Create Air conditioning in clean rooms dashboard // for specific room insert room number // for all rooms insert 0
    client_id = 3
    # Run publisher and subscriber in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        subscriber_future = executor.submit(subscriber.subscribe, client_id)
        publisher_future = executor.submit(publisher.generate_Air_conditioning_rate_and_publish, client_id)
        concurrent.futures.wait([subscriber_future, publisher_future])

main()


