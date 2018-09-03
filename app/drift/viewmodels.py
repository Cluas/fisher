from app.libs.enums import PendingStatus


class Drift:

    def __init__(self, drift, user_id):
        self.data = {}
        self.data = self.__parse(drift, user_id)

    @staticmethod
    def requester_or_contributor(drift, user_id):
        if drift.requester_id == user_id:
            you_are = 'requester'
        else:
            you_are = 'contributor'
        return you_are

    def __parse(self, drift, user_id):
        you_are = self.requester_or_contributor(drift, user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        result = {
            'you_are': you_are,
            'operator':
                drift.requester_nickname if you_are != 'requester' else drift.contributor_nickname,
            'pending_status': pending_status,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending,
        }
        return result


class Drifts:

    def __init__(self, drifts, user_id):
        self.data = []
        self.data = self.__parse(drifts, user_id)

    @staticmethod
    def __parse(drifts, user_id):
        result = [Drift(drift, user_id).data for drift in drifts]
        return result
