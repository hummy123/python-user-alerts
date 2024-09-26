class MockDb:
    """This class contains an in-memory mock database for the task."""

    # The only data we really need to store for checking the alert conditions
    # is the list of transactions made. 
    # We use a simple dict for this.
    # The dict's keys are `user_id`s and the dict's values 
    # are arrays containing transaction data.
    db = {}

    def add_transaction(self, transaction):
        """Saves a transaction to the mock database"""
        userId = transaction["user_id"]
        if userId in self.db:
            # If userId exists, just append to the list for this user
            self.db[userId].append(transaction)
        else:
            # If userId does not exist, create new list containing transaction for user
            self.db[userId] = [transaction]

    def get_user_transactions(self, userId):
        """Returns an array of transactions for this user."""
        """If the user does not exist, returns an empty array."""
        if userId in self.db:
            return self.db[userId]
        else:
            return []
