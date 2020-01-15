from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from accounts.serializers import UserDetailsSerializer

class UserDetailsView(RetrieveAPIView):
    """
    Returns UserModel fields.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
