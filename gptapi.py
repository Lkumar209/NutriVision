from flask import Flask, request, jsonify
import openai
import base64

app = Flask(__name__)

# OpenAI API Key
openai.api_key = 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

@app.route("/analyze", methods=["POST"])
def analyze_image():
    # Check if the image is uploaded
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Get the image from the request
    uploaded_image = request.files['image']

    # Convert the image to a Base64 string (or another format GPT-4 can process)
    image_bytes = uploaded_image.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Create a prompt for GPT-4
    prompt = (
        "Analyze the following image and identify the food shown in it. "
        "Provide the name of the food and its nutritional values (calories, protein, carbs, fat)."
        " The image is encoded in Base64 format:\n\n"
        f"{image_base64}"
    )

    try:
        # Send the prompt to GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and return the result
        result = response['choices'][0]['message']['content']
        return jsonify({"analysis": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
