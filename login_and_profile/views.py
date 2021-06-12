import re
from .models import Invite, User, Item, Invite, House, Balance, Notification
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

################### Login Methods ###################


def index(request):
    return render(request, "login.html")

# not redirecting to /profile


def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validation(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        Notification.objects.create(receiver=new_user, action="REGISTERED")
        request.session.clear()
        request.session['user_id'] = new_user.id
        request.session['first_name'] = new_user.first_name
        return redirect('/profile')


def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session.clear()
    request.session['user_id'] = user.id
    request.session['first_name'] = user.first_name
    return redirect('/profile')


def logout(request):
    request.session.clear()
    return redirect('/')


################### Profile Methods ###################

def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': this_user,
    }
    # add if statement to redirect to main_house if existing?
    return render(request, 'profile.html', context)


def create_house(request):
    if request.method == "GET":
        return redirect('/profile')
    # validate house name length
    if len(request.POST['nickname']) < 2:
        e = "House nickname must be at least 2 characters."
        messages.error(request, e)
        return redirect('/profile')
    this_user = User.objects.get(id=request.session['user_id'])
    new_house = House.objects.create(
        nickname=request.POST['nickname'])
    new_house.members.add(this_user)
    # add self to house and create initial balance with self
    Balance.objects.create(first_user=this_user)
    Notification.objects.create(
        receiver=this_user, sender=this_user, house=new_house, action="CREATED")
    request.session['main_house_id'] = new_house.id
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return redirect(f'/profile/main_house/')


def select_main_house(request, house_id):
    if request.method == "GET":
        return redirect('/profile')
    request.session['main_house_id'] = house_id
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return redirect('/profile/main_house/')


def invite_response(request, notification_id, bool):
    if request.method == "GET":
        return redirect('/profile')
    # get variables needed for acceptance
    this_notification = Notification.objects.get(id=notification_id)
    my_invite = this_notification.invite
    this_house = my_invite.house
    this_user = User.objects.get(id=request.session['user_id'])
    if bool == 0:  # if declined
        Notification.objects.create(
            receiver=this_user, sender=this_user, house=this_house, action="DECLINED")
    elif bool == 1:  # if accepted
        Notification.objects.create(
            receiver=this_user, sender=this_user, house=this_house, action="ACCEPTED")
        # create a new balance for all users now in the house
        all_users = this_house.members.all()
        for user in all_users:
            new_bal = Balance.objects.create(first_user=user)
            new_bal.two_users.add(user)
            new_bal.two_users.add(this_user)
        my_invite.house.members.add(this_user)
        request.session['main_house_id'] = my_invite.house.id
    return redirect('/profile/main_house')


################### House Methods ###################


def add_housemate(request):
    if request.method == "GET":
        return redirect('/profile/house/')
    if User.objects.verifyAccountExists(request.POST['email']):
        messages.error(request, 'No users by that email exist')
        return redirect('/profile/main_house/')
    sender = User.objects.get(id=request.session['user_id'])
    receiverQuery = User.objects.filter(email=request.POST['email'])
    receiver = receiverQuery[0]
    house = House.objects.get(id=request.session['main_house_id'])
    if house.invites.filter(user=receiver).exists():
        messages.error(request, 'Invite already sent')
        return redirect('/profile/main_house/')
    invite = Invite.objects.create(
        house=house, user=receiver)
    Notification.objects.create(
        sender=sender, action="INVITED", receiver=receiver, house=house, invite=invite)
    return redirect('/profile/main_house/')


def main_house(request):
    if 'main_house_id' not in request.session:
        return redirect('/profile')
    this_house = House.objects.get(id=request.session['main_house_id'])
    context = {
        'house': this_house,
    }
    return render(request, 'house.html', context)


def add_item(request):
    if request.method == "GET":
        redirect('/profile/main_house')
    this_user = User.objects.get(id=request.session['user_id'])
    this_house = House.objects.get(id=request.session['main_house_id'])
    this_item = Item.objects.create(
        name=request.POST['name'], price=float(request.POST['price']), location=this_house)
    this_user.users_items.add(this_item)
    Notification.objects.create(
        sender=this_user, action="PURCHASED", item=this_item, house=this_house)
    return redirect('/profile/main_house')


def help_purchase(request, item_id, amount):
    if request.method == "GET":
        return redirect('/profile/main_house')
    # Get session user, relevant item, original buyer of item, and current house.
    this_user = User.objects.get(id=request.session['user_id'])
    this_item = Item.objects.get(id=item_id)
    original_buyer = this_item.owned_by.first()
    this_house = House.objects.get(id=request.session['main_house_id'])
    # Add session user to be an additonal owner of the item.
    this_user.users_items.add(this_item)
    # Get Balance instance shared between original owner and session user.
    shared_balance = this_user.between_balance.all().filter(
        two_users=original_buyer)[0]
    # Add amount due FROM session user TO original owner.
    # When the shared_balance.first_user is the same as session user,
    # the balance is subtracted, otherwise it is added.
    if shared_balance.first_user == this_user:
        shared_balance.balance_owed -= amount
    else:
        shared_balance.balance_owed += amount
    # Create notification of the event.
    Notification.objects.create(
        sender=this_user, action="HELPED", item=this_item, house=this_house, helped_purchase=amount)
    return redirect('/profile/main_house')


def delete_item(request, notification_id):
    if request.method == "GET":
        return redirect('profile/main_house')
    this_notification = Notification.objects.get(id=notification_id)
    this_item = this_notification.item
    if this_item.owned_by.all().count < 2:
        this_item.delete()
    else:
        messages.error(
            request, 'Cannot delete item because there is more than one owner,would you like to remove ownership of this item?')
        return redirect('/profile/main_house/')
    this_notification.delete()
    return redirect('/profile/main_house')
