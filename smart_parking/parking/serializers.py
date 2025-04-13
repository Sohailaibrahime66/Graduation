import smart_parking.settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *
from rest_framework import serializers
from django.core.mail import send_mail
import random
import string
from django.db import IntegrityError
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FamilyCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyCommunity
        fields = '__all__'

class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '__all__'

class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = '__all__'

# class FavoriteGarageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FavoriteGarage
#         fields = '__all__'

class ParkingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingZone
        fields = '__all__'

class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ParkingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingEvent
        fields = '__all__'

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'

class ParkingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingHistory
        fields = '__all__'

class ParkingAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingAlert
        fields = '__all__'

class ParkingSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSubscription
        fields = '__all__'

class ParkingSlotReservationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlotReservationHistory
        fields = '__all__'

class ParkingSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSensor
        fields = '__all__'

class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = '__all__'

class DiscountCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCoupon
        fields = '__all__'

class ParkingNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingNotification
        fields = '__all__'

# class InvoiceSerializer(serializers.Serializer):
#     reservation_id = serializers.IntegerField()
#     vehicle_plate = serializers.CharField()
#     parking_slot = serializers.CharField()
#     parking_zone = serializers.CharField()
#     start_time = serializers.DateTimeField()
#     end_time = serializers.DateTimeField()
#     total_duration = serializers.FloatField()
#     amount = serializers.DecimalField(max_digits=6, decimal_places=2)
#     payment_status = serializers.CharField()

#     @staticmethod
#     def generate_invoice(reservation):
#         """Generate an invoice dictionary from a Reservation object."""
#         try:
#             payment = Payment.objects.get(reservation=reservation)

#             return {
#                 "reservation_id": reservation.id,
#                 "vehicle_plate": reservation.vehicle.plate_number,
#                 "parking_slot": reservation.parking_slot.slot_number,
#                 "parking_zone": reservation.parking_slot.parking_zone.name,
#                 "start_time": reservation.start_time,
#                 "end_time": reservation.end_time,
#                 "total_duration": round((reservation.end_time - reservation.start_time).total_seconds() / 3600, 2),
#                 "amount": payment.amount,
#                 "payment_status": payment.payment_status
#             }
#         except Payment.DoesNotExist:
#             return {"error": "Payment not found for this reservation."}

from django.db import IntegrityError
from rest_framework import serializers
from .models import User, Vehicle  # Adjust import as needed

class UserRegistrationSerializer(serializers.ModelSerializer):
    license_plate = serializers.CharField(write_only=True)
    car_model = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'national_id',
            'password', 'profile_picture', 'gender', 'license_id',
            'license_plate', 'car_model'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        license_plate = validated_data.pop('license_plate')
        car_model = validated_data.pop('car_model')

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        try:
            Vehicle.objects.create(
                user=user,
                license_plate=license_plate,
                car_model=car_model
            )
        except IntegrityError as e:
            print(f"Vehicle creation error: {e}")
            # Optional: you could delete the user or raise a validation error
            user.delete()
            raise serializers.ValidationError("Vehicle already exists or data is invalid.")

        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user is None:
            raise serializers.ValidationError("No user found with this email.")
        
        # Generate reset token
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
        user.reset_password_token = token
        user.save()

        # Send reset password email
        try:
            send_mail(
                'Password Reset Request',
                f'Your password reset token: {token}',
                smart_parking.settings.DEFAULT_FROM_EMAIL,  # Ensure this is correct
                [user.email],
            )
            print(f"Email sent to {user.email}")
        except Exception as e:
            print(f"Error sending email: {e}")

        return data
    
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


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'user', 'card_number', 'expiry_date', 'cvv']
        read_only_fields = ['user']


class FavoriteGarageSerializer(serializers.ModelSerializer):
    garage_name = serializers.ReadOnlyField(source='garage.name')
    user = serializers.StringRelatedField(read_only=True)  # Shows the username

    class Meta:
        model = FavoriteGarage
        fields = ['id', 'user', 'garage', 'garage_name']



class FamilyInvitationSerializer(serializers.ModelSerializer):
    inviter_email = serializers.ReadOnlyField(source='inviter.email')
    invitee_email = serializers.ReadOnlyField(source='invitee.email')
    family_name = serializers.ReadOnlyField(source='family.name')

    class Meta:
        model = FamilyInvitation
        fields = [
            'id', 'inviter', 'inviter_email', 'invitee',
            'invitee_email', 'family', 'family_name',
            'accepted', 'created_at'
        ]
        read_only_fields = ['inviter', 'created_at', 'inviter_email', 'invitee_email', 'family_name']