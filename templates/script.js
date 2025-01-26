var config = {
    cUrl: 'https://api.countrystatecity.in/v1/countries',
    ckey: 'UU5wdms0Z0JzWDZJT2dpSk1MeWUyTzhjWVNTMW5kSkpQSW1mUGJYSw=='
}

var stateSelect = document.querySelector('.state');
var citySelect = document.querySelector('.city');

function loadStates() {
    stateSelect.disabled = false;
    citySelect.disabled = true;
    stateSelect.style.pointerEvents = 'auto';
    citySelect.style.pointerEvents = 'none';
    stateSelect.innerHTML = '<option value="">Select State</option>'; // Clear existing state options
    citySelect.innerHTML = '<option value="">Select City</option>'; // Clear existing city options

    fetch(`${config.cUrl}/IN/states`, { headers: { "X-CSCAPI-KEY": config.ckey } })
        .then(response => response.json())
        .then(data => {
            data.forEach(state => {
                const option = document.createElement('option');
                option.value = state.iso2;
                option.textContent = state.name;
                stateSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading states:', error));
}

function loadCities() {
    const selectedStateCode = stateSelect.value;
    citySelect.disabled = false;
    citySelect.style.pointerEvents = 'auto';
    citySelect.innerHTML = '<option value="">Select City</option>'; // Clear existing city options

    fetch(`${config.cUrl}/IN/states/${selectedStateCode}/cities`, { headers: { "X-CSCAPI-KEY": config.ckey } })
        .then(response => response.json())
        .then(data => {
            data.forEach(city => {
                const option = document.createElement('option');
                option.value = city.iso2;
                option.textContent = city.name;
                citySelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading cities:', error));
}

window.onload = loadStates; // Load states on page load
