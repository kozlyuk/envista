from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from rest_framework import views, permissions, status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from messaging.tasks import send_email

from accounts.serializers import UserDetailsSerializer
from accounts.models import User
from accounts.services import account_activation_token
from purchase.serializers import OrderSerializer
from purchase.models import Order


class UserDetailsView(RetrieveAPIView):
    """
    Returns UserModel fields.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class GetOrders(ListAPIView):
    """
    List all orders of customer.
    * Requires parameters: customer.
    * Only customer has permission to his orders.
    * Return error HTTP_400_BAD_REQUEST if customer does not exist
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        customer_pk = self.kwargs['customer']
        # get the customer
        try:
            customer = User.objects.get(pk=customer_pk)
        # return error HTTP_400_BAD_REQUEST if apartment does not exist
        except User.DoesNotExist:
            return Response(_('Customer with such id does not exist'),
                            status=status.HTTP_400_BAD_REQUEST)
        # get bills for apartment
        queryset = customer.order_set.exclude(status=Order.InCart)

        # Set up eager loading to avoid N+1 selects
        # queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class Register(views.APIView):
    """
    If post_data valid - updates user data,
    sends confirmation email with token and return HTTP_200_OK.
    If post_data not valid return status HTTP_400_BAD_REQUEST.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserDetailsSerializer(data=request.data)
        # check if serializer is valid
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = _('Activate your Envista account.')
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            send_email(mail_subject, message, to=[user.email]) # TODO add delay
            return Response(_('User registered'), status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activate(views.APIView):
    """
    Check actvation url and mark user email confirmed.
    If token is valid send HTTP_200_OK and make user active.
    If token is not valid send HTTP_400_BAD_REQUEST.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        # check if token is valid
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.email_confirmed = True
            user.save()
            return Response(_('Thank you for your email confirmation. '
                              'You will be able to log in to your account '
                              'after being activated by administrator.'),
                            status=status.HTTP_200_OK)
        else:
            return Response(_('Activation link is invalid!'),
                            status=status.HTTP_400_BAD_REQUEST)
