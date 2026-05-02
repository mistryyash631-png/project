import json
from pathlib import Path
from datetime import date

from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import BloodRequest, ContactMessage

FRONTEND_DIR = Path(__file__).resolve().parents[2]
FRONTEND_PAGES = {
    "index.html": "index.html",
    "contact.html": "Contact.html",
    "register-as-donor.html": "register as donor.html",
    "request-blood.html": "Request Blood.html",
    "find-donor.html": "find donor.html",
    "admin-panel.html": "admin panel.html",
}


def contacts_list(request: HttpRequest):
    messages = ContactMessage.objects.all()[:500]
    return render(request, "contacts/list.html", {"messages": messages})


def frontend_page(_request: HttpRequest, page_slug: str = "index.html"):
    filename = FRONTEND_PAGES.get(page_slug.lower())
    if not filename:
        raise Http404("Page not found.")

    file_path = FRONTEND_DIR / filename
    if not file_path.exists():
        raise Http404("Page not found.")

    return HttpResponse(file_path.read_text(encoding="utf-8"), content_type="text/html")


def api_contacts(_request: HttpRequest):
    rows = list(
        ContactMessage.objects.values(
            "id", "name", "contact", "subject", "message", "created_at"
        )[:1000]
    )
    return JsonResponse({"success": True, "data": rows})


@csrf_exempt
def api_contact(request: HttpRequest):
    if request.method == "GET":
        rows = list(
            ContactMessage.objects.values(
                "id", "name", "contact", "subject", "message", "created_at"
            )[:1000]
        )
        return JsonResponse({"success": True, "data": rows})

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Only GET and POST methods are allowed."},
            status=405,
        )

    name = ""
    contact = ""
    subject = "General Enquiry"
    message = ""

    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            payload = {}
        name = str(payload.get("name", "")).strip()
        contact = str(payload.get("contact", "")).strip()
        subject = str(payload.get("subject", subject)).strip() or subject
        message = str(payload.get("message", "")).strip()
    else:
        # Handles x-www-form-urlencoded (your HTML uses this)
        name = str(request.POST.get("name", "")).strip()
        contact = str(request.POST.get("contact", "")).strip()
        subject = str(request.POST.get("subject", subject)).strip() or subject
        message = str(request.POST.get("message", "")).strip()

    if not name or not contact or not message:
        return JsonResponse(
            {
                "success": False,
                "message": "Name, contact, and message are required.",
            },
            status=422,
        )

    ContactMessage.objects.create(
        name=name, contact=contact, subject=subject, message=message
    )
    return JsonResponse({"success": True, "message": "Contact message saved."})


@csrf_exempt
def api_blood_requests(request: HttpRequest):
    if request.method == "GET":
        rows = list(
            BloodRequest.objects.values(
                "request_id",
                "patient_name",
                "patient_age",
                "hospital",
                "ward",
                "blood_group",
                "units_required",
                "required_by_date",
                "contact_phone",
                "urgency",
                "notes",
                "status",
                "user_email",
                "created_at",
            )[:1000]
        )
        return JsonResponse({"success": True, "data": rows})

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Only GET and POST methods are allowed."},
            status=405,
        )

    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            payload = {}
    else:
        payload = request.POST

    request_id = str(payload.get("request_id", "")).strip()
    patient_name = str(payload.get("patient_name", "")).strip()
    hospital = str(payload.get("hospital", "")).strip()
    blood_group = str(payload.get("blood_group", "")).strip()
    contact_phone = str(payload.get("contact_phone", "")).strip()
    urgency = str(payload.get("urgency", "Medium")).strip() or "Medium"
    status = str(payload.get("status", "Open")).strip() or "Open"
    notes = str(payload.get("notes", "")).strip()
    ward = str(payload.get("ward", "")).strip()
    user_email = str(payload.get("user_email", "")).strip()

    patient_age_raw = str(payload.get("patient_age", "")).strip()
    units_raw = str(payload.get("units_required", "1")).strip()
    required_by_date_raw = str(payload.get("required_by_date", "")).strip()

    if not all([request_id, patient_name, hospital, blood_group, contact_phone]):
        return JsonResponse(
            {
                "success": False,
                "message": "request_id, patient_name, hospital, blood_group, and contact_phone are required.",
            },
            status=422,
        )

    try:
        units_required = max(1, int(units_raw))
    except (TypeError, ValueError):
        units_required = 1

    patient_age = None
    if patient_age_raw:
        try:
            patient_age = max(0, int(patient_age_raw))
        except (TypeError, ValueError):
            patient_age = None

    required_by_date = None
    if required_by_date_raw:
        try:
            required_by_date = date.fromisoformat(required_by_date_raw)
        except ValueError:
            required_by_date = None

    obj, created = BloodRequest.objects.update_or_create(
        request_id=request_id,
        defaults={
            "patient_name": patient_name,
            "patient_age": patient_age,
            "hospital": hospital,
            "ward": ward,
            "blood_group": blood_group,
            "units_required": units_required,
            "required_by_date": required_by_date,
            "contact_phone": contact_phone,
            "urgency": urgency if urgency in {"High", "Medium", "Low"} else "Medium",
            "notes": notes,
            "status": status if status in {"Open", "In Progress", "Closed"} else "Open",
            "user_email": user_email,
        },
    )
    return JsonResponse(
        {
            "success": True,
            "message": "Blood request saved.",
            "created": created,
            "request_id": obj.request_id,
        }
    )
