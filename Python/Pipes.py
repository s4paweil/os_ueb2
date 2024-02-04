import multiprocessing
import random
import logging
import copy
import time

class BankServer:
    def __init__(self, num_accounts, min_starting_balance, max_starting_balance, pipe):
        self.accounts = {i + 1: random.randint(min_starting_balance, max_starting_balance) for i in range(num_accounts)}
        self.accountsStartConf = copy.deepcopy(self.accounts)
        self.lock = multiprocessing.Lock()
        self.pipe = pipe
        self.start_time = time.time()
        self.num_accounts = num_accounts
        self.num_clients = num_clients
        self.num_operations = num_operations


    def transfer(self, from_account, to_account, amount):
        with self.lock:
            if 1 <= from_account <= len(self.accounts) and 1 <= to_account <= len(self.accounts):
                if self.accounts[from_account] >= amount:
                    self.accounts[from_account] -= amount
                    self.accounts[to_account] += amount

    def log(self, end_time):
        with self.lock:
            logMsg = f"Python - Multiprocessing / Pipes\n"
            logMsg += f"Execution time: {end_time - self.start_time:.5f} seconds\n"
            logMsg += f"Number of accounts: {self.num_accounts}, Number of clients: {self.num_clients}, Number of transfers per client: {self.num_operations}\n"

            total_balance_end = sum(self.accounts.values())
            total_balance_start = sum(self.accountsStartConf.values())

            if total_balance_start == total_balance_end:
                logMsg += f"Consistency check passed. Total balance at start and end are equal: {total_balance_end}\n"
            else:
                logMsg += f"Consistency check failed. Total balance at start: {total_balance_start} versus end: {total_balance_end}\n"

            logMsg += "{:<10}{:<20}{:<20}\n".format("Konto", "Balance Start", "Balance End")

            for k, v in self.accountsStartConf.items():
                logMsg += "{:<10}{:<20}{:<20}\n".format(k, v, self.accounts[k])


            logging.basicConfig(filename='log.txt', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.INFO)

            logging.info(logMsg)

    def run_server(self):
        while True:
            try:
                data = self.pipe.recv()
                if data == "STOP":
                    self.log(time.time())
                    break
                k1, k2, amount = data
                self.transfer(k1, k2, amount)
            except EOFError:
                break

class BankClient:
    def __init__(self, pipe, num_operations, num_accounts, min_transfer_amount, max_transfer_amount):
        self.pipe = pipe
        self.num_operations = num_operations
        self.num_accounts = num_accounts
        self.min_transfer_amount = min_transfer_amount
        self.max_transfer_amount = max_transfer_amount

    def run_operations(self):
        for _ in range(self.num_operations):
            k1 = random.randint(1, self.num_accounts)
            k2 = random.randint(1, self.num_accounts)
            amount = random.randint(self.min_transfer_amount, self.max_transfer_amount)
            self.pipe.send((k1, k2, amount))

def run_simulation(num_accounts, num_clients, num_operations, seed, min_starting_balance, max_starting_balance):
    client_pipe, server_pipe = multiprocessing.Pipe()
    server = BankServer(num_accounts, min_starting_balance, max_starting_balance, server_pipe)
    server_process = multiprocessing.Process(target=server.run_server)
    server_process.start()

    clients = [BankClient(client_pipe, num_operations, num_accounts, min_transfer_amount, max_transfer_amount) for _ in range(num_clients)]
    client_processes = [multiprocessing.Process(target=client.run_operations) for client in clients]

    for process in client_processes:
        process.start()

    for process in client_processes:
        process.join()

    client_pipe.send("STOP")
    server_process.join()

if __name__ == "__main__":
    num_accounts = 5
    num_clients = 10
    num_operations = 10
    seed = 42
    min_starting_balance = 500
    max_starting_balance = 1000
    min_transfer_amount = 0
    max_transfer_amount = 300

    run_simulation(num_accounts, num_clients, num_operations, seed, min_starting_balance, max_starting_balance)
