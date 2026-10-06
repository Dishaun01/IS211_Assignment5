"""Compare the average queue wait for one or more web servers."""

import argparse
import csv
from collections import deque


class Request:
    def __init__(self, arrival, path, duration):
        self.arrival = int(arrival)
        self.path = path.strip()
        self.duration = int(duration)
        if self.arrival < 0 or self.duration < 0:
            raise ValueError("Times cannot be negative")


class Server:
    def __init__(self):
        self.queue = deque()
        self.time = 0

    def process(self):
        total_wait = 0
        while self.queue:
            request = self.queue.popleft()
            # Start when the request arrives or the server becomes free.
            start = max(self.time, request.arrival)
            total_wait += start - request.arrival
            self.time = start + request.duration
        return total_wait


def simulateManyServers(file, servers):
    if servers < 1:
        raise ValueError("Use at least one server")

    with open(file, newline="", encoding="utf-8-sig") as source:
        requests = [Request(*row) for row in csv.reader(source) if row]
    requests.sort(key=lambda request: request.arrival)

    pool = [Server() for _ in range(servers)]
    for index, request in enumerate(requests):
        # Take turns assigning requests to the servers.
        pool[index % servers].queue.append(request)

    total_wait = sum(server.process() for server in pool)
    average = total_wait / len(requests) if requests else 0
    print(f"Average wait time: {average:.7f} seconds")
    return average


def simulateOneServer(file):
    return simulateManyServers(file, 1)


def main(file, servers=None):
    if servers is None:
        return simulateOneServer(file)
    return simulateManyServers(file, servers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--servers", type=int)
    args = parser.parse_args()
    main(args.file, args.servers)
