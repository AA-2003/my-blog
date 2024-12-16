// فایل posts.js

// URL API
const API_URL = "http://127.0.0.1:8000/api/posts/";

// عنصر لیست پست‌ها
const postList = document.getElementById("post-list");

// دریافت لیست پست‌ها
fetch(API_URL)
    .then((response) => response.json())
    .then((data) => {
        data.forEach((post) => {
            // ساخت لینک به صفحه جزئیات پست
            const listItem = document.createElement("li");
            listItem.innerHTML = `
                <h2><a href="post/${post.id}/"</a></h2>
                <p>${post.content.slice(0, 100)}...</p>
            `;
            postList.appendChild(listItem);
        });
    })
    .catch((error) => {
        console.error("Error fetching posts:", error);
    });
