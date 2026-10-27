from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title='NivaranX API', description='Demo API for integrated institution complaint monitoring.', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
Status = Literal['Registered', 'Under Review', 'Assigned', 'Action Required', 'Resolved', 'Closed']

class Action(BaseModel):
    timestamp: datetime
    actor: str
    action: str
    notes: str

class Complaint(BaseModel):
    complaint_id: str
    institution_id: str
    institution_name: str
    bureau: str
    category: str
    subject: str
    description: str
    received_at: datetime
    assigned_to: str | None
    status: Status
    sla_deadline: datetime
    actions: list[Action] = Field(default_factory=list)

class Institution(BaseModel):
    permanent_id: str
    name: str
    location: str
    institution_type: str
    complaints_count: int
    open_count: int

class StatusUpdate(BaseModel):
    status: Status
    actor: str = Field(min_length=1, max_length=100)
    notes: str = Field(min_length=3, max_length=1000)

now = datetime.now(timezone.utc)
institutions = [
    Institution(permanent_id='1-1234567890', name='Central Institute of Technology', location='Indore, Madhya Pradesh', institution_type='Engineering', complaints_count=4, open_count=3),
    Institution(permanent_id='1-0987654321', name='North Valley College of Engineering', location='Bhopal, Madhya Pradesh', institution_type='Engineering', complaints_count=3, open_count=1),
    Institution(permanent_id='1-2468013579', name='Riverfront Institute of Management', location='Jabalpur, Madhya Pradesh', institution_type='Management', complaints_count=2, open_count=1),
]
complaints: list[Complaint] = [
    Complaint(complaint_id='NVX-2026-001', institution_id='1-1234567890', institution_name='Central Institute of Technology', bureau='Regulation Bureau', category='Faculty Compliance', subject='Faculty qualification and strength review', description='A submission alleges that the institution faculty strength may not meet applicable requirements.', received_at=now-timedelta(days=12), assigned_to='R. Sharma', status='Under Review', sla_deadline=now+timedelta(days=2), actions=[Action(timestamp=now-timedelta(days=12), actor='Intake Desk', action='Registered', notes='Synthetic demo complaint received.'), Action(timestamp=now-timedelta(days=10), actor='R. Sharma', action='Assigned', notes='Assigned for initial review.')]),
    Complaint(complaint_id='NVX-2026-002', institution_id='1-1234567890', institution_name='Central Institute of Technology', bureau='Public Grievance Redressal Cell', category='Faculty Compliance', subject='Concern regarding faculty availability', description='A grievance states that the college may have insufficient qualified faculty members.', received_at=now-timedelta(days=9), assigned_to='A. Verma', status='Assigned', sla_deadline=now+timedelta(days=1), actions=[Action(timestamp=now-timedelta(days=9), actor='PGRC Intake', action='Registered', notes='Synthetic demo grievance received.'), Action(timestamp=now-timedelta(days=8), actor='A. Verma', action='Assigned', notes='Assigned to grievance review queue.')]),
    Complaint(complaint_id='NVX-2026-003', institution_id='1-1234567890', institution_name='Central Institute of Technology', bureau='Regulation Bureau', category='Document Verification', subject='Verification of compliance documents', description='Review the institution recently submitted compliance documents.', received_at=now-timedelta(days=25), assigned_to='S. Khan', status='Action Required', sla_deadline=now-timedelta(days=3), actions=[Action(timestamp=now-timedelta(days=25), actor='Intake Desk', action='Registered', notes='Synthetic demo complaint received.'), Action(timestamp=now-timedelta(days=15), actor='S. Khan', action='Evidence requested', notes='Awaiting supporting documents.')]),
    Complaint(complaint_id='NVX-2026-004', institution_id='1-0987654321', institution_name='North Valley College of Engineering', bureau='Public Grievance Redressal Cell', category='Student Services', subject='Delay in issuing student documents', description='Students report delays in issuing requested academic documents.', received_at=now-timedelta(days=6), assigned_to='M. Patel', status='Resolved', sla_deadline=now+timedelta(days=4), actions=[Action(timestamp=now-timedelta(days=6), actor='PGRC Intake', action='Registered', notes='Synthetic demo grievance received.'), Action(timestamp=now-timedelta(days=1), actor='M. Patel', action='Resolved', notes='Resolution recorded in synthetic demo data.')]),
    Complaint(complaint_id='NVX-2026-005', institution_id='1-2468013579', institution_name='Riverfront Institute of Management', bureau='Academic Bureau', category='Course Approval', subject='Clarification on course approval status', description='Request for clarification regarding a course approval record.', received_at=now-timedelta(days=4), assigned_to=None, status='Registered', sla_deadline=now+timedelta(days=5), actions=[Action(timestamp=now-timedelta(days=4), actor='Intake Desk', action='Registered', notes='Synthetic demo complaint received.')]),
]

def is_open(item: Complaint) -> bool:
    return item.status not in ('Resolved', 'Closed')

@app.get('/api/health')
def health():
    return {'status': 'ok', 'project': 'NivaranX', 'mode': 'demo', 'data': 'synthetic'}

@app.get('/api/dashboard')
def dashboard():
    total = len(complaints)
    current = datetime.now(timezone.utc)
    open_cases = [c for c in complaints if is_open(c)]
    resolved = [c for c in complaints if c.status in ('Resolved', 'Closed')]
    bureaus: dict[str, dict[str, int]] = {}
    for item in complaints:
        metrics = bureaus.setdefault(item.bureau, {'total': 0, 'open': 0, 'overdue': 0})
        metrics['total'] += 1
        metrics['open'] += int(is_open(item))
        metrics['overdue'] += int(is_open(item) and item.sla_deadline < current)
    return {'total_complaints': total, 'open_complaints': len(open_cases), 'overdue_complaints': sum(1 for c in open_cases if c.sla_deadline < current), 'resolved_complaints': len(resolved), 'disposal_rate': round(len(resolved)/total*100, 1) if total else 0, 'bureau_metrics': [{'bureau': key, **value} for key, value in bureaus.items()]}

@app.get('/api/institutions', response_model=list[Institution])
def list_institutions(search: str | None = Query(default=None, min_length=1)):
    return [i for i in institutions if not search or search.casefold() in i.name.casefold() or search.casefold() in i.permanent_id.casefold()]

@app.get('/api/institutions/{permanent_id}')
def institution_profile(permanent_id: str):
    institution = next((i for i in institutions if i.permanent_id == permanent_id), None)
    if not institution:
        raise HTTPException(status_code=404, detail='Institution not found')
    return {'institution': institution, 'complaints': [c for c in complaints if c.institution_id == permanent_id]}

@app.get('/api/complaints', response_model=list[Complaint])
def list_complaints(search: str | None = None, status: Status | None = None, bureau: str | None = None, overdue_only: bool = False):
    result = complaints
    if search:
        q = search.casefold()
        result = [c for c in result if any(q in v.casefold() for v in (c.complaint_id, c.institution_name, c.institution_id, c.subject, c.category, c.bureau))]
    if status:
        result = [c for c in result if c.status == status]
    if bureau:
        result = [c for c in result if c.bureau == bureau]
    if overdue_only:
        current = datetime.now(timezone.utc)
        result = [c for c in result if is_open(c) and c.sla_deadline < current]
    return result

@app.get('/api/complaints/{complaint_id}', response_model=Complaint)
def get_complaint(complaint_id: str):
    item = next((c for c in complaints if c.complaint_id == complaint_id), None)
    if not item:
        raise HTTPException(status_code=404, detail='Complaint not found')
    return item

@app.patch('/api/complaints/{complaint_id}/status', response_model=Complaint)
def update_complaint_status(complaint_id: str, update: StatusUpdate):
    item = next((c for c in complaints if c.complaint_id == complaint_id), None)
    if not item:
        raise HTTPException(status_code=404, detail='Complaint not found')
    item.status = update.status
    item.actions.append(Action(timestamp=datetime.now(timezone.utc), actor=update.actor, action=f'Status changed to {update.status}', notes=update.notes))
    return item

@app.get('/api/duplicates')
def duplicate_candidates():
    by_id = {c.complaint_id: c for c in complaints}
    pairs = [('NVX-2026-001', 'NVX-2026-002', 0.87, ['Same institution Permanent ID', 'Same complaint category', 'Similar faculty-related wording'])]
    return [{'complaint_a': by_id[a], 'complaint_b': by_id[b], 'demo_similarity_score': score, 'matching_reasons': reasons, 'review_status': 'Needs human review'} for a, b, score, reasons in pairs]

@app.get('/api/analytics/aging')
def case_aging():
    current = datetime.now(timezone.utc)
    buckets = {'0–7 days': 0, '8–14 days': 0, '15–30 days': 0, '31+ days': 0}
    for item in [c for c in complaints if is_open(c)]:
        age = max(0, (current - item.received_at).days)
        key = '0–7 days' if age <= 7 else '8–14 days' if age <= 14 else '15–30 days' if age <= 30 else '31+ days'
        buckets[key] += 1
    return [{'bucket': key, 'count': value} for key, value in buckets.items()]
