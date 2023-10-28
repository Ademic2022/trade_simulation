import uuid, random, time, asyncio
import threading

class Trader:
    def __init__(self, name, balance=100.0):
        self._id = str(uuid.uuid4())
        self.name = name
        self.balance = balance
        self.total_trades = 0
        self.minute_lock = threading.Lock()

    def generate_profit_loss(self):
        min_value = -0.10  # -10%
        max_value = 0.10   # +10%
        return random.uniform(min_value, max_value)

    def update_balance(self, profit_loss):
        self.balance += self.balance * profit_loss

    def simulate(self, db, duration_minutes, simulation_state):
        """Create a thread for running the simulation"""
        simulation_thread = threading.Thread(target=self._run_simulation, args=(db, duration_minutes, simulation_state))
        """Start the thread"""
        simulation_thread.start()

    def _run_simulation(self, db, duration_minutes, simulation_state):
        last_total_trades = self.get_last_total_trades(db)
        for minute in range(1, duration_minutes + 1):
            """Check the simulation state before each iteration"""
            with self.minute_lock:  # Use a lock to ensure only one thread accesses the minute
                if self.get_simulation_state(db) == "stopped":
                    break

                profit_loss = self.generate_profit_loss()
                self.update_balance(profit_loss)
                last_total_trades += 1
                self.total_trades = last_total_trades
                self.store_data(simulation_state, db)

                # print(f"{self.name} - Minute {minute}: Balance = ${self.balance:.2f}")
                time.sleep(60)

    def store_data(self, simulation_state, db):
        collection = db[self.name]
        data = {
            "timestamp": int(time.time()),
            "balance": self.balance,
            "total_trades": self.total_trades,
            "simulation_state": simulation_state
        }
        collection.insert_one(data)

    def user_data(self):
        user_datas = {
            "trader_name": self.name,
            "balance": self.balance,
            "trades": self.total_trades,
        }
        return user_datas
    
    def get_last_total_trades(self, db):
        collection = db[self.name]
        document = collection.find_one(sort=[("timestamp", -1)])

        if document:
            return document.get('total_trades', 0)
        else:
            return 0
    
    def get_simulation_state(self, db):
        collection = db[self.name]
        document = collection.find_one(sort=[("timestamp", -1)])
        return document.get('simulation_state', 'stopped')

    def set_simulation_state(self, state, db):
        collection = db[self.name]
        latest_document = collection.find_one(sort=[("timestamp", -1)])

        if latest_document:
            collection.update_one({"_id": latest_document["_id"]}, {'$set': {'simulation_state': state}})
