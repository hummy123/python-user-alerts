from flask import Blueprint, request, current_app
from user_monitoring.mock_db import MockDb
from user_monitoring.alert_controller import AlertController


api = Blueprint("api", __name__)

db = MockDb()

@api.post("/event")
def handle_user_event() -> dict:
    current_app.logger.info("Handling user event")

    # Check for validation errors
    validationErrors = AlertController.get_validation_errors(request.json)

    # Return response containing validation errors
    # if there is at least one error
    if (len(validationErrors) > 0):
        return { "errors": validationErrors }

    # Save transaction to mock db if there are not validation errors
    db.add_transaction(request.json)

    # Get transaction history from user's ID
    userId = request.json["user_id"]
    userTransactions = db.get_user_transactions(userId)

    # Get alerts from user's transactions
    alerts = AlertController.get_user_alerts(userTransactions)
    # If there is at least one alert returned
    hasAlert = len(alerts) > 0

    return {
        "alert": hasAlert,
        "alert_codes": alerts,
        "user_id": userId
    }
