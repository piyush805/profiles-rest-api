from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.models import BaseUserManager

# Create your models here.
class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model  """

    def create_user(self,email,name,password=None):
        """Creates a new user profile object"""
        if not email: #if user name is noe or false
            raise ValueError('User must have an email address.')

        #normalizes(converts to lowercase to standardize)
        email =self.normalize_email(email)
        user = self.model(email=email, name=name)
        #will encrypt the password as hash
        user.set_password(password)
        #save the user in database
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        """Create and saves a superuser with given details."""
        #take info from create_user
        user = self.create_user(email,name,password)
        #set following values to true
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represnts a "user profile" inside our system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    #to check if user is active or not(can use it to disable accounts)
    #requirement when you add a custome user model to django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #will create later
    objects = UserProfileManager()
    #customer's 'username field' used when logging in, setting it to email
    USERNAME_FIELD = 'email'
    #required firld in the system, can be as many as you want
    REQUIRED_FIELDS = ['name']
    #requiredd func to use profile with django-admin
    def get_full_name(self):
        """Used to get a users full name"""
        return self.name
    #may have print first_last name with full name and ponly first name with short name

    def get_short_name(self):
        """Used to get a user's shoer name"""
        return self.name

    def __str__(self):
        """django uses this when it needs to convert the object to a string"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update."""
    #what to do if user profile link ever gets deleted?
    user_profile = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    #if user deletes that profile and delete all the status updates that go along with it
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
