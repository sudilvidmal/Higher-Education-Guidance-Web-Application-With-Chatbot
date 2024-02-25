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
            url: "/predict",
            contentType: "application/json",
            data: JSON.stringify({ message: message }),
            success: function(response){
                var botResponse = response.answer;
                $("#messageFormeight").append(`
                    <div class="d-flex justify-content-start mb-4">
                        <div class="msg_cotainer">${botResponse}</div>
                    </div>`
                );
            }
        });
    });
});
