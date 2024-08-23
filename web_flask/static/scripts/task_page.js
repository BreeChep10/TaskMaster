$(document).ready(function() {
    let subtaskCount = 1;

    $(".add-subtask-btn").on("click", function() {
        subtaskCount++; // Increment the subtask count

        // Clone the first subtask
        let newSubtask = $(".subtask").first().clone();

        // Update the IDs and values in the cloned subtask
        newSubtask.find("input[type='checkbox']").attr("id", "subtaskComplete" + subtaskCount).prop("checked", false);
        newSubtask.find("label[for^='subtaskName']").attr("for", "subtaskName" + subtaskCount);
        newSubtask.find("input[type='text']").attr("id", "subtaskName" + subtaskCount).val("");

        newSubtask.find("label[for^='subtaskDesc']").attr("for", "subtaskDesc" + subtaskCount);
        newSubtask.find("textarea").attr("id", "subtaskDesc" + subtaskCount).val("");

        newSubtask.find("label[for^='subtaskStatus']").attr("for", "subtaskStatus" + subtaskCount);
        newSubtask.find("select[id^='subtaskStatus']").attr("id", "subtaskStatus" + subtaskCount).val("new");

        newSubtask.find("label[for^='subtaskPriority']").attr("for", "subtaskPriority" + subtaskCount);
        newSubtask.find("select[id^='subtaskPriority']").attr("id", "subtaskPriority" + subtaskCount).val("low");

        // Append the cloned subtask to the subtasks container
        $(".subtasks").append(newSubtask);
    });
});