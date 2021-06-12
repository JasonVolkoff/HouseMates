# from Projects.HouseMates.housemates_proj.login_and_profile.views import main_house
from django.db import models
import re
from django.db.models.deletion import CASCADE
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.


class UserManager(models.Manager):
    def validation(self, form):
        errors = {}
        if len(form['firstName']) < 2:
            errors['firstName'] = 'First Name must be at least 2 characters'
        if len(form['lastName']) < 2:
            errors['lastName'] = 'Last Name must be at least 2 characters'
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid email address'
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if form['password'] != form['confirmPassword']:
            errors['password'] = 'Passwords do not match'
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(),
                           bcrypt.gensalt()).decode()
        return self.create(
            first_name=form['firstName'],
            last_name=form['lastName'],
            email=form['email'],
            password=pw
        )

    def verifyAccountExists(self, email):
        users = self.filter(email=email)
        if not users:
            return True
        return False


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    notification_amount = models.IntegerField(default=0)
    total_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    # Eventually add default profile_image + upload option
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class House(models.Model):
    nickname = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name="houses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    # Can be owned by multiple people. Can reference ownership history via related notifications
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    owned_by = models.ManyToManyField(User, related_name="users_items")
    location = models.ForeignKey(
        House, related_name="items", on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Invite(models.Model):
    house = models.ForeignKey(
        House, related_name="invites", on_delete=CASCADE)
    user = models.ForeignKey(
        User, related_name="invites", on_delete=CASCADE)


class Notification(models.Model):
    ACTIONS = (
        ('PURCHASED', 'purchased'),
        ('INVITED', 'invited'),
        ('CREATED', 'created'),
        ('HELPED', 'helped purchase'),
        ('REGISTERED', 'registered an account'),
        ('ACCEPTED', 'accepted invite to'),
        ('DECLINED', 'declined invite to'))
    sender = models.ForeignKey(
        User, on_delete=CASCADE, blank=True, null=True, related_name='sent_notifications')
    receiver = models.ForeignKey(User, on_delete=CASCADE,
                                 blank=True, null=True, related_name='received_notifications')
    house = models.ForeignKey(
        House, on_delete=CASCADE, blank=True, null=True, related_name='notifications')
    item = models.ForeignKey(Item, blank=True, null=True,
                             related_name='item_notifications', on_delete=CASCADE)
    helped_purchase = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)
    action = models.CharField(
        choices=ACTIONS, default='CREATED', max_length=32)
    invite = models.ForeignKey(
        Invite, blank=True, null=True, related_name='notifications', on_delete=CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def profileFormat(self):
        action = f"{self.get_action_display()}"
        house = self.house
        sender = self.sender
        if self.action == "INVITED":
            notification = f'{sender.first_name} {sender.last_name} {action} you to {house.nickname}'
        elif self.action == "CREATED":
            notification = f'You {action} {house.nickname}'
        elif self.action == "REGISTERED":
            notification = f'You {action}'
        elif self.action == "ACCEPTED":
            notification = f'You {action} {house.nickname}'
        elif self.action == "DECLINED":
            notification = f'You {action} {house.nickname}'
        return notification

    def houseFormat(self):
        notification = f"{self.sender.first_name} {self.get_action_display()}"
        receiver = self.receiver
        house = self.house
        item = self.item
        if self.action == "PURCHASED":
            notification += f'{item.name}'
        elif self.action == "INVITED":
            notification += f'{receiver.first_name} {receiver.last_name} to {house.nickname}'
        elif self.action == "CREATED":
            notification += f'{house.nickname}'
        elif self.action == "HELPED":
            notification += f'{item.name}'
        elif self.action == "ACCEPTED":
            notification += f'{house.nickname}'
        elif self.action == "DECLINED":
            notification += f'{house.nickname}'
        return notification

    def houseOutputFormat(self):
        if self.action == "PURCHASED":
            output = f'{self.item.price}'
        elif self.action == "INVITED":
            if House.objects.filter(member=self.receiver).exists():
                output = "Accepted"
            elif Invite.objects.filter(user=self.receiver).exists():
                output = "Declined"
            else:
                output = "Pending"
        elif self.action == "CREATED" or self.action == "ACCEPTED":
            output = "Welcome!"
        elif self.action == "HELPED":
            output = f'${self.helped_purchase} of ${self.item.price}'
        elif self.action == "DECLINED":
            output = ""
        return output


class Balance(models.Model):
    balance_owed = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    two_users = models.ManyToManyField(User, related_name="between_balance")
    first_user = models.ForeignKey(
        User, related_name="first_balance", on_delete=CASCADE)
