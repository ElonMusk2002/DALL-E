from django.shortcuts import render
import openai  # OpenAI Python library to make API calls
import requests  # used to download images
from django import forms
import os
from PIL import Image
from IPython.display import display

# Set API key
openai.api_key = "Paste_Your_API_Key_Here"

# Set a directory to save DALL-E images to
image_dir_name = "static"
image_dir = os.path.join(os.curdir, image_dir_name)

# Create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Print the directory to save to
print(f"{image_dir=}")

class ContactForm(forms.Form):
    prompt = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your prompt here'}))

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            # Call the OpenAI API
            generation_response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="url",
            )

            # Print response
            print(generation_response)

            # Save the image
            generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
            generated_image_filepath = os.path.join(image_dir, generated_image_name)
            generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
            generated_image = requests.get(generated_image_url).content  # download the image

            with open(generated_image_filepath, "wb") as image_file:
                image_file.write(generated_image)

            # Print the image filepath
            print(generated_image_filepath)

            # Display the image
            display(Image.open(generated_image_filepath))

            # Create variations
            variation_response = openai.Image.create_variation(
                image=generated_image,
                n=2,
                size="1024x1024",
                response_format="url",
            )

            # Print response
            print(variation_response)

    else:
        form = ContactForm()

    return render(request, 'layout.html', {'form': form})