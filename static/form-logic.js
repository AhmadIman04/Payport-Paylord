/**
 * form-logic.js
 * Manages the state of the multi-page form using sessionStorage.
 * - Handles QR code scanning to pre-fill data.
 * - Manages PayPort sign-in flow: sends PIN, verifies PIN, and fetches merchant data.
 * - Correctly transforms file keys and populates menu items, including meal pictures.
 * - CORRECTED: Sends PayPort NRIC data in the correct JSON format for the backend.
 */

const PANDA_FORM_DATA_KEY = 'pandaMerchantRegistrationData';
const PANDA_QR_RELOAD_FLAG = 'pandaFormJustLoadedFromQR';

// --- Core Data & Helper Functions ---

function savePageData() {
    const form = document.querySelector('form');
    if (!form) return;
    const existingData = JSON.parse(sessionStorage.getItem(PANDA_FORM_DATA_KEY)) || {};
    const preservedFiles = existingData.files || {};
    const formData = new FormData(form);
    const currentPageData = {};
    for (const [key, value] of formData.entries()) {
        if (typeof value === 'string') { currentPageData[key] = value; }
    }
    const updatedData = { ...existingData, ...currentPageData };
    updatedData.files = preservedFiles;
    sessionStorage.setItem(PANDA_FORM_DATA_KEY, JSON.stringify(updatedData));
}

function loadStandardFields() {
    const data = JSON.parse(sessionStorage.getItem(PANDA_FORM_DATA_KEY));
    if (!data) return;
    for (const key in data) {
        if (key !== 'files' && !key.startsWith('meal_')) {
            const element = document.querySelector(`[name="${key}"]`);
            if (element && element.type !== 'file') {
                element.value = data[key];
            }
        }
    }
}

function loadFileInputs() {
    const data = JSON.parse(sessionStorage.getItem(PANDA_FORM_DATA_KEY));
    if (!data || !data.files) return;
    for (const [inputName, fileUrl] of Object.entries(data.files)) {
        if (inputName === 'json_menu') continue;
        const inputElement = document.querySelector(`input[name="${inputName}"]`);
        if (inputElement) {
            const displayContainer = inputElement.closest('.file-input-container').querySelector('.file-display');
            if (displayContainer) {
                const fileName = fileUrl.split('/').pop().split('?')[0];
                displayExistingFile(inputElement, displayContainer, decodeURIComponent(fileName), fileUrl);
            }
        }
    }
}

// --- Navigation and UI Helpers ---

function navigateTo(destinationUrl) {
    savePageData();
    window.location.href = destinationUrl;
}

function updateProgressBar() {
    const currentPage = parseInt(document.body.dataset.page || "1", 10);
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach((step, index) => {
        const pageNum = index + 1;
        step.classList.remove('bg-pink-600', 'text-white', 'bg-gray-200', 'text-gray-600', 'font-bold');
        if (pageNum < currentPage) { step.classList.add('bg-pink-600', 'text-white'); }
        else if (pageNum === currentPage) { step.classList.add('bg-pink-600', 'text-white', 'font-bold'); }
        else { step.classList.add('bg-gray-200', 'text-gray-600'); }
    });
}

function displayExistingFile(inputElement, displayContainer, fileName, fileUrl) {
    inputElement.style.display = 'none';
    displayContainer.innerHTML = `<div class="flex items-center justify-between p-2 bg-gray-100 rounded-lg"><a href="${fileUrl}" target="_blank" class="text-pink-600 hover:underline truncate" title="${fileName}">${fileName}</a><button type="button" class="ml-4 text-sm text-gray-500 hover:text-red-600" title="Change file">Change</button></div>`;
    displayContainer.querySelector('button').addEventListener('click', (e) => {
        e.preventDefault();
        displayContainer.innerHTML = '';
        displayContainer.appendChild(inputElement);
        inputElement.style.display = 'block';
    });
}


// --- API Interaction for Data Loading ---

async function fetchAndStoreMerchantData(merchantId) {
    console.log(`Fetching data for Merchant ID: ${merchantId}...`);
    try {
        const response = await fetch(`/api/merchant/${merchantId}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `Server error: ${response.status}`);
        }
        const data = await response.json();

        // Transform file keys
        if (data.files) {
            const transformedFiles = {};
            for (const originalFilename in data.files) {
                const inputName = originalFilename.substring(0, originalFilename.lastIndexOf('.')) || originalFilename;
                if (inputName) {
                    transformedFiles[inputName] = data.files[originalFilename];
                }
            }
            data.files = transformedFiles;
        }

        // Asynchronously fetch menu data and merge it
        if (data.files && data.files.json_menu) {
            const menuResponse = await fetch(data.files.json_menu);
            if (menuResponse.ok) {
                const menuData = await menuResponse.json();
                if (menuData.meals && Array.isArray(menuData.meals)) {
                    menuData.meals.forEach((meal, index) => {
                        data[`meal_name_${index}`] = meal.name || '';
                        data[`meal_price_${index}`] = meal.price || '';
                        data[`meal_description_${index}`] = meal.description || '';
                        data[`meal_category_${index}`] = meal.Category || '';
                        if (meal.picture) {
                           data[`meal_picture_${index}`] = meal.picture;
                        }
                    });
                }
            }
        }
        
        sessionStorage.setItem(PANDA_QR_RELOAD_FLAG, 'true');
        sessionStorage.setItem(PANDA_FORM_DATA_KEY, JSON.stringify(data));
        console.log("Success! Data transformed and loaded. Reloading page.");
        window.location.reload();
    } catch (e) {
        console.error(`Error fetching data: ${e.message}`);
        // Also show error in PayPort modal if it's open
        const errorDiv = document.getElementById('payport-error');
        if (errorDiv) {
            errorDiv.textContent = `Failed to load merchant data: ${e.message}`;
            errorDiv.style.display = 'block';
        }
    }
}


// --- MAIN EXECUTION BLOCK ---

document.addEventListener('DOMContentLoaded', () => {
    // Refresh detection logic
    const justLoadedFromQR = sessionStorage.getItem(PANDA_QR_RELOAD_FLAG);
    if (justLoadedFromQR) {
        sessionStorage.removeItem(PANDA_QR_RELOAD_FLAG);
    }
    const navigationEntries = performance.getEntriesByType("navigation");
    if (navigationEntries.length > 0 && navigationEntries[0].type === 'reload') {
        if (!justLoadedFromQR) {
            sessionStorage.removeItem(PANDA_FORM_DATA_KEY);
        }
    }
    
    // Load standard fields and update UI
    loadStandardFields();
    updateProgressBar();
    
    // Page-specific initializers
    if (document.querySelector('.file-input-container')) {
        loadFileInputs();
    }
    
    const menuContainer = document.getElementById('menu-items-container');
    if (menuContainer) {
        initializeMenu();
    }

    if (document.getElementById('qr-button')) {
        initializeQRScanner();
    }
    
    if (document.getElementById('payport-signin-btn')) {
        initializePayPortSignIn();
    }
});


// --- Dedicated Initializer Functions ---

function initializeMenu() {
    const menuContainer = document.getElementById('menu-items-container');
    let mealCount = 0;

    const createMenuItemHTML = (index) => `
        <div class="menu-item bg-gray-50 grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4 border border-gray-200 p-4 rounded-lg relative">
            <button type="button" onclick="this.closest('.menu-item').remove()" class="absolute top-2 right-2 bg-red-100 text-red-600 hover:bg-red-200 rounded-full p-1 w-8 h-8 flex items-center justify-center font-bold" title="Delete Meal">X</button>
            <div><label class="block text-sm font-medium text-gray-700">Meal Name</label><input type="text" name="meal_name_${index}" class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm sm:text-sm p-3" /></div>
            <div><label class="block text-sm font-medium text-gray-700">Price (RM)</label><input type="number" step="0.01" name="meal_price_${index}" class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm sm:text-sm p-3" /></div>
            <div class="md:col-span-2"><label class="block text-sm font-medium text-gray-700">Description</label><textarea name="meal_description_${index}" rows="2" class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm sm:text-sm p-3"></textarea></div>
            <div class="md:col-span-2"><label class="block text-sm font-medium text-gray-700">Category</label><select name="meal_category_${index}" class="mt-1 block w-full border-gray-300 rounded-lg shadow-sm sm:text-sm p-3"><option value="">-- Select --</option><option>Main Course</option><option>Drinks</option><option>Sides</option><option>Dessert</option></select></div>
            <div class="file-input-container md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">Meal Photo</label>
                <div class="file-display mt-1">
                    <input type="file" name="meal_picture_${index}" class="block w-full border-gray-300 rounded-lg shadow-sm text-sm file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:font-semibold file:bg-pink-50 file:text-pink-700 hover:file:bg-pink-100 p-2 cursor-pointer" />
                </div>
            </div>
        </div>`;
    
    const addMeal = () => {
        menuContainer.insertAdjacentHTML('beforeend', createMenuItemHTML(mealCount));
        mealCount++;
    };
    
    document.getElementById('add-meal-btn').addEventListener('click', addMeal);

    const data = JSON.parse(sessionStorage.getItem(PANDA_FORM_DATA_KEY)) || {};
    const meals = [];
    for (const key in data) {
        if (key.startsWith('meal_')) {
            const parts = key.split('_');
            const field = parts.slice(1, -1).join('_'); // handle field names with underscores
            const index = parseInt(parts[parts.length - 1], 10);
            if (!meals[index]) meals[index] = {};
            meals[index][field] = data[key];
        }
    }

    if (meals.length > 0) {
        meals.forEach((mealData, index) => {
            menuContainer.insertAdjacentHTML('beforeend', createMenuItemHTML(index));
            mealCount = index + 1;
            for (const field in mealData) {
                const inputName = `meal_${field}_${index}`;
                const input = menuContainer.querySelector(`[name="${inputName}"]`);
                if(input) {
                    if (field === 'picture') {
                        const displayContainer = input.closest('.file-display');
                        const fileUrl = mealData[field];
                        const fileName = fileUrl.split('/').pop().split('?')[0];
                        displayExistingFile(input, displayContainer, decodeURIComponent(fileName), fileUrl);
                    } else {
                        input.value = mealData[field];
                    }
                }
            }
        });
    } else {
        addMeal();
    }
}

function initializeQRScanner() {
    const qrButton = document.getElementById('qr-button');
    const scannerDiv = document.getElementById('qr-scanner');
    const stopBtn = document.getElementById('qr-stop');
    qrButton.addEventListener('click', () => {
        scannerDiv.style.display = 'block';
        const html5Qr = new Html5Qrcode("reader");
        html5Qr.start(
            { facingMode: "environment" }, { fps: 10, qrbox: { width: 250, height: 250 } },
            (qrCodeMessage) => {
                html5Qr.stop().then(() => {
                    scannerDiv.style.display = 'none';
                    fetchAndStoreMerchantData(qrCodeMessage);
                });
            },
            (errorMessage) => {}
        ).catch((err) => { console.error("QR Scanner Error.", err); });
        stopBtn.addEventListener('click', () => {
            if (html5Qr.isScanning) { html5Qr.stop(); }
            scannerDiv.style.display = 'none';
        });
    });
}

function initializePayPortSignIn() {
    const modal = document.getElementById('payport-modal');
    const openBtn = document.getElementById('payport-signin-btn');
    const closeBtn = document.getElementById('payport-modal-close');
    
    const step1 = document.getElementById('payport-step-1');
    const step2 = document.getElementById('payport-step-2');
    
    const infoForm = document.getElementById('payport-info-form');
    const pinForm = document.getElementById('payport-pin-form');

    const nricInput = document.getElementById('payport-nric');
    const emailInput = document.getElementById('payport-email');
    const pinInput = document.getElementById('payport-pin');

    const sendPinBtn = document.getElementById('payport-send-pin-btn');
    const verifyPinBtn = document.getElementById('payport-verify-pin-btn');
    const errorDiv = document.getElementById('payport-error');

    let storedNric = '';

    const showSpinner = (btn, show = true) => {
        btn.querySelector('.spinner').style.display = show ? 'inline-block' : 'none';
        btn.querySelector('.btn-text').style.display = show ? 'none' : 'inline-block';
        btn.disabled = show;
    };

    const showError = (message) => {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    };
    
    const hideError = () => {
        errorDiv.style.display = 'none';
    };

    const openModal = () => {
        modal.style.display = 'block';
        step1.style.display = 'block';
        step2.style.display = 'none';
        infoForm.reset();
        pinForm.reset();
        hideError();
    };

    const closeModal = () => {
        modal.style.display = 'none';
    };

    openBtn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Step 1: Send PIN
    infoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();
        showSpinner(sendPinBtn, true);

        const email = emailInput.value;
        storedNric = nricInput.value;

        try {
            const response = await fetch('/send-verification-pin-foodpanda', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            });
            const result = await response.json();
            
            if (result === true) {
                step1.style.display = 'none';
                step2.style.display = 'block';
                pinInput.focus();
            } else {
                throw new Error('Failed to send PIN. Please try again.');
            }
        } catch (err) {
            showError(err.message);
        } finally {
            showSpinner(sendPinBtn, false);
        }
    });

    // Step 2: Verify PIN and fetch data
    pinForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();
        showSpinner(verifyPinBtn, true);
        
        const pin = pinInput.value;

        try {
            // 1. Check PIN
            const pinCheckResponse = await fetch(`/check_pin?pin=${pin}`);
            const pinResult = await pinCheckResponse.json();

            if (pinResult !== true) {
                throw new Error('Invalid PIN. Please try again.');
            }

            // 2. Get Merchant ID by NRIC
            // --- THIS BLOCK IS THE ONLY PART THAT HAS CHANGED ---
            const merchantIdResponse = await fetch(`/get_merchant_id_by_nric?nric=${storedNric}`, { method: 'POST' });
            // --- END OF CHANGED BLOCK ---

            if (!merchantIdResponse.ok) {
                // Try to parse error from backend, otherwise show generic error
                let errorMsg = 'Could not find a merchant account with that NRIC.';
                try {
                    const errorJson = await merchantIdResponse.json();
                    errorMsg = errorJson.detail || errorMsg;
                } catch(e) {
                    // Ignore if response is not JSON
                }
                throw new Error(errorMsg);
            }
            
            const merchantId = await merchantIdResponse.json();
            
            if (!merchantId) {
                 throw new Error('Merchant ID not found for the provided NRIC.');
            }

            // 3. Fetch all data and reload page (re-uses existing function)
            await fetchAndStoreMerchantData(merchantId);

        } catch (err) {
            showError(err.message);
            pinInput.value = ''; // Clear pin input on error
        } finally {
            showSpinner(verifyPinBtn, false);
        }
    });
}
