from flask.testing import FlaskClient

def test_missing_fields(client: FlaskClient) -> None:
    response = client.post("/event", json={})
    expectedErrors = [
        'missing field: payload.type',
        'missing field: payload.amount',
        'missing field: payload.user_id',
        'missing field: payload.time',
    ]
    assert response.json["errors"] == expectedErrors

def test_fields_wrong_type(client: FlaskClient) -> None:
    request = { "type": "hello", "amount": 23.1, "user_id": "hxz", "time": "GMT" }
    response = client.post("/event", json=request)
    # Expect errors array to indicate that there are four errors
    assert (len(response.json["errors"]) == 4)

def test_returns_user_id(client: FlaskClient) -> None:
    # This test checks that the same user ID that is given in the request
    # is returned in the response
    req1 = { "type" : "withdraw", "amount": "23.1", "user_id": 1, "time": 0}
    res1 = client.post("/event", json=req1)
    assert(res1.json["user_id"] == 1)

    req1 = { "type" : "withdraw", "amount": "23.1", "user_id": 3, "time": 0}
    res1 = client.post("/event", json=req1)
    assert(res1.json["user_id"] == 3)

    req1 = { "type" : "withdraw", "amount": "23.1", "user_id": 5, "time": 0}
    res1 = client.post("/event", json=req1)
    assert(res1.json["user_id"] == 5)

def test_alert_is_false_when_request_returns_no_alert_codes(client: FlaskClient) -> None:
    req = { "type": "withdraw", "amount": "11.11", "user_id": 0, "time": 0}
    res = client.post("/event", json=req)
    # I'm aware of the lint warning from Ruff not to check equality with false
    # but I believe the meaning is clearer in this case when that is ignored.
    assert(res.json["alert"] == False)

def test_alert_is_true_when_request_returns_at_least_one_alert_code(client: FlaskClient) -> None:
    req = { "type": "withdraw", "amount": "101.11", "user_id": 0, "time": 0}
    res = client.post("/event", json=req)
    # Lint warning not to test equality with True is more reasonable in this case
    # so it might be worth listening to, but I am not sure.
    assert(res.json["alert"] == True)

def test_get_code_1100_when_withdraw_more_than_100(client: FlaskClient) -> None:
    req = { "type": "withdraw", "amount": "101.11", "user_id": 0, "time": 0}
    res = client.post("/event", json=req)
    assert(1100 in res.json["alert_codes"])

def test_get_code_30_when_same_user_makes_three_consecutive_withdrawals(client: FlaskClient) -> None:
    req1 = { "type": "withdraw", "amount": "10.11", "user_id": 0, "time": 0}
    req2 = { "type": "withdraw", "amount": "10.11", "user_id": 0, "time": 45}
    req3 = { "type": "withdraw", "amount": "10.11", "user_id": 0, "time": 90}
    client.post("/event", json=req1)
    client.post("/event", json=req2)
    res = client.post("/event", json=req3)
    assert(30 in res.json["alert_codes"])

def test_get_code_300_when_user_makes_consecutive_and_increading_deposits(client: FlaskClient) -> None:
    req1 = { "type": "deposit", "amount": "10.11", "user_id": 0, "time": 0}
    req2 = { "type": "deposit", "amount": "10.12", "user_id": 0, "time": 45}
    req3 = { "type": "deposit", "amount": "10.13", "user_id": 0, "time": 90}
    client.post("/event", json=req1)
    client.post("/event", json=req2)
    res = client.post("/event", json=req3)
    assert(300 in res.json["alert_codes"])

def test_get_code_123_when_user_deposits_more_than_200_in_30_seconds(client: FlaskClient) -> None:
    req1 = { "type": "deposit", "amount": "99", "user_id": 0, "time": 5}
    req2 = { "type": "deposit", "amount": "53", "user_id": 0, "time": 10}
    req3 = { "type": "deposit", "amount": "77", "user_id": 0, "time": 15}
    client.post("/event", json=req1)
    client.post("/event", json=req2)
    res = client.post("/event", json=req3)
    assert(123 in res.json["alert_codes"])
