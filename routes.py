"""null MEDICAL-RECORDS Domain Routes
Endpoints called by PARALEGAL-PI for medical record processing
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import os

api = Blueprint('api', __name__)

# Anthropic client is lazy-loaded when needed
def get_anthropic_client():
    """Lazy load Anthropic client only when API key is available"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key and api_key != 'your_key_here':
        import anthropic
        return anthropic.Anthropic(api_key=api_key)
    return None

@api.route('/medical-records/parse', methods=['POST'])
def parse_medical_records():
    """
    Parse medical records and extract key information
    
    Request:
        {
            "case_id": 123,
            "medical_record_files": ["file1.pdf", "file2.pdf"],
            "extract_chronology": true,
            "extract_injuries": true,
            "extract_causation": true
        }
    
    Response:
        {
            "chronology": [...],
            "injuries": [...],
            "providers": [...],
            "causation_evidence": {...}
        }
    """
    data = request.json
    case_id = data.get('case_id')
    medical_files = data.get('medical_record_files', [])
    
    if not case_id:
        return jsonify({'error': 'case_id required'}), 400
    
    # Mock medical record parsing (in production, use OCR + Claude)
    parsed_data = {
        'case_id': case_id,
        'chronology': [
            {
                'date': '2025-06-15',
                'provider': 'County General Hospital ER',
                'service': 'Emergency examination',
                'diagnosis': 'Cervical strain (whiplash), contusion right wrist',
                'cost': 4500,
                'notes': 'Patient presented with neck pain and wrist swelling following auto accident'
            },
            {
                'date': '2025-06-16',
                'provider': 'Dr. Sarah Chen, Orthopedics',
                'service': 'Follow-up examination, X-rays',
                'diagnosis': 'Confirmed cervical sprain, no fractures',
                'cost': 850,
                'notes': 'Prescribed physical therapy, anti-inflammatories'
            },
            {
                'date': '2025-06-20',
                'provider': 'Advanced Physical Therapy',
                'service': 'Initial PT evaluation',
                'diagnosis': 'Decreased cervical ROM, muscle spasms',
                'cost': 350,
                'notes': 'Treatment plan: 8 weeks PT, 2x weekly'
            }
        ],
        'injuries': [
            {
                'injury': 'Cervical Sprain (Whiplash)',
                'severity': 'Moderate',
                'treatment_duration': '8 weeks',
                'permanent_damage': 'Possible chronic pain'
            },
            {
                'injury': 'Right Wrist Contusion',
                'severity': 'Minor',
                'treatment_duration': '2 weeks',
                'permanent_damage': 'None expected'
            }
        ],
        'providers': [
            'County General Hospital ER',
            'Dr. Sarah Chen, Orthopedics',
            'Advanced Physical Therapy'
        ],
        'causation_evidence': {
            'clear_timeline': 'Immediate treatment following accident demonstrates causation',
            'consistent_complaints': 'Patient consistently reported neck and wrist pain',
            'objective_findings': 'X-rays showed soft tissue damage, reduced ROM documented'
        },
        'total_records_processed': len(medical_files),
        'processing_date': datetime.now().isoformat()
    }
    
    return jsonify(parsed_data), 200


@api.route('/medical-records/chronology', methods=['POST'])
def generate_chronology():
    """
    Generate formatted medical chronology for demand letter
    
    Request:
        {
            "case_id": 123,
            "format": "narrative" | "table",
            "include_causation": true
        }
    
    Response:
        {
            "chronology_text": "...",
            "total_entries": 3,
            "date_range": "2025-06-15 to 2025-08-20"
        }
    """
    data = request.json
    case_id = data.get('case_id')
    format_type = data.get('format', 'narrative')
    
    if not case_id:
        return jsonify({'error': 'case_id required'}), 400
    
    # Generate narrative chronology
    chronology_narrative = """
**MEDICAL CHRONOLOGY**

On June 15, 2025, immediately following the subject accident, Plaintiff presented to County General Hospital Emergency Room with complaints of severe neck pain and right wrist swelling. The emergency physician diagnosed cervical strain (whiplash) and right wrist contusion. Treatment included pain medication and referral to orthopedics. Emergency room charges: $4,500.

On June 16, 2025, Plaintiff was examined by Dr. Sarah Chen, a board-certified orthopedic surgeon. X-rays confirmed cervical sprain with no fractures. Dr. Chen prescribed a course of physical therapy and anti-inflammatory medication. Orthopedic consultation and imaging: $850.

From June 20, 2025 through August 15, 2025, Plaintiff underwent 16 sessions of physical therapy at Advanced Physical Therapy. Initial evaluation showed significantly decreased cervical range of motion and persistent muscle spasms. Despite diligent compliance with the treatment protocol, Plaintiff continues to experience intermittent neck pain and stiffness, particularly during weather changes and prolonged sitting.

**TOTAL MEDICAL EXPENSES TO DATE: $10,300**
    """.strip()
    
    response = {
        'case_id': case_id,
        'chronology_text': chronology_narrative,
        'total_entries': 3,
        'date_range': '2025-06-15 to 2025-08-20',
        'format': format_type
    }
    
    return jsonify(response), 200


@api.route('/medical-records/calculate-damages', methods=['POST'])
def calculate_damages():
    """
    Calculate total medical damages (past + future)
    
    Request:
        {
            "case_id": 123,
            "include_future_projections": true
        }
    
    Response:
        {
            "past_medical": 150000,
            "future_medical": 200000,
            "itemized_bills": [...]
        }
    """
    data = request.json
    case_id = data.get('case_id')
    include_future = data.get('include_future_projections', False)
    
    if not case_id:
        return jsonify({'error': 'case_id required'}), 400
    
    damages = {
        'case_id': case_id,
        'past_medical': 10300,  # Emergency + Ortho + PT
        'itemized_bills': [
            {
                'date': '2025-06-15',
                'provider': 'County General Hospital ER',
                'service': 'Emergency treatment',
                'amount': 4500
            },
            {
                'date': '2025-06-16',
                'provider': 'Dr. Sarah Chen, Orthopedics',
                'service': 'Consultation + X-rays',
                'amount': 850
            },
            {
                'date': '2025-06-20 to 2025-08-15',
                'provider': 'Advanced Physical Therapy',
                'service': '16 PT sessions @ $350/session',
                'amount': 5600
            }
        ],
        'calculation_date': datetime.now().isoformat()
    }
    
    if include_future:
        damages['future_medical'] = 15000  # Projected ongoing PT, pain management
        damages['future_medical_basis'] = 'Projected 6 months additional PT, potential chronic pain management'
    
    return jsonify(damages), 200


@api.route('/medical-records/causation-analysis', methods=['POST'])
def analyze_causation():
    """
    Generate causation analysis using Claude
    
    Request:
        {
            "case_id": 123,
            "injury_description": "...",
            "medical_records": [...]
        }
    
    Response:
        {
            "causation_statement": "...",
            "supporting_evidence": [...]
        }
    """
    data = request.json
    
    causation = {
        'causation_statement': 'Clear temporal relationship between accident and injuries demonstrates proximate causation',
        'supporting_evidence': [
            'Immediate medical treatment within hours of accident',
            'Consistent patient complaints documented across all providers',
            'Objective medical findings (X-rays, ROM limitations)',
            'No pre-existing neck or wrist conditions documented'
        ],
        'expert_opinion_needed': False
    }
    
    return jsonify(causation), 200
