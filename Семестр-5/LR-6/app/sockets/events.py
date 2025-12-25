from flask import current_app, request
from flask_socketio import emit


def register_socket_events(socketio):
    """
    Registers socket events for given socketio instance.

    Listens for "connect", "subscribe", "unsubscribe" and "disconnect" events.

    Emits "client_id" event with the client's sid upon connection.
    Subscribes given codes to the RatesSubject upon subscription.
    Unsubscribes given code from the RatesSubject upon unsubscription.
    Unsubscribes all codes from the RatesSubject upon disconnection.
    """

    @socketio.on("connect")
    def connect():
        emit("client_id", {"client_id": request.sid})

    @socketio.on("subscribe")
    def subscribe(data):
        codes = data.get("codes", [])
        subject = current_app.extensions["rates_subject"]
        subject.subscribe(request.sid, codes)

    @socketio.on("unsubscribe")
    def unsubscribe(data):
        code = data.get("code")
        subject = current_app.extensions["rates_subject"]
        subject.unsubscribe(request.sid, code)

    @socketio.on("disconnect")
    def disconnect():
        subject = current_app.extensions["rates_subject"]
        subject.unsubscribe_all(request.sid)
