from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User

# Create your views here.

# '/hello' route (define functions for serving different kinds of requests here)
class HelloWorldView(APIView):
  def get(self, request):
    message = "Hello, world!"
    return Response(data={'message': message})


class UpdateEmailVerificationStatus(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        verified_email = request.data.get('verified_email')
        if verified_email is not None:
            user.verified_email = verified_email
            user.save()
            return Response({'message': 'Email verification status updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Verified email status not provided'}, status=status.HTTP_400_BAD_REQUEST)

"""
UpdatePhoneVerificationStatus class

This class is used to update the phone verification status of a user.
"""
class UpdatePhoneVerificationStatus(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        verified_phone = request.data.get('verified_phone')
        if verified_phone is not None:
            user.verified_phone = verified_phone
            user.save()
            return Response({'message': 'Phone verification status updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Verified phone status not provided'}, status=status.HTTP_400_BAD_REQUEST)


"""
UpdateAddressVerificationStatus class

This class is used to update the address verification status of a user.
"""
class UpdateAddressVerificationStatus(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        verified_address = request.data.get('verified_address')
        if verified_address is not None:
            user.verified_address = verified_address
            user.save()
            return Response({'message': 'Address verification status updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Verified address status not provided'}, status=status.HTTP_400_BAD_REQUEST)
        

class PopulateBadges(APIView):
    def post(self, request):
        try:
            # Inquirer Badge
            inquirer_badge = Badge.objects.create(
                name="Inquirer Badge",
                img_link="inquirer_badge_img_link",
                rarity="Common",
                description="Awarded after their first insightful comment or question. This badge acknowledges the initiation into the realm of discussions.",
                points=100,  # Set appropriate points
                category="Discussion"
            )
            # New Voice Badge
            new_voice_badge = Badge.objects.create(
                name="New Voice Badge",
                img_link="new_voice_badge_img_link",
                rarity="Common",
                description="Celebrating your inaugural participation! This badge acknowledges your initial step in voicing your opinion and contributing to the community's collective decision-making. As a 'New Voice,' you've begun your journey in shaping our neighborhood's future.",
                points=100,  # Set appropriate points
                category="Participation"
            )
            # Welcoming Whisperer Badge
            welcoming_whisperer_badge = Badge.objects.create(
                name="Welcoming Whisperer Badge",
                img_link="welcoming_whisperer_badge_img_link",
                rarity="Rare",
                description="For inviting their first neighbor to PlaceSpeak to participate in a poll or discussion.",
                points=200,  # Set appropriate points
                category="Engagement"
            )
            # Trusted Neighbour Badge
            trusted_neighbour_badge = Badge.objects.create(
                name="Trusted Neighbour Badge",
                img_link="trusted_neighbour_badge_img_link",
                rarity="Epic",
                description="This badge signifies that a user's identity and address have been verified, enhancing the trustworthiness and authenticity of their contributions. As a Trusted Neighbor, their commitment to genuine engagement strengthens the integrity and reliability of our civic community platform.",
                points=500,  # Set appropriate points
                category="Verification"
            )
            # Legacy Citizen Badge
            legacy_citizen_badge = Badge.objects.create(
                name="Legacy Citizen Badge",
                img_link="legacy_citizen_badge_img_link",
                rarity="Legendary",
                description="Long-time users consistently participating over the years. Their stories and contributions become legendary within the community.",
                points=1000,  # Set appropriate points
                category="Participation"
            )
            # New Neighbour Badge
            new_neighbour_badge = Badge.objects.create(
                name="New Neighbour Badge",
                img_link="new_neighbour_badge_img_link",
                rarity="Common",
                description="Awarded to those who have recently joined Placespeak. This badge recognizes newcomers and encourages them to dive into discussions, share their thoughts, and become active participants in shaping our neighbourhood's future.",
                points=100,  # Set appropriate points
                category="Participation"
            )

            # TODO: Associate the badge with the user by creating User_Badge instances

            # Example: Get users who meet the condition for Inquirer Badge
            # inquirer_badge_users = User.objects.filter(
            #     # Add your condition logic here
            # )

            # Example: Associate Inquirer Badge with users
            # for user in inquirer_badge_users:
            #     User_Badge.objects.create(
            #         user=user,
            #         badge=inquirer_badge
            #     )

            # Repeat the above process for each badge

            return Response({"message": "Badges populated successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

