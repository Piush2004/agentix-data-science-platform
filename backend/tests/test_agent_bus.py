import pytest
from core.services.agent_communication_bus import MessageBus

@pytest.fixture
def bus():
    return MessageBus()

def test_subscribe_and_publish_success(bus):
    received = []
    
    def on_dataset_uploaded(payload):
        received.append(payload["filename"])
        
    bus.subscribe("DatasetUploaded", on_dataset_uploaded)
    bus.publish("DatasetUploaded", {"filename": "sales.csv"}, source="Dataset Agent")
    
    assert len(received) == 1
    assert received[0] == "sales.csv"
    
    metrics = bus.get_metrics()
    assert metrics["success_events"] == 1
    assert metrics["failed_events"] == 0

def test_unrouted_event(bus):
    bus.publish("GhostEvent", {}, source="Unknown")
    
    metrics = bus.get_metrics()
    assert metrics["unrouted_events"] == 1

def test_retry_and_dead_letter_queue(bus):
    attempts = []
    
    def faulty_handler(payload):
        attempts.append(1)
        raise ValueError("Simulated handler crash")
        
    bus.subscribe("EDACompleted", faulty_handler)
    bus.publish("EDACompleted", {"status": "done"}, source="EDA Agent")
    
    # 1 initial attempt + 3 retries = 4 attempts total
    assert len(attempts) == 4
    
    metrics = bus.get_metrics()
    assert metrics["failed_events"] == 1
    assert metrics["retried_events"] == 1
    
    # Check DLQ
    assert len(bus.dlq.failed_events) == 1
    failed_event, error = bus.dlq.failed_events[0]
    assert failed_event.topic == "EDACompleted"
    assert "Simulated handler crash" in error
