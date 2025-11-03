from processors.telemetry import process_telemetry
from processors.motion import process_motion
from processors.lap_data import process_lap_data
# Add other imports...

class PacketRouter:
    def __init__(self, queues, stop_event):
        self.queues = queues
        self.stop_event = stop_event
        self.handlers = {
            0: process_motion,
            2: process_lap_data,
            6: process_telemetry,
            # Add others...
        }

    def get_processor_threads(self):
        threads = []
        for packet_id, handler in self.handlers.items():
            t = threading.Thread(
                target=handler,
                args=(self.queues[packet_id], self.stop_event),
                daemon=True
            )
            threads.append(t)
        return threads
