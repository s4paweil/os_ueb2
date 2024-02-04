import threading
import time
import logging
import copy

from LCG import LCG


class BankServer:
    def __init__(self, num_accounts, min_starting_balance, max_starting_balance, seed):
        self.random_generator = LCG(str(seed))
        self.initial_accounts = {i + 1: self.random_generator.get_next_number_between(min_starting_balance, max_starting_balance) for i in range(num_accounts)}
        self.accounts = copy.deepcopy(self.initial_accounts)
        self.lock = threading.Lock()

    def transfer(self, from_account, to_account, amount):
        with self.lock:
            if 1 <= from_account <= len(self.accounts) and 1 <= to_account <= len(self.accounts) and from_account != to_account:
                if self.accounts[from_account] >= amount:
                    self.accounts[from_account] -= amount
                    self.accounts[to_account] += amount

    def log(self, start_time, end_time, num_accounts, num_clients, num_transfers_per_client):
        with self.lock:
            logMsg = f"Python - Single Process / Threads\n"
            logMsg += f"Execution time: {end_time - start_time:.5f} seconds\n"
            logMsg += f"Number of accounts: {num_accounts}, Number of clients: {num_clients}, Number of transfers per client: {num_transfers_per_client}\n"

            total_balance_end = sum(self.accounts.values())
            total_balance_start = sum(self.initial_accounts.values())

            logMsg += f"{'Consistency check passed' if total_balance_start == total_balance_end else 'Consistency check failed'}"
            logMsg += f". Total balance at start and end are equal: {total_balance_end}\n"

            logMsg += "{:<10}{:<20}{:<20}\n".format("Konto", "Balance Start", "Balance End")

            for k, v in self.initial_accounts.items():
                logMsg += "{:<10}{:<20}{:<20}\n".format(k, v, self.accounts[k])

            logging.basicConfig(filename='log.txt', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.INFO)

            logging.info(logMsg)


class BankClient:
    def __init__(self, server, num_operations, min_transfer_amount, max_transfer_amount, seed):
        self.server = server
        self.num_operations = num_operations
        self.min_transfer_amount = min_transfer_amount
        self.max_transfer_amount = max_transfer_amount
        self.random_generator = LCG(str(seed))

    def run_operations(self):
        for _ in range(self.num_operations):
            k1 = self.random_generator.get_next_number(len(self.server.accounts)) + 1
            k2 = self.random_generator.get_next_number(len(self.server.accounts)) + 1
            amount = self.random_generator.get_next_number_between(self.min_transfer_amount, self.max_transfer_amount)
            self.server.transfer(k1, k2, amount)

def run_simulation(num_accounts, num_clients, num_operations, seed, min_starting_balance, max_starting_balance,
                   min_transfer_amount, max_transfer_amount):
    random_generator = LCG(seed)

    server = BankServer(num_accounts, min_starting_balance, max_starting_balance, random_generator.get_next_number(1000))
    clients = [BankClient(server, num_operations, min_transfer_amount, max_transfer_amount, random_generator.get_next_number(1000)) for _ in range(num_clients)]

    start_time = time.time()

    threads = [threading.Thread(target=client.run_operations) for client in clients]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    server.log(start_time, end_time, num_accounts, num_clients, num_operations)

if __name__ == "__main__":
    num_accounts = 5
    num_clients = 10
    num_operations = 1000
    seed = "42"
    min_starting_balance = 0
    max_starting_balance = 1000
    min_transfer_amount = 0
    max_transfer_amount = 300

    run_simulation(num_accounts, num_clients, num_operations, seed, min_starting_balance, max_starting_balance,
                   min_transfer_amount, max_transfer_amount)
