import requests


class HTTP:
    @staticmethod
    def get(url, json_return=True):
        r = requests.get(url)
        if not r.ok:
            return {} if json_return else r.text
        return r.json() if json_return else r.text
