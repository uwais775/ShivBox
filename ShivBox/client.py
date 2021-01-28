
class Client():
    def update(self, activity):
        current_time = time.time()
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "activity": activity,
                "pid": os.getpid()
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        print("sending data")
        sent = self.send_data(1, payload)
        self.loop.run_until_complete(self.read_output())

    def close(self):
        self.sock_writer.close()
        self.loop.close()

    def start(self):
        self.loop.run_until_complete(self.handshake())
