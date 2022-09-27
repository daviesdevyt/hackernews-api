window.onload = (e) => {
    const items = document.querySelectorAll(".dropdown-item")
    const dropdownButton = document.getElementById("dropdownMenuButton")
    const searchOut = document.querySelector("[search-out]");
    const pageNav = document.querySelector("[page]");
    const pageNum = document.querySelector("page");
    const results = document.getElementById("posts");  
    const prevPage = document.getElementById("prev");  
    const nextPage = document.getElementById("next");  
    const pageCount = document.querySelector("page-count");  
    var currPage = 1;
    
    prevPage.addEventListener("click", (e) => {
        currPage--
        if (currPage < 1) currPage = 1
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
        pageNum.innerHTML = currPage
        fetch("/api/filter-news?type="+item.innerHTML+"&page="+currPage)
        .then(res => res.json())
        .then(data => {
        results.innerText = ""
        data.forEach((element) => {
            if (element.has_next != undefined) {
                if (element.has_next != true){
                    nextPage.style.visibility = "hidden"
                }
                else{
                    nextPage.style.visibility = "visible"
                }
                if (element.has_previous != true){
                    prevPage.style.visibility = "hidden"
                }
                else{
                    prevPage.style.visibility = "visible"
                }
                if (element.page_count != undefined) pageCount.innerHTML = element.page_count
            }
            let children = searchOut.content.cloneNode(true).children
            let title = children[0]
            if (element.title != undefined) title.innerHTML = `<a href="/api/view-comments/${element.id}">${element.title}</a>`
            else if (element.text != undefined) title.innerHTML = element.text.slice(0, 50)+"..."
            else if (element.url != undefined) title.innerHTML = element.url.slice(0, 50)+"..."
            else title.innerHTML = "No presentable value"
            results.appendChild(title)
        })
    })}
}
