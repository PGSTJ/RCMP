document.addEventListener("DOMContentLoaded", () => {
    // Get references to elements
    const sections = document.querySelectorAll(".dashboard-section");
    const sectionHeadings = document.querySelectorAll(".section-heading");
  
    // Add event listeners to section headings for toggling sections
    sectionHeadings.forEach((heading, index) => {
      heading.addEventListener("click", () => {
        sections[index].classList.toggle("collapsed");
      });
    });
  
    // Add event listener to profile picture for displaying a notification
    const profilePicture = document.querySelector(".profile-picture");
    profilePicture.addEventListener("click", () => {
      displayNotification("Profile Picture Clicked");
    });
  
    // Function to display a notification
    function displayNotification(message) {
      const notification = document.createElement("div");
      notification.classList.add("notification");
      notification.textContent = message;
      document.body.appendChild(notification);
  
      // Remove the notification after 3 seconds
      setTimeout(() => {
        document.body.removeChild(notification);
      }, 3000);
    }
  });
  