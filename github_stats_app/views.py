from django.shortcuts import render
from .models import GitHubStats
import requests


def get_github_stats(username):
    # Make a request to the GitHub API
    response = requests.get(f'https://api.github.com/users/{username}')

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        # Extract relevant information
        repos_count = data.get('public_repos', 0)
        followers_count = data.get('followers', 0)
        following_count = data.get('following', 0)

        return {
            'repos_count': repos_count,
            'followers_count': followers_count,
            'following_count': following_count,
        }
    else:
        # Handle the case where the GitHub user does not exist
        return None

def github_stats(request):
    username = request.GET.get('username', '')
    stats = None  # Initialize stats here to avoid UnboundLocalError

    if username:
        stats, created = GitHubStats.objects.get_or_create(username=username)

        if created or request.GET.get('refresh'):
            # Fetch new data from GitHub API
            github_data = get_github_stats(username)

            # Check if the GitHub user exists
            if github_data is not None:
                # Update the database
                stats.repos_count = github_data['repos_count']
                stats.followers_count = github_data['followers_count']
                stats.following_count = github_data['following_count']
                stats.save()
            else:
                # Handle the case where the GitHub user does not exist
                return render(request, 'github_stats_app/user_not_found.html', {'username': username})

    # If no username is entered, set context without stats
    context = {'username': username}

    if stats is not None:
        # Return data to render in the template
        context.update({
            'repos_count': stats.repos_count,
            'followers_count': stats.followers_count,
            'following_count': stats.following_count,
        })

    # Render the HTML template
    return render(request, 'github_stats_app/github_stats.html', context)
