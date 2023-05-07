from fastapi.testclient import TestClient
from app.main import app
from app.database.models import MRISequence

client = TestClient(app)

# Add test functions for create_sequence, get_sequences, update_sequence, delete_sequence, and search_sequences here