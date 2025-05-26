from itertools import chain
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Value, CharField
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows


@login_required
def inscription_message(request):
    return render(request, 'reviews/inscription_message.html')


@login_required
def dashboard(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    follows = UserFollows.objects.filter(user=request.user)

    followed_users = request.user.following.values_list(
        'followed_user', flat=True
    )

    feed_tickets = Ticket.objects.filter(
        Q(user__in=followed_users) | Q(user=request.user)
    )
    feed_reviews = Review.objects.filter(
        Q(user__in=followed_users) |
        Q(user=request.user) |
        Q(ticket__user=request.user)
    )

    feed_tickets = feed_tickets.annotate(
        content_type=Value('TICKET', CharField())
    )
    feed_reviews = feed_reviews.annotate(
        content_type=Value('REVIEW', CharField())
    )

    posts = sorted(
        chain(feed_tickets, feed_reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'reviews/dashboard.html', {
        'tickets': tickets,
        'reviews': reviews,
        'follows': follows,
        'posts': posts
    })


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('dashboard')
    else:
        form = TicketForm()

    return render(request, 'reviews/ticket_form.html', {'form': form})


@login_required
def create_review(request, ticket_id=None):
    ticket = get_object_or_404(Ticket, id=ticket_id) if ticket_id else None
    # Vérifier si l'utilisateur a déjà posté une critique pour ce ticket
    if ticket and Review.objects.filter(ticket=ticket, user=request.user).exists():
        messages.error(request, "Vous avez déjà publié une critique pour ce billet.")
        return redirect('dashboard')

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(
            request.POST, request.FILES
        ) if not ticket else None

        if review_form.is_valid() and (
            ticket or (ticket_form and ticket_form.is_valid())
        ):
            if not ticket:
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('dashboard')
    else:
        review_form = ReviewForm()
        ticket_form = TicketForm() if not ticket else None

    return render(request, 'reviews/review_form.html', {
        'review_form': review_form,
        'ticket_form': ticket_form,
        'ticket': ticket
    })


@login_required
def follow_user(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        User = get_user_model()

        try:
            followed_user = User.objects.get(username=username)
            if followed_user == request.user:
                error_message = "Vous ne pouvez pas vous suivre vous-même."
            else:
                UserFollows.objects.get_or_create(
                    user=request.user, followed_user=followed_user
                )
                return redirect('subscriptions')
        except User.DoesNotExist:
            error_message = "L'utilisateur n'existe pas."

    return render(
        request, 'reviews/follow_user.html', {'error_message': error_message}
    )


@login_required
def subscriptions(request):
    follows = request.user.following.all()
    return render(request, 'reviews/subscriptions.html', {'follows': follows})


@login_required
def create_ticket_and_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            messages.success(request, "Votre billet et critique ont été publiés !")
            return redirect('dashboard')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'reviews/create_ticket_and_review.html', {
        'ticket_form': ticket_form,
        'review_form': review_form
    })


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre billet a été modifié !")
            return redirect('dashboard')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews/edit_ticket.html', {'form': form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Votre billet a été supprimé !")
        return redirect('dashboard')

    return render(request, 'reviews/confirm_delete.html', {'object': ticket})


@login_required
def unfollow_user(request, follow_id):
    follow = get_object_or_404(UserFollows, id=follow_id, user=request.user)

    if request.method == 'POST':
        follow.delete()
        messages.success(
            request,
            f"Vous ne suivez plus {follow.followed_user.username}"
        )
        return redirect('subscriptions')

    return render(request, 'reviews/confirm_unfollow.html', {'follow': follow})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    form = ReviewForm(request.POST or None, instance=review)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Votre critique a été modifiée !")
        return redirect('dashboard')

    return render(request, 'reviews/review_form.html', {
        'review_form': form,
        'ticket': review.ticket
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Votre critique a été supprimée !")
        return redirect('dashboard')

    return render(request, 'reviews/delete_review_confirm.html', {
        'review': review
    })


@login_required
def user_follow_list(request):
    follows = UserFollows.objects.all()
    return render(request, 'reviews/user_follow_list.html', {'follows': follows})
