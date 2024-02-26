$(document).ready(function(){
    $("#messageArea").submit(function(e){
        e.preventDefault();
        var message = $("#text").val();
        $("#messageFormeight").append(`
            <div class="d-flex justify-content-end mb-4">
                <div class="msg_cotainer_send">${message}</div>
            </div>`
        );
        $("#text").val("");

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/predict",
            contentType: "application/json",
            data: JSON.stringify({ message: message }),
            success: function(response){
                var botResponse = response.answer;
                $("#messageFormeight").append(`
                    <div class="d-flex justify-content-start mb-4">
                        <div class="msg_cotainer">${botResponse}</div>
                    </div>`
                );

                // Check if feedback is requested
                if (response.feedback_request === "true") {
                    // If feedback is requested, prompt the user for feedback
                    var userFeedback = prompt("Please provide your feedback:");
                    if (userFeedback !== null && userFeedback !== "") {
                        // If user provides feedback, send it to the server
                        storeFeedback(userFeedback);
                    }
                }
            },
            error: function(error) {
                console.error('Error:', error);
                // Provide feedback to the user about the error
                alert('An error occurred while sending the message. Please try again later.');
            }
        });
    });
});

function storeFeedback(feedbackText) {
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/predict?feedback_request=true",
        contentType: "application/json",
        data: JSON.stringify({ message: feedbackText }),
        success: function(response) {
            // Handle success response if needed
            console.log("Feedback stored successfully");
            alert("Thank you for your feedback!");
        },
        error: function(error) {
            console.error('Error:', error);
            // Provide feedback to the user about the error
            alert('An error occurred while sending the feedback. Please try again later.');
        }
    });
}
