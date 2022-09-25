window.onload = (e) => {
    const items = document.querySelectorAll(".dropdown-item")
    const dropdownButton = document.getElementById("dropdownMenuButton")
    const searchOut = document.querySelector("[search-out]");
    const results = document.getElementById("posts");  

    items.forEach((item) => {
        item.addEventListener("click", (e) => {
            dropdownButton.innerHTML = item.innerHTML
            fetch("/api/filter-news?type="+item.innerHTML)
            .then(res => res.json())
            .then(data => {
            console.log(data)
            data.forEach((element) => {
                let children = searchOut.content.cloneNode(true).children
                let title = children[0]
                title.innerHTML = element.type +": " +element.title
                results.appendChild(title)
            })
            })
        })
    })

}