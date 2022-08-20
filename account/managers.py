from django.contrib.auth.models import BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, phone_number, username, fullname, password, **other_fields):

        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_admin') is not True:
            raise ValueError(_(
                'Superuser must be assigned to is_admin=True.'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_(
                'Superuser must be assigned to is_superuser=True.'))

        return self.create_user(email, phone_number, username, fullname, password, **other_fields)

    def create_user(self, email, phone_number, username, fullname, password, **other_fields):

        if not phone_number:
            raise ValueError(_('You must provide an phone_number'))

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          phone_number=phone_number, fullname=fullname, **other_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user
