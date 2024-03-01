from flask import Flask, jsonify, request
import requests
import base64
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

@app.route('/api/custom_task', methods=['POST'])
def custom_task():
    data = request.get_json()
    param1 = data['param1']
    param2 = data['param2']
    param3 = data['param3']
    param4 = data['param4']

    def save_base64_to_file(base64_string, output_file):
        with open(output_file, "wb") as file:  # Используем бинарный режим записи
            file.write(base64.b64decode(base64_string))

    output_file = "base64_imagerest.txt"
    save_base64_to_file(param1, output_file)

    url = "http://127.0.0.1:7860"
    payload = {
        "init_images": [param1],
        "image_cfg_scale": 0,
        "mask_blur": 4,
        "inpainting_fill": 0,
        "prompt": "",
        "negative_prompt": "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation",
        "batch_size": 8,
        "steps": param2,
        "cfg_scale": param3,
        "denoising_strength": param4
      
    }

    try:
        response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
        r = response.json()
        

        return jsonify(r)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

