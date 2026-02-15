
let animalsData = {};

// Modal megnyitása
function openAnimalModal(animalId) {
    const animal = animalsData[animalId];
    if (!animal) return;

    const modal = document.getElementById('animalModal');

    // Fejléc kitöltése
    const modalImage = document.getElementById('modalImage');
    if (animal.image_url) {
        modalImage.src = animal.image_url;
        modalImage.style.display = 'block';
    } else {
        modalImage.style.display = 'none';
    }

    document.getElementById('modalName').textContent = animal.name;
    document.getElementById('modalBreed').textContent =
        `${animal.species}${animal.breed ? ' • ' + animal.breed : ''} • ${animal.gender}`;
    //document.getElementById('modalChip').textContent =
        //animal.chip_number ? `Chip: ${animal.chip_number}` : '';

    // Alapadatok kitöltése
    const infoGrid = document.getElementById('modalInfoGrid');
    infoGrid.innerHTML = `
        <div class="modal__info-item">
            <span class="modal__info-label">Faj</span>
            <span class="modal__info-value">${animal.species}</span>
        </div>
        <div class="modal__info-item">
            <span class="modal__info-label">Fajta</span>
            <span class="modal__info-value">${animal.breed || 'Ismeretlen'}</span>
        </div>
        <div class="modal__info-item">
            <span class="modal__info-label">Életkor</span>
            <span class="modal__info-value">${animal.age} év</span>
        </div>
        <div class="modal__info-item">
            <span class="modal__info-label">Nem</span>
            <span class="modal__info-value">${animal.gender}</span>
        </div>
              
    `;


    // Kórtörténet kitöltése
    //renderMedicalHistory(animal.medical_history);

    // Szerkesztés gomb URL frissítése
    const editBtn = document.getElementById('modalEditBtn');
    if (editBtn) {
        editBtn.href = `/edit_animal/${animal.id}`;
    }

    // Első tab aktívvá tétele
    switchTab('info', document.querySelector('.modal__tab'));

    // Modal megjelenítése
    modal.classList.add('modal--active');
    document.body.style.overflow = 'hidden';
}


// Kórtörténet renderelése
/*function renderMedicalHistory(medicalHistory) {
    const medicalDiv = document.getElementById('modalMedical');

    if (medicalHistory && medicalHistory.length > 0) {
        medicalDiv.innerHTML = medicalHistory.map(med => `
            <div class="modal__list-item modal__list-item--info">
                <div class="modal__list-item-content">
                    <p class="modal__list-item-title">${med.date}</p>
                    <p class="modal__list-item-desc">${med.description}</p>
                </div>
            </div>
        `).join('');
    } else {
        medicalDiv.innerHTML = '<p class="modal__empty">Nincs rögzített kórtörténet.</p>';
    }
}
*/

// Modal bezárása
function closeAnimalModal() {
    const modal = document.getElementById('animalModal');
    modal.classList.remove('modal--active');
    document.body.style.overflow = '';
}

// Tab váltás
function switchTab(tabId, clickedBtn) {
    // Tab gombok
    document.querySelectorAll('.modal__tab').forEach(tab => {
        tab.classList.remove('modal__tab--active');
    });
    clickedBtn.classList.add('modal__tab--active');

    // Tab tartalmak
    document.querySelectorAll('.modal__tab-content').forEach(content => {
        content.classList.remove('modal__tab-content--active');
    });
    document.getElementById(`tab-${tabId}`).classList.add('modal__tab-content--active');
}

// Állat adatok inicializálása (a HTML-ből hívjuk)
function initAnimalsData(data) {
    animalsData = data;
}

// Event listenerek inicializálása
document.addEventListener('DOMContentLoaded', function() {
    // ESC billentyűvel bezárás
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAnimalModal();
        }
    });
});