document.addEventListener("DOMContentLoaded", function () {
  // ฟังก์ชันสำหรับลบรูปภาพ
  const removeButtons = document.querySelectorAll(".remove-image");
  let existingImageCount = document.querySelectorAll(".image-card").length; // จำนวนรูปที่มีอยู่ใน DOM

  removeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const imageId = this.getAttribute("data-image-id");
      const imageCard = document.getElementById(`image-card-${imageId}`);

      // สร้าง input hidden สำหรับเก็บ imageId ที่ถูกลบ
      const inputRemove = document.createElement("input");
      inputRemove.type = "hidden";
      inputRemove.name = "existing_image_ids_to_remove";
      inputRemove.value = imageId;

      document.querySelector("form").appendChild(inputRemove);

      // ลบ image card ออกจาก DOM
      imageCard.remove();
      existingImageCount--; // ลดจำนวนรูปที่มีอยู่
    });
  });

  // เลือกฟิลด์สำหรับการอัปโหลดไฟล์
  const uploadInput = document.getElementById("id_upload_image");
  const maxImages = 3; // จำนวนไฟล์สูงสุดที่อนุญาต
  const allowedTypes = ["image/jpeg", "image/png", "image/gif", "image/webp"]; // ประเภทไฟล์ที่อนุญาต

  // ตรวจสอบการเลือกไฟล์ใหม่
  uploadInput.addEventListener("change", function (event) {
    // นับจำนวนไฟล์ที่ผู้ใช้เลือก
    const selectedFilesCount = uploadInput.files.length;
    const totalUploadedImages = existingImageCount + selectedFilesCount;

    // ตรวจสอบว่าไฟล์ที่เลือกจะทำให้รวมกับรูปเดิมเกิน 3 หรือไม่
    if (totalUploadedImages > maxImages) {
      alert(
        `You uploaded ${totalUploadedImages} images but you can only upload a maximum of ${maxImages} images in total.`
      );
      // Reset การเลือกไฟล์เพื่อไม่ให้เกิน
      uploadInput.value = "";
      return; // ยกเลิกการทำงานต่อไป
    }

    // ตรวจสอบ MIME type ของไฟล์
    for (let i = 0; i < selectedFilesCount; i++) {
      const file = uploadInput.files[i]; // เข้าถึงไฟล์ที่อัปโหลด

      if (!allowedTypes.includes(file.type)) {
        alert(
          "File type is not supported. Please upload JPEG, PNG, GIF, or WEBP files."
        );
        uploadInput.value = ""; // ล้างค่าไฟล์ที่ไม่ถูกต้อง
        return; // ยกเลิกการทำงานต่อไป
      }
    }
  });

  const activityType = document.getElementById("id_activity_type");
  const platformContainer = document.getElementById("platform_container");
  const locationContainer = document.getElementById("location_container");

  function updateVisibility() {
    const selectedType = activityType.value;
    if (selectedType == "online") {
      platformContainer.style.display = "block";
      locationContainer.style.display = "none";
    } else if (selectedType == "onsite") {
      platformContainer.style.display = "none";
      locationContainer.style.display = "block";
    } else if (selectedType == "hybrid") {
      platformContainer.style.display = "block";
      locationContainer.style.display = "block";
    } else {
      platformContainer.style.display = "none";
      locationContainer.style.display = "none";
    }
  }

  activityType.addEventListener("change", updateVisibility);
  updateVisibility(); // เรียกใช้ฟังก์ชันเพื่อเริ่มต้น
});

function confirmSubmit(action, activityId = null) {
  let message;
  if (action === "create") {
    message = "Are you sure you want to create this activity?";
  } else if (action === "edit") {
    message = "Are you sure you want to edit this activity?";
  }

  if (confirm(message)) {
    if (action === "create") {
      window.location.href = "{% url 'url_o_createactivity' %}";
    } else if (action === "edit" && activityId) {
      window.location.href =
        "{% url 'url_mo_editactivity' activity_id=1 %}".replace(
          "1",
          activityId
        );
    }
    return true;
  }
  return false;
}
