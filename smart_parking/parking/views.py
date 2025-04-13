from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import GarageSerializer, UserSerializer
from .models import *
from .serializers import *
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FamilyCommunityViewSet(viewsets.ModelViewSet):
    queryset = FamilyCommunity.objects.all()
    serializer_class = FamilyCommunitySerializer

class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer

class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer

    # 🔍 Search for parking around my area
    @action(detail=False, methods=['get'], url_path='search-nearby')
    def search_nearby(self, request):
        try:
            lat = float(request.query_params.get('lat'))
            lng = float(request.query_params.get('lng'))
        except (TypeError, ValueError):
            return Response({'error': 'Invalid coordinates'}, status=400)

        nearby = Garage.objects.filter(
            latitude__range=(lat - 0.05, lat + 0.05),
            longitude__range=(lng - 0.05, lng + 0.05)
        )
        serializer = self.get_serializer(nearby, many=True)
        return Response(serializer.data)



class ParkingZoneViewSet(viewsets.ModelViewSet):
    queryset = ParkingZone.objects.all()
    serializer_class = ParkingZoneSerializer


class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ParkingEventViewSet(viewsets.ModelViewSet):
    queryset = ParkingEvent.objects.all()
    serializer_class = ParkingEventSerializer


class PricingViewSet(viewsets.ModelViewSet):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer


class ParkingHistoryViewSet(viewsets.ModelViewSet):
    queryset = ParkingHistory.objects.all()
    serializer_class = ParkingHistorySerializer


class ParkingAlertViewSet(viewsets.ModelViewSet):
    queryset = ParkingAlert.objects.all()
    serializer_class = ParkingAlertSerializer


class ParkingSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = ParkingSubscription.objects.all()
    serializer_class = ParkingSubscriptionSerializer


class ParkingSlotReservationHistoryViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlotReservationHistory.objects.all()
    serializer_class = ParkingSlotReservationHistorySerializer


class ParkingSensorViewSet(viewsets.ModelViewSet):
    queryset = ParkingSensor.objects.all()
    serializer_class = ParkingSensorSerializer


class UserFeedbackViewSet(viewsets.ModelViewSet):
    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer


class DiscountCouponViewSet(viewsets.ModelViewSet):
    queryset = DiscountCoupon.objects.all()
    serializer_class = DiscountCouponSerializer


class ParkingNotificationViewSet(viewsets.ModelViewSet):
    queryset = ParkingNotification.objects.all()
    serializer_class = ParkingNotificationSerializer



class ResetPasswordSerializer(serializers.Serializer):
    reset_password_token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(reset_password_token=data['reset_password_token']).first()
        if user is None:
            raise serializers.ValidationError("Invalid token.")
        
        return data

    def save(self):
        user = User.objects.filter(reset_password_token=self.validated_data['reset_password_token']).first()
        user.set_password(self.validated_data['new_password'])
        user.reset_password_token = ''  # Clear the token
        user.save()
        return user

# 5. Registration View

class UserRegistrationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 6. Login View
class LoginViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 7. Forgot Password View
class ForgotPasswordViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password reset email sent!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 8. Reset Password View
class ResetPasswordViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Add Card
class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteGarageViewSet(viewsets.ModelViewSet):
    queryset = FavoriteGarage.objects.all()
    serializer_class = FavoriteGarageSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# Favorite Garage

class FamilyInvitationViewSet(viewsets.ModelViewSet):
    queryset = FamilyInvitation.objects.all()
    serializer_class = FamilyInvitationSerializer


    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        family_id = request.data.get("family_id")
        try:
            invitee = User.objects.get(email=email)
            family = FamilyCommunity.objects.get(id=family_id)
            invitation = FamilyInvitation.objects.create(
                inviter=request.user,
                invitee=invitee,
                family=family
            )
            return Response({"message": "Invitation sent."})
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=404)
        except FamilyCommunity.DoesNotExist:
            return Response({"message": "Family not found"}, status=404)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        accepted = request.data.get("accepted")
        instance.accepted = accepted
        instance.save()

        if accepted:
            FamilyMember.objects.create(family=instance.family, user=instance.invitee)
            return Response({"message": "Invitation accepted and user added to family."})
        else:
            return Response({"message": "Invitation declined. Notification sent."})
# Family Invitation
