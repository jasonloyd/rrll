import datetime as dt
import os
import requests
from xml.etree import ElementTree

from random import randrange

from django.db.transaction import atomic, non_atomic_requests

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.shortcuts import get_object_or_404, render, redirect

from django.core.mail import send_mail

from django.http import HttpResponse

from django.utils import timezone

from .forms import SignupForm
from .models import Volunteer, VolunteerStatusMessage
from rrll.settings import (
    BASE_DIR,
    BACKGROUND_CHECK_PASSWORD,
    BACKGROUND_CHECK_USERNAME,
    BACKGROUND_CHECK_URL,
    DEVELOPMENT_MODE,
    EMAIL_HOST_USER,
    SEND_TO_JDP,
)


def home(request):
    return render(
        request,
        "volunteers/home.html",
        {"volunteer_list": Volunteer.objects.order_by("-created_at")},
    )


def success(request):
    return render(request, "volunteers/success.html", {})


def volunteer(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    if volunteer is not None:
        return render(request, "volunteers/volunteer.html", {"volunteer": volunteer})


@non_atomic_requests
def signup(request):
    error_messages = []
    if request.POST:
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            saved_volunteer = form.save()
            subject = "RRLL Volunteer Signup Successful"
            message = (
                request.POST["first_name"]
                + ", thank you for volunteering! You will receive an email from JDP shortly. Check the volunteers page for volunteer status."
            )
            if not DEVELOPMENT_MODE:
                send_mail(
                    subject,
                    message,
                    EMAIL_HOST_USER,
                    [request.POST["email_address"], EMAIL_HOST_USER],
                    True,
                )
            process_signup_payload(saved_volunteer.id)
            return redirect("volunteers:success")
        else:
            form = SignupForm()
            error_messages.append("Invalid captcha entry, please try again.")
    return render(
        request,
        "volunteers/signup.html",
        {"form": SignupForm, "error_messages": error_messages},
    )


@csrf_exempt
@require_POST
@non_atomic_requests
def volunteer_status_webhook(request):
    # TODO Do I need to give them a token? do they require it?
    """
    provided_token = request.headers.get("Jdp-Webhook-Token", "")
    if not compare_digest(provided_token, settings.JDP_WEBHOOK_TOKEN):
        return HttpResponseForbidden(
            "Incorrect token in Jdp-Webhook-Token header.",
            content_type="text/plain",
        )
    """
    VolunteerStatusMessage.objects.filter(
        received_at__lte=timezone.now() - dt.timedelta(days=7)
    ).delete()
    payload = ElementTree.fromstring(request.body)
    VolunteerStatusMessage.objects.create()
    process_webhook_payload(payload)
    return HttpResponse(status=204)


@atomic
def process_webhook_payload(payload):
    order_id = payload.find(".//OrderId")
    order_status = payload.find(".//OrderStatus")
    order_status_flag = order_status.get("flag")
    volunteer_set = Volunteer.objects.filter(order_id=int(order_id.text)).order_by(
        "-created_at"
    )
    if volunteer_set.exists() and "ready" in order_status.text:
        volunteer = volunteer_set.last()
        if order_status_flag.lower() == "true":
            volunteer.background_check_status = "inactive"
        else:
            volunteer.background_check_status = "active"
        volunteer.save()


@atomic
def process_signup_payload(id):
    # TODO may need to set and parse reference id
    if SEND_TO_JDP:
        volunteer = Volunteer.objects.get(id=id)

        order_template_tree = ElementTree.parse(
            os.path.join(BASE_DIR, "rrll/static/assets/digitalforms/order.xml")
        )

        given_name = order_template_tree.find(".//GivenName")
        given_name_orig = given_name.text
        middle_name = order_template_tree.find(".//MiddleName")
        middle_name_orig = middle_name.text
        family_name = order_template_tree.find(".//FamilyName")
        family_name_orig = family_name.text
        email_address = order_template_tree.find(".//EmailAddress")
        email_address_orig = email_address.text

        background_check_root = order_template_tree.getroot()
        original_user_id = background_check_root.get("userId")
        original_password = background_check_root.get("password")

        given_name.text = volunteer.first_name
        middle_name.text = volunteer.middle_name
        family_name.text = volunteer.last_name
        email_address.text = volunteer.email_address
        background_check_root.set("userId", BACKGROUND_CHECK_USERNAME)
        background_check_root.set("password", BACKGROUND_CHECK_PASSWORD)

        headers = {"Content-Type": "application/xml"}  # verify this
        # get post URL from settings
        response = requests.post(
            BACKGROUND_CHECK_URL,
            data=ElementTree.tostring(order_template_tree.getroot()),
            headers=headers,
        )

        # restore orignal values
        given_name.text = given_name_orig
        middle_name.text = middle_name_orig
        family_name.text = family_name_orig
        email_address.text = email_address_orig
        background_check_root.set("userId", original_user_id)
        background_check_root.set("password", original_password)

        if response.ok:
            if not DEVELOPMENT_MODE:
                # assuming order_id is in response
                order_id = response.text.find(".//OrderId")
                volunteer.order_id = int(order_id.text)
            else:
                volunteer.order_id = randrange(1000000)
            volunteer.save()
        else:
            print("Request Error ", response.status_code)
