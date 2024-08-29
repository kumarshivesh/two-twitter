from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet, LikeTweet, Favorite, Follow
from .forms import UserRegistrationForm, TweetForm, ProfileEditForm
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
  return  render(request, 'index.html')

def tweet_list(reqest):
  tweets = Tweet.objects.all().order_by('-created_at')
  return render(reqest, 'tweet_list.html', {'tweets': tweets})



def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

            profileimg = form.cleaned_data.get('profileimg') or 'profile_images/blank-profile-picture.png'

            # Create a Profile object for the new user
            Profile.objects.create(user=user, profileimg=profileimg)

            # Log the user in and redirect to 'feed' page 
            user_login = auth.authenticate(username=user.username, password=form.cleaned_data.get('password1'))
            auth.login(request, user_login)

            return redirect('feed')  # Redirect to the feed page
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})


def custom_logout(request):
  logout(request)
  return redirect('tweet_list') # Redirect to 'tweet_list' (temporarily to 'index' page)

@login_required
def tweet_create(request):
  if request.method == "POST":
   form = TweetForm(request.POST, request.FILES)
   if form.is_valid():
     tweet = form.save(commit=False)
     tweet.user = request.user
     tweet.save()
     return redirect('tweet_list')
  else:
    form = TweetForm()
  return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
  tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
  if request.method == "POST":
   form = TweetForm(request.POST, request.FILES, instance=tweet)
   if form.is_valid():
     tweet = form.save(commit=False)
     tweet.user = request.user
     tweet.save()
     return redirect('tweet_list')
  else:
    form = TweetForm(instance=tweet)
  return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
  tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
  if request.method == "POST":
    tweet.delete()
    return redirect('tweet_list')
  return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

@login_required
def user_posts_list(request):
    user_tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tweet/user_posts_list.html', {'user_tweets': user_tweets})

def search(request):
  query = request.GET.get('q')
  if query:
    results = Tweet.objects.filter(text__icontains=query)
  else:
    results = Tweet.objects.none()
  return render(request, 'search_results.html', {'results': results, 'query': query})


@login_required
def edit_profile(request):
  try:
    profile = request.user.profile
  except Profile.DoesNotExist:
    profile = Profile.objects.create(user=request.user)

  if request.method == 'POST':
    form = ProfileEditForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
      profile = form.save(commit=False)
      profile.user.first_name = form.cleaned_data.get('first_name')
      profile.user.last_name = form.cleaned_data.get('last_name')
      profile.user.save()
      profile.save()
      return redirect('tweet_list')
  else:
    form = ProfileEditForm(instance=profile)
    form.fields['first_name'].initial = request.user.first_name
    form.fields['last_name'].initial = request.user.last_name

  return render(request, 'profile/edit_profile.html', {'form': form})

@login_required
def like_tweet(request):
  tweet_id = request.GET.get('tweet_id')
  tweet = Tweet.objects.get(id=tweet_id)
  like_filter = LikeTweet.objects.filter(tweet=tweet, user=request.user).first()

  if like_filter is None:
    new_like = LikeTweet.objects.create(tweet=tweet, user=request.user)
    tweet.no_of_likes += 1
    tweet.save()
  else:
    like_filter.delete()
    tweet.no_of_likes -= 1
    tweet.save()

  return redirect('tweet_list')

@login_required
def likes_list(request):
    liked_tweets = Tweet.objects.filter(liketweet__user=request.user).order_by('-created_at')
    return render(request, 'tweet/likes_list.html', {'liked_tweets': liked_tweets})

@login_required
def save_to_favorites(request, tweet_id):
  tweet = Tweet.objects.get(id=tweet_id)
  favorite, created = Favorite.objects.get_or_create(user=request.user, tweet=tweet)
  
  if not created:
    favorite.delete()  # If it already exists, remove it (toggle functionality)

  return redirect('tweet_list')

@login_required
def favorites_list(request):
  favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
  return render(request, 'tweet/favorites_list.html', {'favorites': favorites})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    # Check if the logged-in user is already following this profile
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    # Fetch tweets by the user
    user_tweets = Tweet.objects.filter(user=user).order_by('-created_at')

    context = {
        'profile': profile,
        'user_tweets': user_tweets,
        'tweet_count': user_tweets.count(),
        'is_following': is_following,
    }
    return render(request, 'tweet/profile.html', context)


@login_required
def profile_media(request, username):
    user = get_object_or_404(User, username=username)
    tweets_with_photos = Tweet.objects.filter(user=user).exclude(photo='').order_by('-created_at')
    
    return render(request, 'tweet/profile_media.html', {
        'user': user,
        'tweets_with_photos': tweets_with_photos,
    })


@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    follow_relation, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

    if not created:
        follow_relation.delete()

    return redirect('profile', username=user_to_follow.username)


@login_required
def feed(request):
    # Get the logged-in user
    user = request.user
    
    # Get the users that the logged-in user follows
    following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
    
    # Get tweets from the logged-in user and those they follow
    tweets = Tweet.objects.filter(user__in=following_users).order_by('-created_at')
    
    # Also include the logged-in user's tweets
    user_tweets = Tweet.objects.filter(user=user)
    
    # Combine the two querysets
    all_tweets = tweets | user_tweets
    
    return render(request, 'tweet/feed.html', {'tweets': all_tweets})







