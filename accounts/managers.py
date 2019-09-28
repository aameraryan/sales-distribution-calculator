from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is must to create a User")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('account_type', "AU")

        if extra_fields.get('is_superuser') is not True or extra_fields.get('account_type') != "AU":
            raise ValueError("Superuser must have is_superuser=True and account_type=AU")

        return self._create_user(email, password, **extra_fields)
