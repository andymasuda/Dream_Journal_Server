import requests
import json
import time
from config import WOMBO_API_KEY

BASE_URL = "https://api.luan.tools/api/tasks/"
HEADERS = {
    'Authorization': f'bearer {WOMBO_API_KEY}',
    'Content-Type': 'application/json'
}


def send_task_to_dream_api(style_id, prompt, target_img_path=None):
    """
    Send requests to the dream API.
    prompt is the text prompt.
    style_id is which style to use (a mapping of ids to names is in the docs).
    target_img_path is an optional path to an image to influence the generation.
    """

    # Step 1) make a POST request to https://api.luan.tools/api/tasks/
    post_payload = json.dumps({
        "use_target_image": bool(target_img_path)
    })
    post_response = requests.request(
        "POST", BASE_URL, headers=HEADERS, data=post_payload)
    
    # Step 2) skip this step if you're not sending a target image otherwise,
    # upload the target image to the url provided in the response from the previous POST request.
    # if target_img_path:
    #     target_image_url = post_response.json()["target_image_url"]
    #     with open(target_img_path, 'rb') as f:
    #         fields = target_image_url["fields"]
    #         fields ["file"] = f.read()
    #         requests.request("POST", url=target_image_url["url"], files=fields)

    # Step 3) make a PUT request to https://api.luan.tools/api/tasks/{task_id}
    # where task id is provided in the response from the request in Step 1.
    task_id = post_response.json()['id']
    task_id_url = f"{BASE_URL}{task_id}"
    put_payload = json.dumps({
        "input_spec": {
            "style": style_id,
            "prompt": prompt,
            "target_image_weight": 0.1,
            "width": 960,
            "height": 1560
    }})
    requests.request(
        "PUT", task_id_url, headers=HEADERS, data=put_payload)

    # Step 4) Keep polling for images until the generation completes
    while True:
        response_json = requests.request(
            "GET", task_id_url, headers=HEADERS).json()

        state = response_json["state"]

        if state == "completed":
            r = requests.request(
                "GET", response_json["result"])
            with open("image.jpg", "wb") as image_file:
                image_file.write(r.content)
            print("image saved successfully :)")
            break

        elif state =="failed":
            print("generation failed :(")
            break

        time.sleep(3)
    return None
    # Step 5) Enjoy your beautiful artwork :3