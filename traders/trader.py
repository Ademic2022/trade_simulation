import uuid
import random
import time

class Trader:
    def __init__(self, name, balance=100.0, simulation_state="stopped"):
        self._id = str(uuid.uuid4())
        self.name = name
        self.balance = balance
        self.total_trades = 0
        self.simulation_state = simulation_state

    def generate_profit_loss(self):
        min_value = -0.10  # -10%
        max_value = 0.10   # +10%
        return random.uniform(min_value, max_value)

    def update_balance(self, profit_loss):
        self.balance += self.balance * profit_loss

    def simulate(self, db, duration_minutes):
        for minute in range(1, duration_minutes + 1):
            """Check the simulation state before each iteration"""
            if self.get_simulation_state(db) == "stopped":
                break

            profit_loss = self.generate_profit_loss()
            self.update_balance(profit_loss)
            self.total_trades += 1
            self.store_data(db)
                
            # print(f"{self.name} - Minute {minute}: Balance = ${self.balance:.2f}")
            time.sleep(60)

    def store_data(self, db):
        collection = db[self.name]
        data = {
            "timestamp": int(time.time()),
            "balance": self.balance,
            "total_trades": self.total_trades,
            "simulation_state": "running"

        }
        collection.insert_one(data)
    def user_data(self):
        user_datas = {
            "trader_name": self.name,
            "balance": self.balance,
            "trades": self.total_trades,
        }
        return user_datas
    
    def get_simulation_state(self, db):
        collection = db[self.name]
        document = collection.find_one(sort=[("timestamp", -1)])
        return document.get('simulation_state', 'stopped')

    def set_simulation_state(self, state, db):
        collection = db[self.name]
        latest_document = collection.find_one(sort=[("timestamp", -1)])

        if latest_document:
            collection.update_one({"_id": latest_document["_id"]}, {'$set': {'simulation_state': state}})

    
