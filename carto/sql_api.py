import requests
import time

SQL_API_URL = '{api_version}/sql'
SQL_BATCH_API_URL = '{api_version}/sql/job/'

class SQLCLient(object):
    """
    Allows you to send requests to Carto's SQL API
    """

    def __init__(self, auth_client, api_version='v2'):
        """
        :param auth_client: Auth client to make authorized requests, such as APIKeyAuthClient
        :param sql_api_version: Current version is 'v2'. 'v1' can be used to avoid caching, but it's not guaranteed to work
        :return:
        """
        self.auth_client = auth_client
        self.api_url = SQL_API_URL.format(api_version=api_version)

    def send(self, sql, parse_json=True, do_post=True, format=None):
        """
        Executes SQL query in a Carto server
        :param sql:
        :param parse_json: Set it to False if you want raw reponse
        :param do_post: Set it to True to force post request
        :param format: Any of the data export formats allowed by Carto's SQL API
        :return: response data, either as json or as a regular response.content object
        """
        params = {'q': sql}
        if format:
            params['format'] = format
            if format not in ['json', 'geojson']:
                parse_json = False

        if len(sql) < self.auth_client.MAX_GET_QUERY_LEN and do_post is False:
            resp = self.auth_client.send(self.api_url, 'GET', params=params)
        else:
            resp = self.auth_client.send(self.api_url, 'POST', body=params)

        return self.auth_client.get_response_data(resp, parse_json)


class BatchSQLClient(object):

    def __init__(self, auth_client, api_version='v2'):
        self.auth_client = auth_client
        self.api_url = SQL_BATCH_API_URL.format(api_version=api_version)

    def create(self, sql_query, api_key):
        header = {'content-type': 'application/json'}
        data = requests.post('https://rsharan.cartodb.com/api/' + self.api_url + "?api_key=" + api_key, json={"query": sql_query}, headers=header)
        print(data.json())
        return data.json()['job_id']

    def read(self, job_id, api_key):
        header = {'content-type': 'application/json'}
        data = requests.get('https://rsharan.cartodb.com/api/' + self.api_url + job_id + "?api_key=" + api_key, headers=header)
        print(data.json())
        return data.json()




class BatchSQLManager(object):
    def __init__(self, client):
        self.client = client

    def get(self):
        pass




