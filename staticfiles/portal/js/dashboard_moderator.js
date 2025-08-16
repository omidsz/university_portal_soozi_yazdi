const token = localStorage.getItem("access_token");
let currentEditId = null;
let currentEventEditId = null;

if (!token) {
alert("ابتدا وارد شوید.");
window.location.href = "/api/accounts/login-page/";
}

document.addEventListener("DOMContentLoaded", function () {
fetchAnnouncements();
fetchIdeas();
fetchEvents();
fetchUsers();
});

function fetchUsers() {
fetch("/api/accounts/api/users/", {
  headers: {
    Authorization: "Bearer " + token,
  },
})
  .then((res) => {
    if (!res.ok) {
      throw new Error("خطا در دریافت لیست کاربران");
    }
    return res.json();
  })
  .then((data) => {
    const container = document.getElementById("userList");
    container.innerHTML = "";
    if (data.length === 0) {
      container.innerHTML =
        "<p class='text-gray-500'>هیچ کاربری ثبت نشده است.</p>";
      return;
    }
    data.forEach((user) => {
      const div = document.createElement("div");
      div.className =
        "bg-white p-4 rounded shadow flex items-center justify-between";
      div.innerHTML = `
        <div>
            <h4 class="font-bold text-gray-800">${user.username}</h4>
            <p class="text-sm text-gray-600">${user.email}</p>
        </div>
    `;
      container.appendChild(div);
    });
  })
  .catch((error) => {
    const container = document.getElementById("userList");
    container.innerHTML = `<p class="text-red-500">${error.message}</p>`;
  });
}

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
      div.className = "bg-gray-50 p-4 rounded shadow space-y-2";

      // شناسه یکتا برای بخش ثبت‌نام‌ها
      const regId = `registrations-${event.id}`;

      div.innerHTML = `
        <div class="flex justify-between items-start">
            <div>
                <h4 class="font-bold text-purple-600">${event.title}</h4>
                <p class="text-sm text-gray-600">${event.description}</p>
                <p class="text-xs text-gray-400 mt-1">تاریخ رویداد: ${event.date}</p>
            </div>
            <div class="flex gap-2 items-center">
                <button onclick="viewRegistrations(${event.id}, '${regId}')" class="bg-blue-500 px-2 py-1 rounded text-white">مشاهده ثبت‌نامی‌ها</button>
                <button onclick="startEditEvent(${event.id}, \`${event.title}\`, \`${event.description}\`, '${event.date}')" class="bg-yellow-400 px-2 py-1 rounded text-white">ویرایش</button>
                <button onclick="deleteEvent(${event.id})" class="bg-red-500 px-2 py-1 rounded text-white">حذف</button>
            </div>
        </div>
        <div id="${regId}" class="hidden mt-2 bg-white border rounded p-3 text-sm space-y-1"></div>
    `;
      list.appendChild(div);
    });
  });
}

document
.getElementById("eventForm")
.addEventListener("submit", function (e) {
  e.preventDefault();
  const form = e.target;
  const data = {
    title: form.title.value,
    description: form.description.value,
    date: form.date.value,
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

function startEditEvent(id, title, description, date) {
const form = document.getElementById("eventForm");
form.title.value = title;
form.description.value = description;
form.date.value = date.split("T")[0]; // فقط بخش تاریخ را جدا می‌کند
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

function viewRegistrations(eventId, containerId) {
const container = document.getElementById(containerId);

// اگر قبلاً باز شده، مخفی کن
if (!container.classList.contains("hidden")) {
  container.classList.add("hidden");
  container.innerHTML = "";
  return;
}

fetch(`/api/portal/events/${eventId}/registrations/`, {
  headers: {
    Authorization: "Bearer " + token,
  },
})
  .then((res) => res.json())
  .then((data) => {
    container.classList.remove("hidden");
    if (data.length === 0) {
      container.innerHTML =
        "<p class='text-gray-500'>هیچ کاربری ثبت‌نام نکرده است.</p>";
    } else {
      container.innerHTML =
        "<p class='font-semibold text-gray-700 mb-1'>ثبت‌نامی‌ها:</p>";
      data.forEach((user) => {
        const item = document.createElement("p");
        item.textContent = `${user.username} (${user.email})`;
        container.appendChild(item);
      });
    }
  })
  .catch((err) => {
    container.innerHTML =
      "<p class='text-red-500'>خطا در دریافت ثبت‌نامی‌ها</p>";
    container.classList.remove("hidden");
    console.error(err);
  });
}

// ---------------- ایده‌ها ----------------
function fetchIdeas() {
fetch("/api/portal/ideas/", {
  headers: {
    Authorization: "Bearer " + token,
  },
})
  .then((res) => res.json())
  .then((data) => {
    const pending = document.getElementById("pending-ideas");
    const approved = document.getElementById("approved-ideas");
    pending.innerHTML = "";
    approved.innerHTML = "";

    data.forEach((idea) => {
      const div = document.createElement("div");
      div.className = "bg-white p-4 rounded-xl shadow";
      div.innerHTML = `
        <h4 class="font-semibold">${idea.title}</h4>
        <p>${idea.content}</p>
        ${
          idea.file
            ? `<a href="${idea.file}" target="_blank" class="text-blue-600 underline text-sm mt-2 inline-block">مشاهده فایل ضمیمه</a>`
            : ""
        }
    `;

      const actions = document.createElement("div");
      actions.className = "mt-2 flex gap-2";

      if (!idea.is_approved) {
        const approveBtn = document.createElement("button");
        approveBtn.textContent = "تایید";
        approveBtn.className =
          "px-4 py-1 bg-green-500 text-white rounded";
        approveBtn.onclick = () => {
          fetch(`/api/portal/ideas/${idea.id}/approve/`, {
            method: "POST",
            headers: { Authorization: "Bearer " + token },
          }).then(() => fetchIdeas());
        };
        actions.appendChild(approveBtn);
      }

      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "حذف";
      deleteBtn.className = "px-4 py-1 bg-red-500 text-white rounded";
      deleteBtn.onclick = () => {
        if (confirm("آیا از حذف این ایده مطمئن هستید؟")) {
          fetch(`/api/portal/ideas/${idea.id}/reject/`, {
            method: "POST", // اگر حذف ایده تأیید شده از این طریق است
            headers: { Authorization: "Bearer " + token },
          }).then(() => fetchIdeas());
        }
      };

      actions.appendChild(deleteBtn);

      div.appendChild(actions);

      if (idea.is_approved) {
        approved.appendChild(div);
      } else {
        pending.appendChild(div);
      }
    });
  });
}

function approveIdea(id) {
fetch(`/api/portal/ideas/${id}/approve/`, {
  method: "POST",
  headers: {
    Authorization: "Bearer " + token,
  },
}).then(() => fetchIdeas());
}

function rejectIdea(id) {
fetch(`/api/portal/ideas/${id}/reject/`, {
  method: "POST",
  headers: {
    Authorization: "Bearer " + token,
  },
}).then(() => fetchIdeas());
}

function deleteApprovedIdea(id) {
if (confirm("آیا از حذف این ایده تایید شده مطمئن هستید؟")) {
  fetch(`/api/portal/ideas/${id}/reject/`, {
    method: "POST", // چون API شما POST هست
    headers: {
      Authorization: "Bearer " + token,
    },
  }).then(() => fetchIdeas());
}
}



// ---------------- خروج ----------------
function logout() {
localStorage.removeItem("access_token");
window.location.href = "/api/accounts/login-page/";
}
