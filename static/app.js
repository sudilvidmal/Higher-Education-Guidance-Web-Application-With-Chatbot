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
                var responseParts = botResponse.split('\n'); // Split response by newline character

                // Append each part as a separate message
                responseParts.forEach(function(part) {
                    $("#messageFormeight").append(`
                        <div class="d-flex justify-content-start mb-4">
                            <div class="msg_cotainer">${part}</div>
                        </div>`
                    );
                });

                // Check if feedback is requested
                if (response.feedback_request === "true") {
                    // If feedback is requested, show the feedback input field
                    $("#feedbackArea").show();
                }
            },
            error: function(error) {
                console.error('Error:', error);
                // Provide feedback to the user about the error
                alert('An error occurred while sending the message. Please try again later.');
            }
        });
    });

    $("#submitFeedback").click(function(){
        var feedbackText = $("#feedbackText").val();
        if (feedbackText.trim() !== "") {
            // If feedback text is not empty, submit feedback
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/submit_feedback",
                data: { feedbackText: feedbackText },
                success: function(response) {
                    alert("Thank you for your feedback!");
                    $("#feedbackArea").hide();
                    $("#feedbackText").val("");  // Clear feedback input field
                },
                error: function(error) {
                    console.error('Error:', error);
                    // Provide feedback to the user about the error
                    alert('An error occurred while sending the feedback. Please try again later.');
                }
            });
        }
    });
});
