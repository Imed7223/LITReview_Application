from itertools import chain
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Value, CharField
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows
from .models import BlockedUser


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
    user = request.user

    
    # utilisateurs que tu suis
    followed_users = UserFollows.objects.filter(user=user)

    # utilisateurs qui te suivent
    followers = UserFollows.objects.filter(followed_user=user)

    # utilisateurs que tu as bloqués
    blocked_users = BlockedUser.objects.filter(blocker=user)
    blocked_ids = blocked_users.values_list('blocked__id', flat=True)

    # utilisateurs qui t’ont bloqué
    blocked_by_others = BlockedUser.objects.filter(blocked=user)

    # on filtre pour ne pas afficher ceux que tu as déjà bloqués
    followers_not_blocked = followers.exclude(user__id__in=blocked_ids)
    #passer la liste des IDs bloqués
    blocked_user_ids = BlockedUser.objects.filter(blocker=request.user).values_list('blocked__id', flat=True)

    return render(request, 'reviews/dashboard.html', {
        'tickets': tickets,
        'reviews': reviews,
        'follows': follows,
        'posts': posts,
        'followed_users': followed_users,
        'followers': followers_not_blocked,
        'blocked_users': blocked_users,
        'blocked_by_others': blocked_by_others
    })


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Votre billet a été publié !")
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
            messages.success(request, "Votre critique a été publié !")
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
            elif BlockedUser.objects.filter(blocker=followed_user, blocked=request.user).exists():
                error_message = f"{followed_user.username} vous a bloqué. Vous ne pouvez pas le suivre."
            elif BlockedUser.objects.filter(blocker=request.user, blocked=followed_user).exists():
                error_message = f"Vous avez bloqué {followed_user.username}. Débloquez-le avant de le suivre."
            else:
                already_following = UserFollows.objects.filter(
                    user=request.user, followed_user=followed_user
                ).exists()

                if already_following:
                    messages.info(
                        request,
                        f"Vous suivez déjà {followed_user.username}."
                    )
                else:
                    UserFollows.objects.get_or_create(
                        user=request.user, followed_user=followed_user
                    )
                    messages.success(
                        request,
                        f"Vous suivez {followed_user.username}"
                    )

                return redirect('dashboard')
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
        return redirect('dashboard')

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


@login_required
def block_user(request, user_id):
    User = get_user_model()
    blocked_user = get_object_or_404(User, id=user_id)
    # Empêche de bloquer soi-même
    if blocked_user == request.user:
        return redirect('dashboard')
    # Crée la relation de blocage si elle n’existe pas
    BlockedUser.objects.get_or_create(blocker=request.user, blocked=blocked_user)
    # Supprimer la relation de suivi si elle existe
    UserFollows.objects.filter(user=request.user, followed_user=blocked_user).delete()
    messages.success(request, f"Vous avez débloqué l'utilisateur {blocked_user.username} !")
    return redirect('dashboard')

def unblock_user(request, user_id):
    User = get_user_model()
    user_to_unblock = User.objects.get(id=user_id)
    BlockedUser.objects.filter(blocker=request.user, blocked=user_to_unblock).delete()
    messages.success(request, f"Vous avez débloqué l'utilisateur {user_to_unblock.username} !")

    return redirect('dashboard')

@login_required
def user_list(request):
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)
    # Récupère les ID des utilisateurs que request.user a bloqués
    blocked_user_ids = request.user.blocked_users.values_list('blocked_id', flat=True)
    return render(request, 'reviews/dashboard.html', {
        'user_list': users,
        'blocked_user_ids': blocked_user_ids,
    })
