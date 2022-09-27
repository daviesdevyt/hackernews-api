window.onload = (e) => {

    const searchOut = document.querySelector("[search-out]");
    const results = document.getElementById("news");
    const more = document.getElementById("more");
    var currPage = 1;

    fetch_news()
    more.addEventListener("click", fetch_news)

    function fetch_news() {
        fetch("/api/latest-news?page=" + currPage)
        .then(res => res.json())
        .then(data => {
            currPage++
            console.log(data)
            data.forEach((element) => {
                if (element.has_next != undefined) {
                    if (element.has_next != true){
                        more.style.display = "none"
                    }
                }
                let children = searchOut.content.cloneNode(true).children
                let title = children[0]
                title.innerHTML = `<a href="/api/view-comments/${element.id}">${element.title}</a>`
                if (element.time == null) date = "No date"
                else date = new Date(element.time).toDateString()
                title.innerHTML += ` <sub>${date}</sub>`
                results.appendChild(title)
            })
        })
    }
}