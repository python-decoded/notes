import logging
from project import app, db

from flask import jsonify, request

from project.models import User


logger = logging.getLogger(__name__)


@app.route('/users', methods=['GET'])
def users():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify(data=[i.as_dict() for i in users.items])


@app.route('/user/<int:_id>', methods=['GET'])
def user(_id: int):
    user = User.query.get_or_404(_id, description="User not found")
    return jsonify(data=user.as_dict())
