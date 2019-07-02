from flask_restful import Resource
from project.models import ActivityModel
from flask import request


class Activities(Resource):

    def get(self):

        _id = request.args.get('id', type=int)

        start = request.args.get('start', 1, type=int)
        page_size = request.args.get('page_size', 2, type=int)

        date_from = request.args.get('date_from', '2019-06-30', type=str)
        date_to = request.args.get('date_to', '9999-09-19', type=str)

        activities = ActivityModel.query.filter_by(user_id=_id)\
                                        .filter(ActivityModel.created_at >= date_from, ActivityModel.created_at <= date_to)\
                                        .order_by(ActivityModel.created_at.desc())\
                                        .paginate(page=start, per_page=page_size)

        return {'Activities': [activity.json() for activity in activities.items]}
