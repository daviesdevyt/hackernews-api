window.onload = (e) => {
    const items = document.querySelectorAll(".dropdown-item")
    const dropdownButton = document.getElementById("dropdownMenuButton")
    const searchOut = document.querySelector("[search-out]");
    const pageNav = document.querySelector("[page]");
    const results = document.getElementById("posts");  
    const prevPage = document.getElementById("prev");  
    const nextPage = document.getElementById("next");  
    var currPage = 1;
    
    prevPage.addEventListener("click", (e) => {
        currPage--
        fetch_news(dropdownButton)
    })
    nextPage.addEventListener("click", (e) => {
        currPage++
        fetch_news(dropdownButton)
    })
    items.forEach((item) => item.addEventListener("click", (e) => {
        pageNav.style.display = "block"
        dropdownButton.innerHTML = item.innerHTML
        currPage = 1
        fetch_news(item)
    }))

    function fetch_news(item) {
        fetch("/api/filter-news?type="+item.innerHTML+"&page="+currPage)
        .then(res => res.json())
        .then(data => {
        results.innerText = ""
        data.forEach((element) => {
            let children = searchOut.content.cloneNode(true).children
            let title = children[0]
            title.innerHTML = element.title
            results.appendChild(title)
        })
    })}
}
