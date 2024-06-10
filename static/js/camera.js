const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture-btn');
    const photoDataInput = document.getElementById('photo-data');

    let stream;
    let photosCaptured = 0;

    async function setupCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({video: true});
            video.srcObject = stream;
        } catch (err) {
            console.error("Error accessing webcam:", err);
        }
    }

    function capturePhoto() {
        // Set canvas dimensions to match video dimensions
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        //const photo = new Image();
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Set photo dimensions to match canvas dimensions

        const photoData = canvas.toDataURL('image/jpeg', 0.8);
        photoDataInput.value = photoData;

        // stopCamera();
    }

    function stopCamera() {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
    }

    function startCamera() {
        setupCamera();
    }

    setupCamera();

    captureButton.addEventListener('click', capturePhoto);

    // startButton.addEventListener('click', startCamera);