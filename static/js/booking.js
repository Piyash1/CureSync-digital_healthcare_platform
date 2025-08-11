// Populate date dropdowns
function populateDateDropdowns() {
    const daySelect = document.getElementById('booking-day');
    const monthSelect = document.getElementById('booking-month');
    const yearSelect = document.getElementById('booking-year');
    const currentYear = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1; // 1-12
    const currentDay = new Date().getDate();

    // Populate Days (1-31)
    for (let i = 1; i <= 31; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.text = i;
        daySelect.appendChild(option);
    }

    // Populate Months (1-12)
    for (let i = 1; i <= 12; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.text = new Date(2025, i - 1, 1).toLocaleString('default', { month: 'long' });
        monthSelect.appendChild(option);
    }

    // Populate Years (current year to +2 years)
    for (let i = currentYear; i <= currentYear + 2; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.text = i;
        yearSelect.appendChild(option);
    }

    // Set default to current date
    daySelect.value = currentDay;
    monthSelect.value = currentMonth;
    yearSelect.value = currentYear;
}

// Simulated doctor availability (based on schedule)
const doctorAvailability = {
    'dr-smith': {
        '2025-07-28': ['09:00-10:00', '11:00-12:00'], // Monday, July 28, 2025
        '2025-07-30': ['10:00-11:00', '14:00-15:00'], // Wednesday, July 30, 2025
        '2025-08-01': ['09:00-10:00', '13:00-14:00']  // Friday, August 1, 2025
    },
    'dr-jane': {
        '2025-07-29': ['09:00-10:00', '14:00-15:00'], // Tuesday, July 29, 2025
        '2025-07-31': ['10:00-11:00', '13:00-14:00'], // Thursday, July 31, 2025
    }
};

function bookAppointment() {
    const day = document.getElementById('booking-day').value;
    const month = document.getElementById('booking-month').value;
    const year = document.getElementById('booking-year').value;
    const timeSlot = document.getElementById('booking-time').value;
    const doctor = document.getElementById('booking-doctor').value;

    if (!day || !month || !year || !timeSlot || !doctor) {
        alert('Please fill in all fields.');
        return;
    }

    const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const availability = doctorAvailability[doctor] || {};

    if (availability[dateStr] && availability[dateStr].includes(timeSlot)) {
        const modal = document.getElementById('booking-modal');
        const details = document.getElementById('booking-details');
        details.textContent = `Appointment booked with ${doctor.replace('dr-', 'Dr. ')} on ${new Date(dateStr).toLocaleDateString()} at ${timeSlot}.`;
        modal.style.display = 'flex';

        const list = document.getElementById('appointments-list');
        list.innerHTML = `<li>${doctor.replace('dr-', 'Dr. ')} - ${new Date(dateStr).toLocaleDateString()} - ${timeSlot}</li>`;
    } else {
        alert(`Doctor is not available on ${new Date(dateStr).toLocaleDateString()} at ${timeSlot}. Please choose another date or time slot.`);
    }
}

function closeModal() {
    const modal = document.getElementById('booking-modal');
    modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    populateDateDropdowns();
    document.querySelector('.close').addEventListener('click', closeModal);
});