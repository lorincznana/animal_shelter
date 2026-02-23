let animalsData = {};


function openMedModal(animalId) {
    document.getElementById('modal-' + animalId).classList.add('active');
}

function closeMedModal(animalId) {
    document.getElementById('modal-' + animalId).classList.remove('active');
}

document.addEventListener('DOMContentLoaded', function () {

    // Háttérre kattintva bezárja
    document.querySelectorAll('.med-modal').forEach(modal => {
        modal.addEventListener('click', function (e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });

    // ESC billentyűvel bezárás
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
        <input type="text" name="vet_name[]" value="">

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