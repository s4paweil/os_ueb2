import multiprocessing
import copy
from LCG import LCG


class BankServer:
    def __init__(self, num_accounts, min_starting_balance, max_starting_balance, seed, queue):
        self.random_generator = LCG(str(seed))
        self.initial_accounts = {
            i + 1: self.random_generator.get_next_number_between(min_starting_balance, max_starting_balance) for i in
            range(num_accounts)}
        self.accounts = copy.deepcopy(self.initial_accounts)
        self.lock = multiprocessing.Lock()
        self.num_accounts = num_accounts
        self.queue = queue

    def transfer(self, from_account, to_account, amount):
        with self.lock:
            if 1 <= from_account <= len(self.accounts) and 1 <= to_account <= len(self.accounts):
                if self.accounts[from_account] >= amount:
                    self.accounts[from_account] -= amount
                    self.accounts[to_account] += amount

    def accounts_to_string(self):
        with self.lock:
            total_balance_end = sum(self.accounts.values())
            total_balance_start = sum(self.initial_accounts.values())

            accounts_balance = []

            accounts_balance.extend([total_balance_start, total_balance_end])

            for key in sorted(set(self.accounts.keys()) & set(self.initial_accounts.keys())):
                accounts_balance.extend([self.initial_accounts[key], self.accounts[key]])

            result_string = "[" + ", ".join(map(str, accounts_balance)) + "]"
            return result_string


def run_server(queue, num_accounts, min_starting_balance, max_starting_balance, seed):
    server = BankServer(num_accounts, min_starting_balance, max_starting_balance, seed, queue)
    while True:
        data = queue.get()
        if data == "STOP":
            print(server.accounts_to_string())
            break
        k1, k2, amount = data
        server.transfer(k1, k2, amount)


def run_client(queue, num_operations, num_accounts, min_transfer_amount, max_transfer_amount, seed):
    random_generator = LCG(str(seed))

    for _ in range(num_operations):
        k1 = random_generator.get_next_number(num_accounts) + 1
        k2 = random_generator.get_next_number(num_accounts) + 1
        amount = random_generator.get_next_number_between(min_transfer_amount, max_transfer_amount)
        queue.put((k1, k2, amount))


if __name__ == "__main__":
    num_accounts = 5
    num_clients = 10
    num_operations = 1000
    seed = "42"
    min_starting_balance = 500
    max_starting_balance = 10000
    min_transfer_amount = 0
    max_transfer_amount = 300

    random_generator = LCG(seed)
    server_queue = multiprocessing.Queue()

    server_process = multiprocessing.Process(target=run_server, args=(server_queue, num_accounts, min_starting_balance, max_starting_balance, random_generator.get_next_number(1000)))
    server_process.start()

    client_processes = [multiprocessing.Process(target=run_client, args=(server_queue, num_operations, num_accounts, min_transfer_amount, max_transfer_amount, random_generator.get_next_number(1000))) for _ in range(num_clients)]

    for process in client_processes:
        process.start()

    for process in client_processes:
        process.join()

    server_queue.put("STOP")

    server_process.join()
