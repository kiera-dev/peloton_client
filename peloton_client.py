"""
Based on endpoints documented at
https://app.swaggerhub.com/apis/DovOps/peloton-unofficial-api/0.2.3
"""
import requests

# Global vars
USER_AGENT = 'web'
API_BASE_URL = 'https://api.onepeloton.com'
API_HEADERS = {
    'Content-Type': 'application/json',
    'Peloton-Platform': 'web',
    'User-Agent': USER_AGENT,
}


class PelotonClient:
    """Primary client class for accessing Peloton API methods in Python."""
    def __init__(self, username=None, password=None):
        if not (username and password):
            raise ValueError('Peloton credentials not provided.')

        self.user_id = None
        self.username = username
        self.password = password
        self.session = self._init_session()

    def _init_session(self):
        """Initializes API client with provided credentials"""
        api_session = requests.Session()
        request_uri = '/auth/login'

        request_parameters = {
            'username_or_email': self.username,
            'password': self.password,
        }

        response = api_session.post(
            API_BASE_URL + request_uri,
            json=request_parameters,
            headers=API_HEADERS,
        )

        if response.status_code != 200:
            raise ValueError(
                'Session authorization failed. Check credential validity.')

        self.user_id = response.json().get('user_id')
        return api_session

    def _call_api(self, request_uri, request_parameters, fetch_all=False):
        """Performs calls against Peloton API endpoints."""
        response_data = []
        initial_response = self.session.get(
            API_BASE_URL + request_uri,
            headers=API_HEADERS,
            params=request_parameters,
        )

        if fetch_all:
            total_pages = initial_response.json().get('page_count')
            while request_parameters['page'] <= total_pages:
                response = self.session.get(
                    API_BASE_URL + request_uri,
                    headers=API_HEADERS,
                    params=request_parameters,
                )
                response_data.append(response.json())
                request_parameters['page'] += 1
        else:
            response_data.append(initial_response.json())

        return response_data

    def fetch_workouts(self, limit=10, fetch_all=False, page=0):
        """Method to fetch user's workout data.  Defaults to 10 workouts."""
        workouts = []
        request_uri = '/api/user/%s/workouts' % self.user_id
        request_parameters = {
            'page': page,
            'limit': limit,
            'joins': 'ride,ride.instructor'
        }
        response = self._call_api(request_uri,
                                  request_parameters,
                                  fetch_all=fetch_all)
        for response_data in response:
            workouts.extend(response_data.get('data'))

        return workouts

    def fetch_user_data(self):
        """Method to fetch user's account data."""
        request_uri = '/api/user/%s' % self.user_id
        request_parameters = {}
        response = self._call_api(request_uri, request_parameters)

        return response

    def fetch_user_achievements(self):
        """Method to fetch user's achievement data."""
        achievements = []
        request_uri = '/api/user/%s/achievements' % self.user_id
        request_parameters = {}
        response = self._call_api(request_uri, request_parameters)
        for response_data in response:
            achievement_categories = response_data.get('categories')
            for achievement_category in achievement_categories:
                achievements.append({
                    'type':
                    achievement_category.get('slug'),
                    'achievements':
                    achievement_category.get('achievements'),
                })

        return achievements

    def fetch_user_overview(self):
        """Method to fetch an overview of a given user's account data."""
        request_uri = '/api/user/%s/overview' % self.user_id
        request_parameters = {}
        response = self._call_api(request_uri, request_parameters)

        return response[0]

    def fetch_user_subscriptions(self):
        """Method to fetch user's subscription data."""
        request_uri = '/api/v2/user/subscriptions'
        request_parameters = {}
        response = self._call_api(request_uri, request_parameters)

        return response[0]

    def fetch_user_followers(self, limit=10, fetch_all=False):
        """Method to fetch user's follower data.  Defaults to 10 followers."""
        followers = []
        request_uri = '/api/user/%s/followers' % self.user_id
        request_parameters = {'page': 0, 'limit': limit}
        response = self._call_api(request_uri,
                                  request_parameters,
                                  fetch_all=fetch_all)
        for response_data in response:
            followers.extend(response_data.get('data'))

        return followers

    def fetch_user_following(self, fetch_all=False):
        """
        Method to fetch users that are being followed.  Defaults to 10 users.
        """
        following = []
        request_uri = '/api/user/%s/following' % self.user_id
        request_parameters = {'page': 0}
        response = self._call_api(request_uri,
                                  request_parameters,
                                  fetch_all=fetch_all)
        for response_data in response:
            following.extend(response_data.get('data'))

        return following

    def fetch_user_calendar(self):
        """Method to fetch user's calendar data."""
        request_uri = '/api/user/%s/calendar' % self.user_id
        request_parameters = {}
        response = self._call_api(
            request_uri,
            request_parameters,
        )
        return response[0]

    def fetch_user_challenges_past(self):
        """Method to fetch challenges user has joined in the past."""
        request_uri = '/api/user/%s/challenges/past' % self.user_id
        request_parameters = {'has_joined': True}
        response = self._call_api(
            request_uri,
            request_parameters,
        )
        return response[0]

    def fetch_user_challenges_current(self):
        """Method to fetch challenges user is currently participating in"""
        request_uri = '/api/user/%s/challenges/current' % self.user_id
        request_parameters = {'has_joined': True}
        response = self._call_api(
            request_uri,
            request_parameters,
        )
        return response[0]

    def fetch_ride(self, ride_id):
        """Method to fetch individual ride data."""
        request_uri = '/api/ride/%s/details' % ride_id
        request_parameters = {}
        response = self._call_api(
            request_uri,
            request_parameters,
        )

        return response[0]

    def fetch_workout_metrics(self, workout_id):
        """Method to fetch individual workout data."""
        request_uri = '/api/workout/%s/performance_graph' % workout_id
        request_parameters = {}
        response = self._call_api(
            request_uri,
            request_parameters,
        )

        return response[0]
