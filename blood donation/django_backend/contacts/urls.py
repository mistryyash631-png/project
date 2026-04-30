from django.urls import path

from . import views

urlpatterns = [
    path("api/contact/", views.api_contact, name="api_contact"),
    path("api/contacts/", views.api_contacts, name="api_contacts"),
    path("contacts/", views.contacts_list, name="contacts_list"),
    path("", views.frontend_page, name="home"),
    path("index.html", views.frontend_page, {"page_slug": "index.html"}, name="index_html"),
    path("Contact.html", views.frontend_page, {"page_slug": "contact.html"}, name="contact_html"),
    path(
        "register as donor.html",
        views.frontend_page,
        {"page_slug": "register-as-donor.html"},
        name="register_as_donor_html",
    ),
    path(
        "Request Blood.html",
        views.frontend_page,
        {"page_slug": "request-blood.html"},
        name="request_blood_html",
    ),
    path("find donor.html", views.frontend_page, {"page_slug": "find-donor.html"}, name="find_donor_html"),
    path("admin panel.html", views.frontend_page, {"page_slug": "admin-panel.html"}, name="admin_panel_html"),
    path("<slug:page_slug>/", views.frontend_page, name="frontend_page_slug"),
]
