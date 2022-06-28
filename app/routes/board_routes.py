from flask import Blueprint, request, jsonify, make_response
from app import db
from app.helper_functions import create_record_safely, success_message_info_as_list
from app.models.board import Board
from app.helper_functions import success_message_info_as_list, get_record_by_id, return_database_info_dict

board_bp = Blueprint('Boards', __name__, url_prefix='/boards')

# create one board
@board_bp.route("", methods=["POST"])
def create_new_board():
    request_body = request.get_json()
    new_board = create_record_safely(Board, request_body)

    db.session.add(new_board)
    db.session.commit()

    return success_message_info_as_list(dict(board=new_board.self_to_dict()), 201)

# read all boards
@board_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    boards_response = [board.self_to_dict() for board in boards]
    return success_message_info_as_list(boards_response, status_code=200)


# reading one board
@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = get_record_by_id(Board, board_id)
    return return_database_info_dict("board", board.self_to_dict())

# read all cards by board id
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board_id(board_id):
    board = get_record_by_id(Board, board_id)

    return success_message_info_as_list(board.self_to_dict())

# def get_record_by_id(cls, id):
#     try:
#         id = int(id)
#     except ValueError:
#         error_message(f"Invalid id: {id}", 400)
#     record = cls.query.get(id)
#     if record:
#         return record
#     else:
#         error_message(f"{cls.return_class_name()} id: {id} not found", 404)
