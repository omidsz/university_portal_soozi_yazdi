const token = localStorage.getItem("access_token");
if (!token) {
  alert("ابتدا وارد شوید.");
  window.location.href = "/api/accounts/login-page/";
}

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  window.location.href = "/api/accounts/login-page/";
}

// ارسال ایده
document
  .getElementById("ideaForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("title", document.getElementById("ideaTitle").value);
    formData.append("content", document.getElementById("ideaContent").value);
    const file = document.getElementById("ideaFile").files[0];
    if (file) formData.append("file", file);

    fetch("/api/portal/ideas/", {
      method: "POST",
      headers: { Authorization: "Bearer " + token },
      body: formData,
    })
      .then((res) =>
        res.ok ? res.json() : res.json().then((err) => Promise.reject(err))
      )
      .then(() => {
        document.getElementById(
          "ideaResult"
        ).innerHTML = `<p class="text-green-600">ایده ارسال شد.</p>`;
        document.getElementById("ideaForm").reset();
        loadApprovedIdeas();
      })
      .catch((err) => {
        document.getElementById(
          "ideaResult"
        ).innerHTML = `<p class="text-red-600">خطا: ${err.detail || "خطا در ارسال"}</p>`;
      });
  });

function submitComment(event, eventId) {
  event.preventDefault();
  const form = event.target;
  const textarea = form.querySelector("textarea");
  const content = textarea.value;

  fetch(`/api/portal/events/${eventId}/comments/`, {
    method: "POST",
    headers: {
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content }),
  })
    .then((res) => {
      if (!res.ok) throw new Error();
      document
        .getElementById(`commentSuccess-${eventId}`)
        .classList.remove("hidden");
      document
        .getElementById(`commentError-${eventId}`)
        .classList.add("hidden");
      textarea.value = "";
    })
    .catch(() => {
      document
        .getElementById(`commentSuccess-${eventId}`)
        .classList.add("hidden");
      document
        .getElementById(`commentError-${eventId}`)
        .classList.remove("hidden");
    });
}

function toggleComments(eventId) {
  const container = document.getElementById(`commentsContainer-${eventId}`);
  if (!container.classList.contains("hidden")) {
    container.classList.add("hidden");
    return;
  }

  fetch(`/api/portal/events/${eventId}/comments/list/`, {
    headers: { Authorization: "Bearer " + token },
  })
    .then((res) => res.json())
    .then((data) => {
      container.innerHTML = data.length
        ? data
            .map(
              (c) =>
                `<p class="text-sm text-gray-700 border-b py-1">${c.content}</p>`
            )
            .join("")
        : `<p class="text-sm text-gray-500">هیچ نظری ثبت نشده است.</p>`;
      container.classList.remove("hidden");
    })
    .catch(() => {
      container.innerHTML = `<p class="text-sm text-red-600">خطا در دریافت نظرات.</p>`;
      container.classList.remove("hidden");
    });
}

function loadEvents() {
  fetch("/api/portal/events/", {
    headers: { Authorization: "Bearer " + token },
  })
    .then((res) => res.json())
    .then((data) => {
      const grid = document.getElementById("eventsGrid");
      grid.innerHTML = data.length
        ? ""
        : '<p class="text-gray-500">هیچ رویدادی وجود ندارد.</p>';
      data.forEach((event) => {
        const div = document.createElement("div");
        div.className = "bg-purple-100 rounded-xl shadow-md p-4 space-y-2";
        div.innerHTML = `
          <h3 class="text-lg font-semibold text-purple-800">${event.title}</h3>
          <p class="text-gray-700">${event.description}</p>
          <p class="text-sm text-gray-600">تاریخ: ${event.date}</p>
          <form onsubmit="submitComment(event, ${event.id})" class="space-y-2">
            <textarea rows="2" required placeholder="نظر خود را بنویسید..."
                      class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-purple-500"></textarea>
            <button type="submit" class="bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700">
              ارسال نظر
            </button>
            <div class="text-sm mt-1 text-green-600 hidden" id="commentSuccess-${event.id}">نظر ثبت شد.</div>
            <div class="text-sm mt-1 text-red-600 hidden" id="commentError-${event.id}">خطا در ارسال.</div>
          </form>
          <button onclick="registerEvent(${event.id}); return false;"
                  class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600">
            ثبت‌نام در رویداد
          </button>
          <button onclick="toggleComments(${event.id})"
                  class="text-sm text-blue-600 hover:underline">نمایش نظرات</button>
          <div id="commentsContainer-${event.id}" class="hidden mt-2 space-y-1 text-sm"></div>
        `;
        grid.appendChild(div);
      });
    });
}

function registerEvent(eventId) {
  const baseUrl = window.location.origin;
  window.location.href = `${baseUrl}/api/portal/events/showregister/?event_id=${eventId}`;
  return false;
}


function loadApprovedIdeas() {
fetch("/api/portal/ideas/approved/", {
  headers: { Authorization: "Bearer " + token },
})
  .then((res) => res.json())
  .then((data) => {
    const container = document.getElementById("approvedIdeas");
    container.innerHTML = data.length
      ? ""
      : '<p class="text-gray-500 text-sm">هیچ ایده‌ای تایید نشده.</p>';
    data.forEach((idea) => {
      const div = document.createElement("div");
      div.className = "bg-white shadow rounded p-4";
      div.innerHTML = `
<h3 class="text-lg font-bold text-purple-700">${idea.title}</h3>
<p class="mt-2 text-gray-700">${idea.content}</p>
<p class="text-sm text-gray-500 mt-1">توسط: ${
  idea.submitted_by?.username || "ناشناس"
}</p>
${
  idea.file
    ? `<a href="${idea.file}" target="_blank" class="text-blue-600 hover:underline mt-2 inline-block">مشاهده فایل PDF</a>`
    : ""
}
`;
      container.appendChild(div);
    });
  });
}
loadEvents();
loadApprovedIdeas();