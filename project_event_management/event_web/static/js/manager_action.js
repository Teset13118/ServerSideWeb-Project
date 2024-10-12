function deleteActivity(activityId, csrf_token) {
  if (confirm("Are you sure you want to delete this activity?")) {
    fetch(`/manage/activities/delete/${activityId}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
    }).then((response) => {
      if (response.ok) {
        alert("Activity deleted successfully");
        window.location.reload();
      } else {
        alert("Error deleting activity");
      }
    });
  }
}

function approveActivity(activityId, csrf_token) {
  if (confirm("Are you sure you want to approve this activity?")) {
    fetch(`/manage/activities/approve/${activityId}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
    }).then((response) => {
      if (response.ok) {
        alert("Activity approved successfully");
        window.location.reload();
      } else {
        alert("Error approving activity");
      }
    });
  }
}

function deleteUser(userId, csrf_token) {
  if (confirm("Are you sure you want to delete this user?")) {
    fetch(`/manage/users/delete/${userId}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
      },
    }).then((response) => {
      if (response.ok) {
        alert("User deleted successfully");
        window.location.reload();
      } else {
        alert("Error deleting user");
      }
    });
  }
}

function deleteReview(reviewId, csrf_token) {
  if (confirm("Are you sure you want to delete this review?")) {
      fetch(`/manage/reviews/delete/${reviewId}/`, {
      method: "DELETE",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf_token,
      },
      })
      .then((response) => {
      if (response.ok) {
          alert("Review deleted successfully");
          window.location.reload();
      } else {
          alert("Error deleting review");
      }
      })
      .catch((error) => {
      });
  }
}