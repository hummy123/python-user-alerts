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
