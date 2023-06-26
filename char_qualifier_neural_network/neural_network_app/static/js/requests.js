async function getData() {
    var canvImage = canvas.toDataURL()
    canvImage = canvImage.replace("data:image/png;base64,", "")

    var url = base_url + "process/"
    data = {
        'image_data': canvImage
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    if(response.ok) {
        const json_response = await response.json()
        numbers = json_response["result"]       
    }
    numbers = numbers.split(" ")
    for(var i = 0; i < 44; i++) {
        var n = numbers[i] * 100
        letter_fields[i].style.width = n + '%'
    }
}
async function save_train_image(self) {
    var char = self.textContent
    var canvImage = canvas.toDataURL();
    canvImage = canvImage.replace("data:image/png;base64,", "");
    var url = base_url + "upload/"


    data = {
        'image_data': canvImage,
        'char': char
    }
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    erase()
}

async function retrain_network() {
    train_iter_count = document.getElementById("train-iter-count").value
    url = base_url + "train/"

    data = {
        'train_iter_count': train_iter_count
    }
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    setTimeout(update_train_progress, 1000);
}
async function update_train_progress() {
    var train_container = document.getElementById("train-progress-container")
    var train_progress_text = document.getElementById("train-progress-text")
    var train_progress = document.getElementById("train-progress")

    train_progress.classList.add('progress-bar-animated')
    train_progress_text.textContent = "Train progress:"
    train_container.style.display = "block"

    url = base_url + "train_progress/"

    const response = await fetch(url)

    const json_response = await response.json()
    progress = json_response["progress"]
    train_progress.style.width = progress + "%"
    train_progress.textContent = progress + "%"

    if (progress != 100) {
        setTimeout(update_train_progress, 1000);
    }
    else {
        train_progress_text.textContent = "Train completed!"
        train_progress.classList.remove('progress-bar-animated')
    }
}