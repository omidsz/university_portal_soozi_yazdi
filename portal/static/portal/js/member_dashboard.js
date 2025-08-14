const token = localStorage.getItem("access_token");
let currentEditId = null;
let currentEventEditId = null;

if (!token) {
alert("ابتدا وارد شوید.");
window.location.href = "/api/accounts/login-page/";
}

document.addEventListener("DOMContentLoaded", function () {
fetchAnnouncements();
fetchEvents();
});

// ---------------- اطلاعیه‌ها ----------------
function fetchAnnouncements() {
fetch("/api/portal/announcements/", {
  headers: {
    Authorization: "Bearer " + token,
  },
})
  .then((res) => res.json())
  .then((data) => {
    const container = document.getElementById("announcements");
    container.innerHTML = "";
    data.forEach((a) => {
      const div = document.createElement("div");
      div.className = "bg-gray-100 p-4 rounded shadow";
      div.innerHTML = `
            <h3 class="font-bold">${a.title}</h3>
            <p>${a.content}</p>
            <div class="mt-2 flex gap-2">
                <button onclick="editAnnouncement(${a.id}, '${a.title}', \`${a.content}\`)" class="text-blue-500">ویرایش</button>
                <button onclick="deleteAnnouncement(${a.id})" class="text-red-500">حذف</button>
            </div>
        `;
      container.appendChild(div);
    });
  });
}

function createAnnouncement() {
document.getElementById("create-form").classList.remove("hidden");
}

function cancelCreate() {
document.getElementById("create-form").classList.add("hidden");
}

function submitCreate() {
const title = document.getElementById("new-title").value;
const content = document.getElementById("new-content").value;

fetch("/api/portal/announcements/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer " + token,
  },
  body: JSON.stringify({ title, content }),
}).then(() => {
  fetchAnnouncements();
  cancelCreate();
});
}

function editAnnouncement(id, title, content) {
document.getElementById("edit-title").value = title;
document.getElementById("edit-content").value = content;
currentEditId = id;
document.getElementById("edit-form").classList.remove("hidden");
}

function cancelEdit() {
document.getElementById("edit-form").classList.add("hidden");
}

function submitEdit() {
const title = document.getElementById("edit-title").value;
const content = document.getElementById("edit-content").value;

fetch(`/api/portal/announcements/${currentEditId}/`, {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer " + token,
  },
  body: JSON.stringify({ title, content }),
}).then(() => {
  fetchAnnouncements();
  cancelEdit();
});
}

function deleteAnnouncement(id) {
if (confirm("آیا از حذف این اطلاعیه مطمئن هستید؟")) {
  fetch(`/api/portal/announcements/${id}/`, {
    method: "DELETE",
    headers: {
      Authorization: "Bearer " + token,
    },
  }).then(() => fetchAnnouncements());
}
}

// ---------------- رویدادها ----------------
function fetchEvents() {
  fetch("/api/portal/events/", {
    headers: {
      Authorization: "Bearer " + token,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      const list = document.getElementById("eventsList");
      list.innerHTML = "";
      data.forEach((event) => {
        const div = document.createElement("div");
        div.className =
          "bg-gray-50 p-4 rounded shadow flex justify-between items-start";
        div.innerHTML = `
          <div>
              <h4 class="font-bold text-purple-600">${event.title}</h4>
              <p class="text-sm text-gray-600">${event.description}</p>
              <p class="text-xs text-gray-400 mt-1">تاریخ رویداد: ${event.date}</p>
              <p class="text-xs text-gray-400">ظرفیت: ${event.capacity} نفر</p>
          </div>
          <div class="flex gap-2 items-center">
              <button onclick="startEditEvent(${event.id}, '${event.title}', '${event.description}', '${event.date}', ${event.capacity})"
                class="bg-yellow-400 px-2 py-1 rounded text-white">ویرایش</button>
              <button onclick="deleteEvent(${event.id})"
                class="bg-red-500 px-2 py-1 rounded text-white">حذف</button>
          </div>
        `;
        list.appendChild(div);
      });
    });
}

document.getElementById("eventForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const form = e.target;
  const data = {
    title: form.title.value,
    description: form.description.value,
    date: form.date.value,
    capacity: parseInt(form.capacity.value), // تبدیل به عدد
  };

  const url = currentEventEditId
    ? `/api/portal/events/${currentEventEditId}/`
    : "/api/portal/events/";
  const method = currentEventEditId ? "PUT" : "POST";

  fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
    body: JSON.stringify(data),
  })
    .then((res) => {
      if (!res.ok) throw new Error("خطا در ثبت یا ویرایش رویداد");
      return res.json();
    })
    .then(() => {
      document.getElementById(
        "eventResult"
      ).innerHTML = `<p class="text-green-600">رویداد با موفقیت ${
        currentEventEditId ? "ویرایش" : "ثبت"
      } شد.</p>`;
      form.reset();
      currentEventEditId = null;
      fetchEvents();
    })
    .catch((error) => {
      document.getElementById(
        "eventResult"
      ).innerHTML = `<p class="text-red-600">${error.message}</p>`;
    });
});

function startEditEvent(id, title, description, date, capacity) {
  const form = document.getElementById("eventForm");
  form.title.value = title;
  form.description.value = description;
  form.date.value = date.split("T")[0];
  form.capacity.value = capacity;
  currentEventEditId = id;
}

function deleteEvent(id) {
  if (confirm("آیا از حذف این رویداد مطمئن هستید؟")) {
    fetch(`/api/portal/events/${id}/`, {
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + token,
      },
    }).then(() => fetchEvents());
  }
}

// ---------------- خروج ----------------
function logout() {
localStorage.removeItem("access_token");
window.location.href = "/api/accounts/login-page/";
}