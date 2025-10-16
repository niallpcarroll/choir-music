from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower
from django.views.decorators.http import require_POST
from datetime import datetime

from .models import MusicPiece
from .forms import ContactForm, CustomUserCreationForm


# --- Registration Form ---
def register_view(request):
    if request.user.is_authenticated:
        return redirect("landing_page")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # inactive until admin approval
            user.save()

            # Send HTML notification email to admin
            subject = "New User Registration Pending Approval"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.DEFAULT_FROM_EMAIL]
            text_content = (
                f"A new user has registered and requires approval:\n\n"
                f"Username: {user.username}\n"
                f"Email: {user.email}\n\n"
                f"Please review and activate the account in the admin panel."
            )
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color:#f0f0f0; padding:20px;">
                <div style="max-width:600px; margin:auto; background-color:#ffffff; border-radius:10px; padding:20px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
                    <h2 style="color:#0b3d91;">New User Registration</h2>
                    <p style="font-size:16px; color:#333333;">
                        A new user has registered and requires approval:
                    </p>
                    <ul style="font-size:16px; color:#333333;">
                        <li><strong>Username:</strong> {user.username}</li>
                        <li><strong>Email:</strong> {user.email}</li>
                    </ul>
                    <p style="font-size:16px; color:#333333;">
                        Please review and activate the account in the admin panel.
                    </p>
                </div>
            </body>
            </html>
            """
            email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

            current_year = datetime.now().year
            return render(
                request,
                "music/register_success.html",
                {"username": user.username, "current_year": current_year},
            )
    else:
        form = CustomUserCreationForm()

    current_year = datetime.now().year
    return render(
        request, "music/register.html", {"form": form, "current_year": current_year}
    )


# --- Login Page ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect("landing_page")

    inactive_user = False

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect("landing_page")
            else:
                inactive_user = True
        else:
            messages.error(request, "Invalid username or password.")

    current_year = datetime.now().year
    return render(
        request,
        "music/login.html",
        {"inactive_user": inactive_user, "current_year": current_year},
    )


# --- Logout Page ---
def logout_view(request):
    logout(request)
    return redirect("login")


# --- Contact Page (Public) ---
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(
                subject=f"Contact Form Message from {name}",
                message=f"From: {name} <{email}>\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            current_year = datetime.now().year
            return render(
                request,
                "music/contact_success.html",
                {"name": name, "current_year": current_year},
            )
    else:
        form = ContactForm()

    current_year = datetime.now().year
    return render(
        request, "music/contact.html", {"form": form, "current_year": current_year}
    )


# --- Protected Pages ---
@login_required
def landing_page(request):
    query = request.GET.get("q", "")
    letter = request.GET.get("letter", "")
    # Case-insensitive ordering
    pieces = MusicPiece.objects.all().order_by(Lower("title"))

    # Search filter
    if query:
        pieces = pieces.filter(Q(title__icontains=query) | Q(composer__icontains=query))

    # Alphabet filter
    if letter:
        pieces = pieces.filter(title__istartswith=letter)

    # Prepare unique part initials for yellow circles in landing.html
    for piece in pieces:
        parts_list = []
        for rec in piece.recordings.all():  # includes full-piece + movement recordings
            if rec.part:
                part_lower = rec.part.lower()
                if "soprano" in part_lower and "alto" in part_lower:
                    part_initial = "S/A"
                elif "tenor" in part_lower and "bass" in part_lower:
                    part_initial = "T/B"
                elif part_lower == "choir":
                    part_initial = "Ch"
                else:
                    part_initial = rec.part[0].upper()

                if part_initial not in parts_list:
                    parts_list.append(part_initial)
        piece.unique_parts = parts_list

    current_year = datetime.now().year
    return render(
        request,
        "music/landing.html",
        {
            "pieces": pieces,
            "query": query,
            "letter": letter,
            "current_year": current_year,
        },
    )


@login_required
def piece_detail(request, piece_id):
    piece = get_object_or_404(MusicPiece, pk=piece_id)

    # Full-piece recordings: recordings without a movement
    full_recordings = piece.recordings.filter(movement__isnull=True)

    # Movements for this piece
    movements = piece.movements.all()

    current_year = datetime.now().year
    return render(
        request,
        "music/music_detail.html",
        {
            "piece": piece,
            "full_recordings": full_recordings,
            "movements": movements,
            "has_full_recordings": full_recordings.exists(),  # <-- pass boolean
            "current_year": current_year,
        },
    )


@login_required
def home(request):
    current_year = datetime.now().year
    return render(request, "music/home.html", {"current_year": current_year})


# --- Delete Account ---
@login_required
def delete_account_confirm(request):
    """Show confirmation page before account deletion."""
    current_year = datetime.now().year
    return render(
        request,
        "music/delete_account_confirm.html",
        {"current_year": current_year},
    )


@login_required
@require_POST
def delete_account(request):
    """Delete the user's account and log them out."""
    user = request.user
    logout(request)
    user.delete()

    current_year = datetime.now().year
    return render(
        request,
        "music/delete_account_success.html",
        {"current_year": current_year},
    )


# --- Useful Links Page (Public) ---
def useful_links(request):
    """Display the 'Other Useful Links' page."""
    current_year = datetime.now().year
    return render(request, "music/useful_links.html", {"current_year": current_year})
