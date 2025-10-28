import pytestimport pytest

from fastapi.testclient import TestClientfrom fastapi.testclient import TestClient

from src.app import appfrom src.app import app



client = TestClient(app)client = TestClient(app)





def test_get_activities():def test_get_activities():

    response = client.get("/activities")    response = client.get("/activities")

    assert response.status_code == 200    assert response.status_code == 200

    data = response.json()    data = response.json()

    assert isinstance(data, dict)    assert isinstance(data, dict)

    assert "Soccer Team" in data    assert "Soccer Team" in data





def test_signup_for_activity():def test_signup_and_unregister():

    email = "testuser@mergington.edu"    activity = "Soccer Team"

    activity = "Soccer Team"    email = "testuser@mergington.edu"

    # Ensure user is not already signed up    # Ensure not already signed up

    client.post(f"/activities/{activity}/unregister?email={email}")    client.post(f"/activities/{activity}/unregister?email={email}")

    response = client.post(f"/activities/{activity}/signup?email={email}")    # Sign up

    assert response.status_code == 200    response = client.post(f"/activities/{activity}/signup?email={email}")

    assert f"Signed up {email} for {activity}" in response.json()["message"]    assert response.status_code == 200

    # Try signing up again (should fail)    assert response.json()["message"] == f"Signed up {email} for {activity}"

    response2 = client.post(f"/activities/{activity}/signup?email={email}")    # Duplicate signup should fail

    assert response2.status_code == 400    response_dup = client.post(f"/activities/{activity}/signup?email={email}")

    assert "already signed up" in response2.json()["detail"]    assert response_dup.status_code == 400

    # Unregister

    response_unreg = client.post(f"/activities/{activity}/unregister?email={email}")

def test_unregister_from_activity():    assert response_unreg.status_code == 200

    email = "testuser2@mergington.edu"    assert response_unreg.json()["message"] == f"Removed {email} from {activity}"

    activity = "Soccer Team"    # Unregister again should fail

    # Sign up first    response_unreg2 = client.post(f"/activities/{activity}/unregister?email={email}")

    client.post(f"/activities/{activity}/signup?email={email}")    assert response_unreg2.status_code == 400

    response = client.post(f"/activities/{activity}/unregister?email={email}")

    assert response.status_code == 200

    assert f"Removed {email} from {activity}" in response.json()["message"]def test_signup_invalid_activity():

    # Try removing again (should fail)    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")

    response2 = client.post(f"/activities/{activity}/unregister?email={email}")    assert response.status_code == 404

    assert response2.status_code == 400

    assert "not registered" in response2.json()["detail"]

def test_unregister_invalid_activity():

    response = client.post("/activities/Nonexistent/unregister?email=foo@bar.com")

def test_signup_invalid_activity():    assert response.status_code == 404

    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
