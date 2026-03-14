let animalsData = {};


function openMedModal(animalId) {
    document.getElementById('modal-' + animalId).classList.add('active');
}

function closeMedModal(animalId) {
    document.getElementById('modal-' + animalId).classList.remove('active');
}

document.addEventListener('DOMContentLoaded', function () {


    document.querySelectorAll('.med-modal').forEach(modal => {
        modal.addEventListener('click', function (e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });


    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.med-modal.active').forEach(modal => {
                modal.classList.remove('active');
            });
            closeAnimalModal();
        }
    });
});


function addRecord() {
    const container = document.getElementById('medical-records-container');
    const block = document.createElement('div');
    block.className = 'medical-record-block';
    block.innerHTML = `
        <hr>
        <input type="hidden" name="record_id[]" value="">
        
        <label>Vakcina:</label>
        <input type="text" name="vaccine[]" value="">

        <label>Vakcina dátuma:</label>
        <input type="date" name="vaccine_date[]" value="">

        <label>Betegség:</label>
        <input type="text" name="disease[]" value="">

        <label>Kezelés:</label>
        <input type="text" name="treatment[]" value="">

        <label>Állatorvos:</label>
        <input type="text" name="vet_name[]" value=""><br><br>

        <button type="button" onclick="removeRecord(this)">🗑 Bejegyzés törlése</button>
    `;
    container.appendChild(block);
}

function removeRecord(btn) {
    btn.closest('.medical-record-block').remove();
}

window.openAppointmentModal = function(animalId) {
    document.getElementById('appointment-modal-' + animalId).classList.add('active');
}

window.closeAppointmentModal = function(animalId) {
    document.getElementById('appointment-modal-' + animalId).classList.remove('active');
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.appointment-modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('image_upload');
    if (imageUpload) {
        imageUpload.addEventListener('change', async function() {
            const file = this.files[0];
            if (!file) return;

            const predictionText = document.getElementById('species-prediction');
            predictionText.textContent = '🔍 Elemzés folyamatban...';

            const formData = new FormData();
            formData.append('image', file);

            try {
                const res = await fetch('/predict_species', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();

                document.getElementById('image_url_hidden').value = data.image_url;

                const speciesSelect = document.getElementById('species-select');
                speciesSelect.value = data.species === 'dog' ? 'kutya' : 'macska';

                const speciesHu = data.species === 'dog' ? '🐶 Kutya' : '🐱 Macska';
                predictionText.textContent = `✅ Felismert faj: ${speciesHu}`;
                predictionText.style.color = 'green';

            } catch (err) {
                predictionText.textContent = '❌ Hiba történt az elemzés során.';
                predictionText.style.color = 'red';
            }
        });
    }
});
const imageUpload = document.getElementById('image_upload');
if (imageUpload) {
    imageUpload.addEventListener('change', async function() {
        const file = this.files[0];
        if (!file) return;

        const predictionText = document.getElementById('species-prediction');
        predictionText.textContent = '🔍 Elemzés folyamatban...';

        const formData = new FormData();
        formData.append('image', file);

        try {
            const res = await fetch('/predict_species', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();

            document.getElementById('image_url_hidden').value = data.image_url;

            const speciesSelect = document.getElementById('species-select');
            speciesSelect.value = data.species === 'dog' ? 'kutya' : 'macska';

            const speciesHu = data.species === 'dog' ? 'Kutya' : 'Macska';
            predictionText.textContent = `Felismert faj: ${speciesHu}`;
            predictionText.style.color = 'green';

        } catch (err) {
            predictionText.textContent = 'Hiba történt az elemzés során.';
            predictionText.style.color = 'red';
        }
    });
}


function toggleChat() {
    const win = document.getElementById('chatWindow');
    win.classList.toggle('active');
}

async function sendMessage() {
    const input= document.getElementById('chatInput');
    const messages = document.getElementById('chatMessages');

    const text = input.value.trim();
    if (!text) return;

    messages.innerHTML += `<div class="chat-msg chat-msg--user">${text}</div>`;
    input.value='';
    messages.scrollTop =messages.scrollHeight;

    messages.innerHTML += `<div class="chat-msg chat-msg--bot" id="typing">...</div>`;
    messages.scrollTop = messages.scrollHeight;

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: text})
        });
        const data = await res.json();
        document.getElementById('typing').remove();
        messages.innerHTML += `<div class="chat-msg chat-msg--bot">${data.reply}</div>`;
    } catch {
        document.getElementById('typing').textContent = 'Hiba történt, próbáld újra!';
    }
    messages.scrollTop = messages.scrollHeight;
}