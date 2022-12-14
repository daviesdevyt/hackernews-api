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
                return
            }
            let children = searchOut.content.cloneNode(true).children
            let title = children[0]
            let text
            if (element.title != undefined && "comment" != element.type) text = element.title
            else if (element.text != undefined) text = element.text.slice(0, 50)+"..."
            else if (element.url != undefined) text = element.url.slice(0, 50)+"..."
            else text = "No text nor title nor url"

            if ("comment" != element.type) title.innerHTML = `<a href="/api/post/${element.id}">${text}</a>`
            else title.innerHTML = text
            
            if (element.time == null) date = "No date"
            else date = new Date(element.time).toDateString()
            if ("comment" != element.type) title.innerHTML += `<sub>${date}</sub> <a href="/api/comments/${element.id}"><cmts class='close' style="font-size:20px;">| comments: ${element.comments.length}</cmts></a>`
            if ("poll" == element.type) title.innerHTML += `<a href="/api/polloptions/${element.id}"><cmts class='close' style="font-size:20px;">polls: ${element.poll_options.length}</cmts> `
            results.appendChild(title)
        })
    })}
}
