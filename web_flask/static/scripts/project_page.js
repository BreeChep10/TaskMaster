$(document).ready(function () {
    // Initially hide the form inside #create-project
    $("#create-project form").hide();

    // Add the 'hooverable' class initially since the form is hidden
    $("#create-project").addClass("hooverable");

    // When the <h2> inside #create-project is clicked
    $("#create-project h2").on("click", function () {
        // Toggle the visibility of the form inside #create-project
        $("#create-project form").toggle();

        // Check if the form is now visible
        if ($("#create-project form").is(":visible")) {
            // Remove the 'hooverable' class if the form is visible
            $("#create-project").removeClass("hooverable");
        } else {
            // Add the 'hooverable' class if the form is hidden
            $("#create-project").addClass("hooverable");
        }
    });
});
