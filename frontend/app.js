document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('dropZone');
    const resultsSection = document.getElementById('resultsSection');
    const loadingSection = document.getElementById('loadingSection');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Tab switching functionality
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show corresponding tab content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${tabId}Tab`).classList.add('active');
        });
    });

    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('highlight');
    }

    function unhighlight() {
        dropZone.classList.remove('highlight');
    }

    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFiles);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            fileInput.files = files;
            handleFiles();
        }
    }

    function handleFiles() {
        const files = fileInput.files;
        if (files.length && isValidFileType(files[0])) {
            processFile(files[0]);
        } else {
            alert('Please upload a valid file (PDF, JPG, PNG, or DOCX)');
        }
    }

    function isValidFileType(file) {
        const validTypes = [
            'application/pdf',
            'image/jpeg',
            'image/png',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ];
        return validTypes.includes(file.type);
    }

    async function processFile(file) {
        try {
            // Show loading state
            loadingSection.style.display = 'flex';
            resultsSection.style.display = 'none';
            
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch('http://localhost:8000/extract', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Display results
            displayResults(data);
            
            // Hide loading and show results
            loadingSection.style.display = 'none';
            resultsSection.style.display = 'block';
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            console.error('Error:', error);
            loadingSection.style.display = 'none';
            alert('Error processing file. Please try again.');
        }
    }

    function displayResults(data) {
        // Display patient info
        const patientInfoContainer = document.getElementById('patientInfo');
        patientInfoContainer.innerHTML = '';
        
        if (data.patient_info) {
            const patient = data.patient_info;
            const patientFields = [
                { label: 'Name', value: patient.name, icon: 'user' },
                { label: 'Date of Birth', value: patient.dob, icon: 'calendar' },
                { label: 'Gender', value: patient.gender, icon: 'venus-mars' },
                { label: 'Patient ID', value: patient.patient_id, icon: 'id-card' },
                { label: 'Address', value: patient.address, icon: 'home' },
                { label: 'Phone', value: patient.phone, icon: 'phone' }
            ];
            
            patientFields.forEach(field => {
                if (field.value) {
                    const item = document.createElement('div');
                    item.className = 'info-item';
                    item.innerHTML = `
                        <span class="info-label"><i class="fas fa-${field.icon}"></i> ${field.label}</span>
                        <span class="info-value">${field.value}</span>
                    `;
                    patientInfoContainer.appendChild(item);
                }
            });
        }
        
        // Display medical data
        if (data.medical_record) {
            const record = data.medical_record;
            
            // Diagnosis
            const diagnosisInfo = document.getElementById('diagnosisInfo');
            if (record.diagnosis) {
                diagnosisInfo.innerHTML = `<div class="info-value">${record.diagnosis}</div>`;
            } else {
                diagnosisInfo.innerHTML = '<p>No diagnosis information found</p>';
            }
            
            // Medications
            const medicationsList = document.getElementById('medicationsList');
            medicationsList.innerHTML = '';
            if (record.medications && record.medications.length > 0) {
                record.medications.forEach(med => {
                    const li = document.createElement('li');
                    li.innerHTML = `<i class="fas fa-pills"></i> ${med}`;
                    medicationsList.appendChild(li);
                });
            } else {
                medicationsList.innerHTML = '<li>No medications found</li>';
            }
            
            // Allergies
            const allergiesList = document.getElementById('allergiesList');
            allergiesList.innerHTML = '';
            if (record.allergies && record.allergies.length > 0) {
                record.allergies.forEach(allergy => {
                    const li = document.createElement('li');
                    li.innerHTML = `<i class="fas fa-allergies"></i> ${allergy}`;
                    allergiesList.appendChild(li);
                });
            } else {
                allergiesList.innerHTML = '<li>No allergies found</li>';
            }
            
            // Procedures
            const proceduresList = document.getElementById('proceduresList');
            proceduresList.innerHTML = '';
            if (record.procedures && record.procedures.length > 0) {
                record.procedures.forEach(proc => {
                    const li = document.createElement('li');
                    li.innerHTML = `<i class="fas fa-procedures"></i> ${proc}`;
                    proceduresList.appendChild(li);
                });
            } else {
                proceduresList.innerHTML = '<li>No procedures found</li>';
            }
        }
        
        // Display raw text
        const rawTextContent = document.getElementById('rawTextContent');
        if (data.raw_text) {
            rawTextContent.textContent = data.raw_text;
        } else {
            rawTextContent.textContent = 'No text content extracted';
        }
    }
});