document.addEventListener("DOMContentLoaded", function () {
    const showFormBtn = document.getElementById("show-task-form-btn");
    const newTaskForm = document.getElementById("new-task-form");
    const closeFormBtn = document.getElementById("close-task-form-btn");

    showFormBtn.addEventListener("click", function () {
        newTaskForm.style.display = "block";
        newTaskForm.setAttribute("aria-hidden", "false");
        showFormBtn.style.display = "none";
        showFormBtn.setAttribute("aria-expanded", "true");
    });

    closeFormBtn.addEventListener("click", function () {
        newTaskForm.style.display = "none";
        newTaskForm.setAttribute("aria-hidden", "true");
        showFormBtn.style.display = "block";
        showFormBtn.setAttribute("aria-expanded", "false");
    });
});


    // Function to toggle edit mode for a specific task
function toggleEditTask(index) {
    // Get the task card elements by index
    const taskCard = document.getElementById(`task-card-${index}`);
    const inputs = taskCard.querySelectorAll('input.editable, textarea.editable, select');
    const editButton = taskCard.querySelector('.task-actions .action-btn:nth-child(1)');
    const saveButton = taskCard.querySelector('.task-actions .action-btn:nth-child(2)');
    const cancelButton = taskCard.querySelector('.task-actions .action-btn:nth-child(3)');

    // Enable all inputs and textarea for editing
    inputs.forEach(input => input.disabled = false);

    // Toggle button visibility
    editButton.style.display = 'none';
    saveButton.style.display = 'inline-block';
    cancelButton.style.display = 'inline-block';
}

// Function to save the edited task
function saveTask(index) {
    const taskCard = document.getElementById(`task-card-${index}`);
    const inputs = taskCard.querySelectorAll('input.editable, textarea.editable, select');

    // Disable all inputs after saving
    inputs.forEach(input => input.disabled = true);

    // Update the server or data (this is where you'd implement your AJAX or form submission)

    // Hide save and cancel buttons, show edit button again
    taskCard.querySelector('.task-actions .action-btn:nth-child(1)').style.display = 'inline-block';
    taskCard.querySelector('.task-actions .action-btn:nth-child(2)').style.display = 'none';
    taskCard.querySelector('.task-actions .action-btn:nth-child(3)').style.display = 'none';
}

// Function to cancel the editing
function cancelEdit(index) {
    const taskCard = document.getElementById(`task-card-${index}`);
    const inputs = taskCard.querySelectorAll('input.editable, textarea.editable, select');

    // Disable all inputs to revert to non-edit mode
    inputs.forEach(input => input.disabled = true);

    // Hide save and cancel buttons, show edit button again
    taskCard.querySelector('.task-actions .action-btn:nth-child(1)').style.display = 'inline-block';
    taskCard.querySelector('.task-actions .action-btn:nth-child(2)').style.display = 'none';
    taskCard.querySelector('.task-actions .action-btn:nth-child(3)').style.display = 'none';
}