import datetime
from django.shortcuts import render

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Address, User, Badge, User_Badge, Comment, Post
from django.utils import timezone

# Create your views here.

# '/hello' route (define functions for serving different kinds of requests here)
class HelloWorldView(APIView):
  def get(self, request):
    message = "Hello, world!"
    return Response(data={'message': message})
  

def extractUserObject(request):
    # Get email from the request body (adjust key name if needed)
    try:
        user_id = request.data['user_id']
    except KeyError:
        return Response(
            {"error": "Missing 'user_id' field in request body."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User with user_id '{}' not found.".format(user_id)},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    return user
      
  
class UserAPI(APIView):
    def post(self, request):
        """
        API endpoint to fetch a user's details by user id.

        Args:
            request (Request): Incoming HTTP request.

        Returns:
            Response: JSON response containing user details or error message.
        """

        user = extractUserObject(request)
      
        serialized_data = {
            "id": user.user_id,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "phone": user.phone_number,
            "password": user.password,
            "about": user.about,
            "linkedIn": user.linkedin,
            "twitter": user.twitter,
            "facebook": user.facebook,
            "pfp_link": user.pfp_link,
            "verified_email": user.verified_email,
            "verified_phone": user.verified_phone,
            "verified_address": user.verified_address,

            # we can add more fields to return as required later
        }

        return Response(serialized_data, status=status.HTTP_200_OK)
    

class LoginUserAPI(APIView):
    def post(self, request):
        """
        API endpoint to authenticate a user based on email and password.

        Args:
            request (Request): Incoming HTTP request containing user credentials in JSON format.

        Returns:
            Response: JSON response with success message or error details.
        """

        try:
            # Validate request data as a dictionary
            user_data = request.data

        except (TypeError, ValueError):
            return Response({'error': 'Request body must be valid JSON.'})

        # Check for required fields
        required_fields = ['email', 'password']
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            return Response({'error': f"Missing required fields: {', '.join(missing_fields)}"})

        # Hardcoded user email for demonstration (replace with appropriate logic)
        user_email = user_data['email']

        try:
            user = User.objects.get(email=user_email)  # Use primary key (pk) for retrieval
        except User.DoesNotExist:
            return Response(
                {'error': f"User with email {user_email} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the provided password matches the user's password
        if user_data['password'] != user.password:
            return Response({'error': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        primary_add = user.primaryAddress()
        return Response({
            'message': 'User authenticated successfully.', 
            'user_id': user.user_id,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'city': primary_add.city if primary_add else "",
            'province': primary_add.province if primary_add else "",
        }, status=status.HTTP_200_OK)
    
class RegisterUserAPI(APIView):
    def post(self, request):
        """
        API endpoint to register a new user.

        Args:
            request (Request): Incoming HTTP request containing user details in JSON format.

        Returns:
            Response: JSON response with success message or error details.
        """

        try:
            # Validate request data as a dictionary
            user_data = request.data

        except (TypeError, ValueError):
            return Response({'error': 'Request body must be valid JSON.'})

        # Check for required fields
        required_fields = ['firstName', 'lastName', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            return Response({'error': f"Missing required fields: {', '.join(missing_fields)}"})

        # Create a new user instance with the provided data
        new_user = User(
            first_name=user_data['firstName'],
            last_name=user_data['lastName'],
            email=user_data['email'],
            password=user_data['password'],
        )

        new_user.save()  # Save the new user to the database

        # new_user.awardBadge("New Neighbour Badge") # give the user a welcome badge

        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
    
class UpdateUserAPI(APIView):
    def post(self, request):
        """
        API endpoint to update a user's details.

        Args:
            request (Request): Incoming HTTP request containing user details in JSON format.

        Returns:
            Response: JSON response with success message or error details.
        """

        try:
            # Validate request data as a dictionary
            user_data = request.data
            print(user_data)

        except (TypeError, ValueError):
            return Response({'error': 'Request body must be valid JSON.'})

        # Check for required fields
        required_fields = ['user_id', 'firstName', 'lastName', 'email', 'phone', 'about', 'linkedIn', 'twitter', 'facebook']
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            return Response({'error': f"Missing required fields: {', '.join(missing_fields)}"})

        # # Hardcoded user ID for demonstration (replace with appropriate logic)
        # user_id = 1

        try:
            user = User.objects.get(pk=user_data['user_id'])  # Use primary key (pk) for retrieval
        except User.DoesNotExist:
            return Response(
                {'error': f"User with ID {user_data['user_id']} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update user fields with data from request
        user.first_name = user_data['firstName']
        user.last_name = user_data['lastName']
        user.email = user_data['email']  # Update email if allowed (security considerations)
        user.phone_number = user_data['phone']
        user.about = user_data['about']
        user.linkedin = user_data['linkedIn']
        user.twitter = user_data['twitter']
        user.facebook = user_data['facebook']
        # Update other relevant fields as needed

        user.save()  # Save changes to the database

        return Response({'message': 'User details updated successfully.'}, status=status.HTTP_200_OK)
    
class UserPrimaryAddressAPI(APIView):
    def post(self, request):
        """
        API endpoint to fetch a user's primary address by user id.

        Args:
            request (Request): Incoming HTTP request.

        Returns:
            Response: JSON response containing user details or error message.
        """
        user = extractUserObject(request)
        primary_add = user.primaryAddress()

        # required fields
        serialized_data = {
            "firstName": user.first_name,
            "lastName": user.last_name,
        }

        # Conditionally add address fields if primary_add is not None
        if primary_add:
            serialized_data.update({
                "street_address": primary_add.street_address,
                "city": primary_add.city,
                "province": primary_add.province,
                "zip_code": primary_add.zip_code,
                "address_type": primary_add.address_type,
            })

        return Response(serialized_data, status=status.HTTP_200_OK)
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'  # Include all fields (or specify specific fields)
    
class UserAddressAPI(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)  # Use pk to get the user information
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get all user addresses
        all_user_addresses = user.addresses.all()

        # Find the primary address
        primary_address = all_user_addresses.filter(primaryAddress=True).first()

        # Serialize addresses
        serializer = AddressSerializer(all_user_addresses, many=True)

        # Create response data
        response_data = {
            "primary": primary_address.address_id if primary_address else None,
            "places": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    
class UserAchievementAPI(APIView):
    def post(self, request):
        """
        API endpoint to fetch a user's details by user_id.

        Args:
            request (Request): Incoming HTTP request.

        Returns:
            Response: JSON response containing user details or error message.
        """

        # Get id from the request body (adjust key name if needed)
        try:
            user_id = request.data['user_id']
        except KeyError:
            return Response(
                {"error": "Missing 'user_id' field in request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User with user_id '{}' not found.".format(user_id)},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        achievement_rec = user.achievement

        if (achievement_rec == None):
            serialized_data = {
            "quest_points": 0,
            "num_badges": 0,
            "days_active" : 0,
	        "num_achievements" : 0
            # we can add more fields to return as required later
            }
        else: 
            serialized_data = {
                "quest_points": achievement_rec.quest_points,
                "num_badges": achievement_rec.num_badges,
                "days_active" : achievement_rec.days_active,
                "num_achievements" : achievement_rec.num_achievements
                # we can add more fields to return as required later
            }

        return Response(serialized_data, status=status.HTTP_200_OK)


class UpdateEmailVerificationStatus(APIView):
    """
    UpdateEmailVerificationStatus class

    This class is used to update the email verification status of a user.
    """
    def post(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        verified_email = request.data.get('verified_email')
        if verified_email is not None:
            user.verified_email = verified_email
            user.save()
            if user.isFullyVerified():
                user.awardVerificationBadge()
            return Response({'message': 'Email verification status updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Verified email status not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        


class UpdatePhoneVerificationStatus(APIView):
    """
    UpdatePhoneVerificationStatus class

    This class is used to update the phone verification status of a user.
    """
    def post(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        verified_phone = request.data.get('verified_phone')
        if verified_phone is not None:
            user.verified_phone = verified_phone
            user.save()
            if user.isFullyVerified():
                user.awardVerificationBadge()
            return Response({'message': 'Phone verification status updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Verified phone status not provided'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateAddressVerificationStatus(APIView):
    """
    UpdateAddressVerificationStatus class

    This class is used to update the address verification status of a user.
    """
    def post(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        verified_address = request.data.get('verified_address')
        if verified_address is not None:
            user.verified_address = verified_address
            user.save()
            if user.isFullyVerified():
                user.awardVerificationBadge()
            return Response({'message': 'Address verification status updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Verified address status not provided'}, status=status.HTTP_400_BAD_REQUEST)
        

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'  # Include all fields (or specify specific fields)
        
class AllBadgesAPI(APIView):
    def get(self, request):
        badges = Badge.objects.all()
        serializer = BadgeSerializer(badges, many=True)  # Pass 'many=True' for multiple instances
        return Response(serializer.data)
    
class UserBadgesAPI(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id) # use pk to get the user information
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        all_user_badges = user.getAllBadges()

        serializer = BadgeSerializer(all_user_badges, many=True)

        return Response(serializer.data)


        

class PopulateBadges(APIView):
    """
    PopulateBadges class

    This class is used to populate the database with predefined badges and associate them with users based on certain conditions.
    """
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


class VerifyTrustedNeighbourBadge(APIView):
    """
    Verifies if a user meets the requirements for the Trusted Neighbour Badge and grants the badge if applicable.

    Requirements:
    - User must have verified email, phone, and address.
    """
    def post(self, request, user_id):
        try:
            # Retrieve the user object based on the user_id
            user = User.objects.get(id=user_id)

            # Check if the user's identity and address have been verified
            if user.verified_email and user.verified_phone and user.verified_address:
                # Create or update User_Badge entry for Trusted Neighbour Badge
                trusted_neighbour_badge = Badge.objects.get(name="Trusted Neighbour Badge") # Assuming the badge already exists
                user_badge, created = User_Badge.objects.get_or_create(user=user, badge=trusted_neighbour_badge)

                # Set the granted date of the badge
                user_badge.granted_date = datetime.now()
                user_badge.save()

                return Response({"message": "User meets the requirements for Trusted Neighbour Badge", "badge_granted": created}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User does not meet the requirements for Trusted Neighbour Badge"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyNewNeighborBadge(APIView):
    """
    Verifies if a user meets the requirements for the New Neighbour Badge and grants the badge if applicable.

    Requirements:
    - User must complete their first post or comment on the platform.
    """
    def post(self, request, user_id):
        try:
            # Retrieve the user object based on the user_id
            user = User.objects.get(id=user_id)

            # Check if the user has completed their first post or comment
            if user.post_count > 0 or user.comment_count > 0:
                # Create or update User_Badge entry for New Neighbour Badge
                new_neighbour_badge = Badge.objects.get(name="New Neighbour Badge")  # Assuming the badge already exists
                user_badge, created = User_Badge.objects.get_or_create(user=user, badge=new_neighbour_badge)

                # Set the granted date of the badge only if it's a new entry
                if created:
                    user_badge.granted_date = datetime.now()
                    user_badge.save()

                return Response({"message": "User meets the requirements for New Neighbour Badge", "badge_granted": created}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User does not meet the requirements for New Neighbour Badge"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VerifyInquirerBadge(APIView):
    """
    Verifies if a user meets the requirements for the Inquirer Badge and grants the badge if applicable.

    Requirements:
    - A comment created by the user has received a certain number of upvotes and is considered insightful (over 80% approval)
    """
    def post(self, request, user_id):
        try:
            # Retrieve the user object based on the user_id
            user = User.objects.get(id=user_id)

            # Retrieve the user's comments from the Comment table
            comments = Comment.objects.filter(user=user)

            # Check if the user's comment complies with the requirements
            if any((comment.upvotes >= 5 and comment.upvotes / comment.downvotes >= 4) for comment in comments):
                # Create or update User_Badge entry for Inquirer Badge
                inquirer_badge = Badge.objects.get(name="Inquirer Badge")  # Assuming the badge already exists
                user_badge, created = User_Badge.objects.get_or_create(user=user, badge=inquirer_badge)

                # Set the granted date of the badge only if it's a new entry
                if created:
                    user_badge.granted_date = datetime.now()
                    user_badge.save()

                return Response({"message": "User meets the requirements for Inquirer Badge", "badge_granted": created}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User does not meet the requirements for Inquirer Badge"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyWelcomingWhispererBadge(APIView):
    """
    Verifies if a user meets the requirements for the Welcoming Whisperer Badge and grants the badge if applicable.

    Requirements:
    - User has invited a new user to participate, and they have completed their first activity.
    """
    def post(self, request, user_id):
        try:
            # Retrieve the user object based on the user_id
            user = User.objects.get(id=user_id)

            # Check all users invitedById field and check if they were invited by the current user
            invited_users = User.objects.filter(invited_by=user.id)

            # Check if any user has completed their first activity
            new_users = [invited_user for invited_user in invited_users if invited_user.post_count > 0 or invited_user.comment_count > 0 or invited_user.polls_answered_count > 0]

            if new_users:
                # Create or update User_Badge entry for Welcoming Whisperer Badge
                welcoming_whisperer_badge = Badge.objects.get(name="Welcoming Whisperer Badge")
                user_badge, created = User_Badge.objects.get_or_create(user=user, badge=welcoming_whisperer_badge)

                # Set the granted date of the badge only if it's a new entry
                if created:
                    user_badge.granted_date = datetime.now()
                    user_badge.save()

                return Response({"message": "User meets the requirements for Welcoming Whisperer Badge", "badge_granted": created}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User does not meet the requirements for Welcoming Whisperer Badge"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyLegacyCitizenBadge(APIView):
    """
    Verifies if a user meets the requirements for the Legacy Citizen Badge and grants the badge if applicable.

    Requirements:
    - User has been active on the platform for a certain number of years.
    """
    def post(self, request, user_id):
        try:
            # Retrieve the user object based on the user_id
            user = User.objects.get(id=user_id)

            # Check if account was created over 1 year ago and user has a few posts/comments
            if user.account_created < timezone.now() - datetime.timedelta(days=365) and (user.post_count > 10 or user.comment_count > 10):
                # Create or update User_Badge entry for Legacy Citizen Badge
                legacy_citizen_badge = Badge.objects.get(name="Legacy Citizen Badge")  # Assuming the badge already exists
                user_badge, created = User_Badge.objects.get_or_create(user=user, badge=legacy_citizen_badge)

                # Set the granted date of the badge only if it's a new entry
                if created:
                    user_badge.granted_date = datetime.now()
                    user_badge.save()

                return Response({"message": "User meets the requirements for Legacy Citizen Badge", "badge_granted": created}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User does not meet the requirements for Legacy Citizen Badge"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class VerifyNewVoiceBadge(APIView):
    """
    Verifies if a user meets the requirements for the New Voice Badge and grants the badge if applicable.
    
    Requirements:
    - User must have participated in at least one poll.
    """
    def post(self, request, user_id):
        try:
            # Retrieve the user object based on the user_id
            user = User.objects.get(id=user_id)

            # Check if the user has participated in at least one poll
            if user.polls_answered_count > 0:
                # Create or update User_Badge entry for New Voice Badge
                new_voice_badge = Badge.objects.get(name="New Voice Badge")  # Assuming the badge already exists
                user_badge, created = User_Badge.objects.get_or_create(user=user, badge=new_voice_badge)

                # Set the granted date of the badge only if it's a new entry
                if created:
                    user_badge.granted_date = datetime.now()
                    user_badge.save()

                return Response({"message": "User meets the requirements for New Voice Badge", "badge_granted": created}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User does not meet the requirements for New Voice Badge"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddPost(APIView):
    def post(self, request):
        """
        API endpoint to add a new post for a user.

        Args:
            request (Request): Incoming HTTP request containing user_id, title, and content in JSON format.

        Returns:
            Response: JSON response with success message or error details.
        """

        try:
            # Validate request data as a dictionary
            post_data = request.data

        except (TypeError, ValueError):
            return Response({'error': 'Request body must be valid JSON.'})

        # Check for required fields
        required_fields = ['user_id', 'title', 'content']
        missing_fields = [field for field in required_fields if field not in post_data]
        if missing_fields:
            return Response({'error': f"Missing required fields: {', '.join(missing_fields)}"})

        # Create a new post instance with the provided data
        new_post = Post(
            user_id=post_data['user_id'],
            title=post_data['title'],
            content=post_data['content'],
        )

        new_post.save()  # Save the new post to the database

        
        # Fetch user and increment their post count
        user = User.objects.get(pk=post_data['user_id'])
        user.post_count += 1
        user.save()

        return Response({'message': 'Post added successfully.'}, status=status.HTTP_201_CREATED)
    

class GetAllPosts(APIView):
    def get(self, request):
        """
        API endpoint to fetch all posts.

        Args:
            request (Request): Incoming HTTP request.

        Returns:
            Response: JSON response containing all posts or error message.
        """

        posts = Post.objects.all()
        serialized_data = [
            {
                "post_id": post.post_id,
                "title": post.title,
                "content": post.content,
                "upvotes": post.upvotes,
                "downvotes": post.downvotes,
                "created_date": post.created_date,
                "user_id": post.user_id,
            }
            for post in posts
        ]

        return Response(serialized_data, status=status.HTTP_200_OK)
    

class GetPostsByUser(APIView):
    def get(self, request, user_id):
        """
        API endpoint to fetch all posts by a specific user.

        Args:
            request (Request): Incoming HTTP request.
            user_id (int): The ID of the user.

        Returns:
            Response: JSON response containing all posts by the user or error message.
        """

        posts = Post.objects.filter(user_id=user_id)
        serialized_data = [
            {
                "post_id": post.post_id,
                "title": post.title,
                "content": post.content,
                "upvotes": post.upvotes,
                "downvotes": post.downvotes,
                "created_date": post.created_date,
                "user_id": post.user_id,
            }
            for post in posts
        ]

        return Response(serialized_data, status=status.HTTP_200_OK)
    

class GetCommentsByUser(APIView):
    def get(self, request, user_id):
        """
        API endpoint to fetch all comments by a specific user.

        Args:
            request (Request): Incoming HTTP request.
            user_id (int): The ID of the user.

        Returns:
            Response: JSON response containing all comments by the user or error message.
        """

        comments = Comment.objects.filter(user_id=user_id)
        serialized_data = [
            {
                "comment_id": comment.comment_id,
                "content": comment.content,
                "upvotes": comment.upvotes,
                "downvotes": comment.downvotes,
                "created_date": comment.created_date,
                "user_id": comment.user_id,
            }
            for comment in comments
        ]

        return Response(serialized_data, status=status.HTTP_200_OK)
    

class AddComment(APIView):
    def post(self, request):
        """
        API endpoint to add a new comment to a post.

        Args:
            request (Request): Incoming HTTP request with user_id, post_id, and content in JSON format.

        Returns:
            Response: JSON response with success message or error details.
        """
            
        try:
            # Validate request data as a dictionary
            comment_data = request.data

        except (TypeError, ValueError):
            return Response({'error': 'Request body must be valid JSON.'})

        # Check for required fields
        required_fields = ['user_id', 'post_id', 'content']
        missing_fields = [field for field in required_fields if field not in comment_data]
        if missing_fields:
            return Response({'error': f"Missing required fields: {', '.join(missing_fields)}"})

        # Create a new comment instance with the provided data
        new_comment = Comment(
            user_id=comment_data['user_id'],
            post_id=comment_data['post_id'],
            content=comment_data['content'],
        )

        new_comment.save()

        # Fetch user and increment their comment count
        user = User.objects.get(pk=comment_data['user_id'])
        user.comment_count += 1
        user.save()

        return Response({'message': 'Comment added successfully.'}, status=status.HTTP_201_CREATED)
    

class GetCommentsByPost(APIView):
    def get(self, request, post_id):
        """
        API endpoint to fetch all comments for a specific post.

        Args:
            request (Request): Incoming HTTP request.
            post_id (int): The ID of the post.

        Returns:
            Response: JSON response containing all comments for the post or error message.
        """

        comments = Comment.objects.filter(post_id=post_id)
        serialized_data = [
            {
                "comment_id": comment.comment_id,
                "content": comment.content,
                "upvotes": comment.upvotes,
                "downvotes": comment.downvotes,
                "created_date": comment.created_date,
                "user_id": comment.user_id,
            }
            for comment in comments
        ]

        return Response(serialized_data, status=status.HTTP_200_OK)
