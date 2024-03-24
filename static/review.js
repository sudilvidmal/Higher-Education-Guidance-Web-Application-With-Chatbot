var btn = $('#back-button');

$(window).scroll(function () {
  if ($(window).scrollTop() > 100) {
    btn.addClass('show');
  } else {
    btn.removeClass('show');
  }
});

btn.on('click', function (e) {
  e.preventDefault();
  $('html, body').animate({ scrollTop: 0 }, '100');
});


// JavaScript function to submit review via AJAX
function submitReview() {
  var reviewText = document.getElementById("reviewText").value;
  var data = { review_text: reviewText };

  fetch("/submit_review", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === "success") {
        // Clear the text area after successful submission
        document.getElementById("reviewText").value = '';

        // Alert the user about successful submission
        alert("Review submitted successfully!");

        // Reload the page to display the updated reviews
        location.reload();
      } else {
        // Alert the user about the error
        alert("Error: " + data.message);
      }
    })
    .catch(error => {
      // Alert the user about the error
      alert("Error: " + error);
    });
}



document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.linkedin-profile-link').forEach(link => {
    link.addEventListener('click', function (event) {
      event.preventDefault();
      const name = this.getAttribute('data-name');
      const linkedinUrl = 'https://www.linkedin.com/search/results/people/?keywords=' + encodeURIComponent(name);
      window.open(linkedinUrl, '_blank'); // Open the link in a new tab
    });
  });
});


document.getElementById('seeAllReviews').addEventListener('click', function (event) {
  event.preventDefault();
  // Scroll the page to the top
  window.scrollTo({
    top: 0,
    behavior: 'smooth' // You can change this to 'auto' for instant scrolling
  });

  // Fetch all reviews from the database
  fetch("/all_reviews")
    .then(response => response.json())
    .then(data => {
      // Clear the current reviews
      document.querySelector('.bg-white').innerHTML = '';

      // Render all reviews
      data.reviews.forEach(review => {
        const reviewHTML = `
          <div class="reviews-members pt-4 pb-4">
              <div class="media">
                  <img alt="User Image" src="${review.image}" class="mr-3 rounded-pill">
                  <div class="media-body pt-2">
                      <div class="reviews-members-header">
                          <h6 class="mb-1"><a class="text-black linkedin-profile-link" href="#" data-name="${review.name}">${review.name}</a></h6>
                      </div>
                      <div class="reviews-members-body">
                          <p>${review.review_text}</p>
                      </div>
                  </div>
              </div>
          </div>
          <hr>`;
        document.querySelector('.bg-white').insertAdjacentHTML('beforeend', reviewHTML);
      });
    })
    .catch(error => console.error('Error:', error));
});



document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('.search-box').addEventListener('submit', function (event) {
    event.preventDefault();
    const keyword = document.querySelector('.form-control').value.trim(); // Get the keyword from the search box
    if (keyword !== "") {
      // Fetch reviews based on the entered keyword
      fetch("/search_reviews?keyword=" + encodeURIComponent(keyword))
        .then(response => response.json())
        .then(data => {
          // Clear the current reviews
          document.querySelector('.bg-white').innerHTML = '';

          // Render searched reviews
          data.reviews.forEach(review => {
            const reviewHTML = `
              <div class="reviews-members pt-4 pb-4">
                  <div class="media">
                      <img alt="User Image" src="${review.image}" class="mr-3 rounded-pill">
                      <div class="media-body pt-2">
                          <div class="reviews-members-header">
                              <h6 class="mb-1"><a class="text-black linkedin-profile-link" href="#" data-name="${review.name}">${review.name}</a></h6>
                          </div>
                          <div class="reviews-members-body">
                              <p>${review.review_text}</p>
                          </div>
                      </div>
                  </div>
              </div>
              <hr>`;
            document.querySelector('.bg-white').insertAdjacentHTML('beforeend', reviewHTML);
          });
        })
        .catch(error => console.error('Error:', error));
    } else {
      // If no keyword is entered, reload all reviews
      document.getElementById('seeAllReviews').click();
    }
  });
});


