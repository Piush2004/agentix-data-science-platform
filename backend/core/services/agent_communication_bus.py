import uuid
import time
import json
import os
import traceback
from typing import Callable, Dict, Any, List

class Event:
    def __init__(self, topic: str, payload: Dict[str, Any], source: str):
        self.id = str(uuid.uuid4())
        self.topic = topic
        self.payload = payload
        self.source = source
        self.timestamp = time.time()
        self.status = "PENDING"
        self.retry_count = 0

class EventStore:
    def __init__(self):
        self.log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../data/event_store.json")
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self.events = []
        
    def log_event(self, event: Event):
        self.events.append(event)
        self._flush(event)
        
    def update_event(self, event: Event):
        self._flush(event)
        
    def _flush(self, event: Event):
        record = {
            "id": event.id,
            "topic": event.topic,
            "payload": event.payload,
            "source": event.source,
            "timestamp": event.timestamp,
            "status": event.status,
            "retry_count": event.retry_count
        }
        try:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            pass

class DeadLetterQueue:
    def __init__(self):
        self.dlq_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../data/dead_letter_queue.json")
        self.failed_events = []
        
    def push(self, event: Event, error_msg: str):
        self.failed_events.append((event, error_msg))
        record = {
            "event_id": event.id,
            "topic": event.topic,
            "source": event.source,
            "error": error_msg,
            "timestamp": time.time()
        }
        try:
            with open(self.dlq_path, "a") as f:
                f.write(json.dumps(record) + "\n")
        except Exception:
            pass

class MessageBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_store = EventStore()
        self.dlq = DeadLetterQueue()
        self.max_retries = 3
        
    def subscribe(self, topic: str, callback: Callable):
        """
        Registers an agent/function to listen for a specific event topic.
        """
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        
    def publish(self, topic: str, payload: Dict[str, Any], source: str):
        """
        Broadcasts an event payload to all subscribed listeners.
        """
        event = Event(topic, payload, source)
        self.event_store.log_event(event)
        
        if topic not in self.subscribers:
            event.status = "UNROUTED"
            self.event_store.update_event(event)
            return
            
        handlers = self.subscribers[topic]
        for handler in handlers:
            success = self._execute_with_retry(handler, event)
            if not success:
                # Note: For multiple subscribers, if one fails we continue broadcasting to others.
                pass
                
    def _execute_with_retry(self, handler: Callable, event: Event) -> bool:
        """
        Executes the handler with exponential backoff / retry limit.
        """
        while event.retry_count <= self.max_retries:
            try:
                handler(event.payload)
                event.status = "SUCCESS"
                self.event_store.update_event(event)
                return True
            except Exception as e:
                event.retry_count += 1
                error_trace = traceback.format_exc()
                if event.retry_count > self.max_retries:
                    event.status = "FAILED"
                    self.event_store.update_event(event)
                    self.dlq.push(event, error_trace)
                    return False
                time.sleep(0.01) # Small backoff for testing
        return False
        
    def get_metrics(self) -> Dict[str, int]:
        """
        Returns basic monitoring telemetry for the Event Bus.
        """
        total = len(self.event_store.events)
        failed = len(self.dlq.failed_events)
        retried = sum(1 for e in self.event_store.events if e.retry_count > 0)
        unrouted = sum(1 for e in self.event_store.events if e.status == "UNROUTED")
        success = sum(1 for e in self.event_store.events if e.status == "SUCCESS")
        
        return {
            "total_events": total,
            "success_events": success,
            "failed_events": failed,
            "unrouted_events": unrouted,
            "retried_events": retried
        }

agent_bus = MessageBus()
