from rest_framework_simplejwt.tokens import Token, AccessToken


class CustomAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        # 🔥 Add custom claims here
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name

        return token
