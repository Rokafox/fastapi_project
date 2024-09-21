

// ページのスクロール位置を保存する
window.addEventListener("beforeunload", function() {
    localStorage.setItem("scrollPosition", window.scrollY);
});

// ページのスクロール位置を復元する
window.addEventListener("load", function() {
    const scrollPosition = localStorage.getItem("scrollPosition");
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition));
    }
});