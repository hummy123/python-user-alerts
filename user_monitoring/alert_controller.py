class AlertController:
    """AlertController class which exists only for namespacing reasons,"""
    """to make it clear where the static methods come from."""
    """This class and its methods are entirely stateless."""

    @staticmethod
    def get_validation_errors(payload):
        """Given a payload, returns an array indicating mismatches"""
        """between the expected format and the actual format."""
        """If no mismatches are found, returns an empty array."""
        errors = [] # String array containin mismatch descriptions

        # Code after this if-statement expects a dict and makes the assumption
        # that the payload is of this type.
        # So just verify that this is true first.
        if not isinstance(payload, dict):
            errors.append("validation error: expected payload to be of type dict")
            return errors

        # I don't think the code below needs to be commented extensively.
        # It just verifies (usually using isinstance) that the type of the given payload
        # is the same as the expected type.
        # I've found an initial request-validation pass helpful for communicating with front-end developers
        # and "feeling safe" despite dynamic typing.

        if "type" in payload:
            if payload["type"] != "deposit" and payload["type"] != "withdraw":
                errors.append("invalid field: payload.type should be equal to 'deposit' or 'withdraw'")
        else:
            errors.append("missing field: payload.type")

        if "amount" in payload:
            if isinstance(payload["amount"], str):
                try:
                    float(payload["amount"])
                except ValueError:
                    errors.append("invalid field: payload.amount should be a string convertible to a float")
            else:
                errors.append("invalid field: payload.amount should be a string convertible to a float")
        else:
            errors.append("missing field: payload.amount")

        if "user_id" in payload:
            if not isinstance(payload["user_id"], int):
                errors.append("invalid field: payload.user_id should be of type int")
        else:
            errors.append("missing field: payload.user_id")

        if "time" in payload:
            if not isinstance(payload["time"], int):
                errors.append("invalid field: payload.time should be of type int")
        else:
            errors.append("missing field: payload.time")
        return errors

    @staticmethod
    def is_amount_over_100(payload):
        """Given a payload, checks if the payload is a withdrawal and has an amount over 100"""
        return payload["type"] == "withdraw" and float(payload["amount"]) > 100

    @staticmethod
    def user_made_three_consecutive_withdrawals(userTransactions):
        """Given an array of payloads (the userTransactions array parameter),"""
        """returns true if the three most recent transactions are all withdrawals"""
        # Check if array has at least three elements first, 
        # because there is no way three consecutive withdrawals have been made
        # if the array has fewer than three elements
        if len(userTransactions) >= 3:

            # Iterate over last three elements in array.
            # If any of the last three transactions has a type
            # different from "withdraw", 
            # return false to indicate that the last three transactions
            # are not all withdrawals
            for i in range(len(userTransactions) - 1, len(userTransactions) - 4, -1):
                transaction = userTransactions[i]
                if transaction["type"] != "withdraw":
                    return False

            # Return true to indicate that last three transactions
            # are all withdrawals
            return True
        else:
            return False

    @staticmethod
    def user_made_deposits_in_increasing_amounts(userTransactions):
        """Given an array of payloads,"""
        """returns true if the last three deposits the user made have each gotten progressively larger"""
        if len(userTransactions) >= 3:
            # Break loop once we have counted three deposits like the task says
            depositsCounted = 0  

            # Store deposits relevant to alert here
            lastDeposit = 0.0
            secondLastDeposit = 0.0
            thirdLastDeposit = 0.0

            # Backwards iteration until three deposits counted
            # or we went through all elements
            for i in range(len(userTransactions) - 1, -1, -1):
                transaction = userTransactions[i]
                if transaction["type"] == "deposit":
                    depositsCounted += 1
                    amount = float(transaction["amount"])
                    if depositsCounted == 1:
                        lastDeposit = amount
                    elif depositsCounted == 2:
                        secondLastDeposit = amount
                    elif depositsCounted == 3:
                        thirdLastDeposit = amount
                        break

            if depositsCounted == 3:
                # True if three deposits have been counted,
                # and each deposit progressively gets bigger
                return lastDeposit > secondLastDeposit and secondLastDeposit > thirdLastDeposit
            else:
                return False
        else:
            return False

    @staticmethod
    def user_deposited_more_than_200_in_30_seconds(userTransactions):
        """Given an array of payloads,"""
        """returns true if the amount in the most recent 30 seconds exceeds 200"""
        # There is no way the user deposited more than 200
        # if the number of transactions they have made is 0
        if len(userTransactions) > 0:
            # Store time of most recent transaction
            # so we can break loop if we exceed 30 deconds
            mostRecentTransactionTime = userTransactions[-1]["time"]
            totalDeposited = 0

            # Backwards iterfation, summing all deposits in last 30 seconds
            for i in range(len(userTransactions) - 1, -1, -1):
                transaction = userTransactions[i]
                curTime = transaction["time"]
                if mostRecentTransactionTime - curTime > 30:
                    # Break loop if we have exceeded 30 seconds
                    break
                if transaction["type"] == "deposit":
                    totalDeposited += float(transaction["amount"])

            return totalDeposited > 200
        else:
            return False
        
    @staticmethod
    def get_user_alerts(userTransactions):
        """Given an array of payloads,"""
        """returns an array of integers, where each integer represents an alert codde"""
        alerts = []

        # Code after first if-statement assumes there is at least 1 transaction. 
        # So check that this is true, and return empty alerts array if there are no transactions
        if len(userTransactions) == 0:
            return alerts

        if AlertController.is_amount_over_100(userTransactions[-1]):
            alerts.append(1100)

        if AlertController.user_made_three_consecutive_withdrawals(userTransactions):
            alerts.append(30)

        if AlertController.user_made_deposits_in_increasing_amounts(userTransactions):
            alerts.append(300)

        if AlertController.user_deposited_more_than_200_in_30_seconds(userTransactions):
            alerts.append(123)

        return alerts
