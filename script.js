// script.js
function showImage() {
    const fileInput = document.getElementById('imageUpload');
    const imageDisplay = document.getElementById('imageDisplay');
    
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            imageDisplay.innerHTML = `<img src="${e.target.result}" width="400" />`;
        };

        reader.readAsDataURL(fileInput.files[0]);
    }
}

function predict() {
    const fileInput = document.getElementById('imageUpload');
    const predictionResult = document.getElementById('predictionResult');

    if (fileInput.files && fileInput.files[0]) {
        const formData = new FormData();
        formData.append('image', fileInput.files[0]);

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            predictionResult.innerHTML = `<p>Prediction: ${data.prediction}</p>`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        predictionResult.innerHTML = '<p>Please upload an image first.</p>';
    }
}
