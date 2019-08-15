import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import app
import pdb
import random
import xml.etree.ElementTree as ET
from common import conditional_map

@pytest.fixture
def client():
    return app.app.test_client()

def test_subject_query(client):
    data = client.get('/scores?subject=Math').get_json()
    assert all([
                len(data['schools']) > 0, 
                len(data['scores']['black']) == len(data['schools']), 
                ('scores' in data and 'schools' in data)
            ])

def test_school_query(client):
    data = client.get('/scores?school=Essex Street Academy').get_json()
    assert all([
                data['math'] == 395.0, 
                data['writing'] == 387.0, 
                data['reading'] == 411.0
            ])

def test_matrix_query(client):
    data = client.get('/matrix')
    element = ET.fromstring(data.data)
    assert 'svg' in element.tag

def test_score_filter_query(client):
    score = str(random.randint(350, 800))
    conditional = random.choice(list(conditional_map.keys()))
    subject = random.choice(['Math', 'Reading', 'Writing'])
    url = f"/scores?subject={subject}&score={score}&conditional={conditional}"
    data = client.get(url).get_json()['scores']
    data =  data[random.choice(list(data.keys()))]
    assert all(eval(f"{s['y']} {conditional_map[conditional]} {float(score)}") for s in data)