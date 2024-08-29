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



    let subtaskCount = 1;  // Initial count of subtasks

    // Function to add a new subtask input field
    document.getElementById("add-subtask-btn").addEventListener("click", function() {
        subtaskCount++;
        const subtaskSection = document.getElementById("subtask-section");

        // Create a new div for the subtask input
        const newSubtaskDiv = document.createElement("div");
        newSubtaskDiv.className = "subtask-section";  // Add a class name if needed

        // Create label for the new subtask input
        const newSubtaskLabel = document.createElement("label");
        newSubtaskLabel.setAttribute("for", `subtask-${subtaskCount}`);
        // newSubtaskLabel.textContent = `Subtask ${subtaskCount}:`;

        // Create new input for the subtask
        const newSubtaskInput = document.createElement("input");
        newSubtaskInput.type = "text";
        newSubtaskInput.id = `subtask-${subtaskCount}`;
        newSubtaskInput.name = "subtasks[]";  // Name with [] to handle multiple inputs as array
        newSubtaskInput.placeholder = "Enter subtask";
        newSubtaskInput.setAttribute("aria-describedby", `subtask-desc-${subtaskCount}`);


        //syle the input
        newSubtaskInput.style.width = "100%";
        newSubtaskInput.style.padding = "5px";
        newSubtaskInput.style.margin = "5px";
        newSubtaskInput.style.border = "1px solid #ccc";
        newSubtaskInput.style.borderRadius = "5px";
        newSubtaskInput.style.fontSize = "1rem";


        // Create span for accessibility description
        const newSubtaskSpan = document.createElement("span");
        newSubtaskSpan.id = `subtask-desc-${subtaskCount}`;
        newSubtaskSpan.className = "sr-only";
        newSubtaskSpan.textContent = "Enter a subtask.";

        // Append the label, input, and span to the new div
        newSubtaskDiv.appendChild(newSubtaskLabel);
        newSubtaskDiv.appendChild(newSubtaskInput);
        newSubtaskDiv.appendChild(newSubtaskSpan);

        // Append the new div to the subtask section
        subtaskSection.appendChild(newSubtaskDiv);
    });

});





    // Function to toggle edit mode for a specific task
function toggleEditTask(index) {
    // Get the task card elements by index
    const taskCard = document.getElementById(`task-card--${index}`);
    const inputs = taskCard.querySelectorAll('input.editable, textarea.editable, select');
    const editButton = taskCard.querySelector('.task-actions .action-btn:nth-child(1)');
    const saveButton = taskCard.querySelector('.task-actions .action-btn:nth-child(2)');
    const cancelButton = taskCard.querySelector('.task-actions .action-btn:nth-child(3)');

    const taskid = taskCard.getAttribute("task_id");
    console.log(taskid);

    // Enable all inputs and textarea for editing
    inputs.forEach(input => input.disabled = false);

    // Toggle button visibility
    editButton.style.display = 'none';
    saveButton.style.display = 'inline-block';
    cancelButton.style.display = 'inline-block';
}

// Function to save the edited task
function saveTask(index) {
    let item_count = 0;
    let data = {}
    const taskCard = document.getElementById(`task-card--${index}`);
    const inputs = taskCard.querySelectorAll('input.editable, textarea.editable, select');
    task_id = taskCard.getAttribute("task_id");
    data["task_id"] = task_id;
    console.log(task_id);

    // Disable all inputs after saving
    inputs.forEach(input => {
        input.disabled = true;

        if (item_count === 0){
            const name = "name"
            data[name] = input.value;

        }
        if (item_count === 1){
            const name = "status"
            data[name] = input.value;

        }
        if (item_count === 2){
            const name = "taskpriority"
            data[name] = input.value;

        }
        if (item_count === 3){
            const name = "progress"
            data[name] = input.value;

        }
        if (item_count === 4){
            const name = "description"
            data[name] = input.value;

        }
        item_count += 1;
        
    });

    data = JSON.stringify(data);

    fetch("http://0.0.0.0:5001/save_task", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: data
    })

    // Update the server or data (this is where you'd implement your AJAX or form submission)

    // Hide save and cancel buttons, show edit button again
    taskCard.querySelector('.task-actions .action-btn:nth-child(1)').style.display = 'inline-block';
    taskCard.querySelector('.task-actions .action-btn:nth-child(2)').style.display = 'none';
    taskCard.querySelector('.task-actions .action-btn:nth-child(3)').style.display = 'none';
}


// Function to delete a task

function deleteTask(index) {
    const taskCard = document.getElementById(`task-card--${index}`);
    const task_id = taskCard.getAttribute("task_id");
    console.log(task_id);
    data = JSON.stringify({"task_id": task_id});

   $.ajax({
        url: "http://0.0.0.0:5001/delete_task",
        type: "POST",
        data: data,
        contentType: "application/json",
        dataType: "json",
        success: function(response){
            console.log(response);
            taskCard.remove();
        }
    });
}

// Function to cancel the editing
function cancelEdit(index) {
    const taskCard = document.getElementById(`task-card--${index}`);
    const inputs = taskCard.querySelectorAll('input.editable, textarea.editable, select');

    // Disable all inputs to revert to non-edit mode
    inputs.forEach(input => input.disabled = true);

    // Hide save and cancel buttons, show edit button again
    taskCard.querySelector('.task-actions .action-btn:nth-child(1)').style.display = 'inline-block';
    taskCard.querySelector('.task-actions .action-btn:nth-child(2)').style.display = 'none';
    taskCard.querySelector('.task-actions .action-btn:nth-child(3)').style.display = 'none';
}


// Function to logout

