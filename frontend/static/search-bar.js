window.onload = (e) => {
  
  const clearBtn = document.getElementById("clearBtn");
  const inputArea = document.getElementById("queryFind");
  const searchBtn = document.getElementById("search");
  const searchOut = document.querySelector("[search-out]");
  const results = document.getElementById("comments");
  const prevPage = document.getElementById("prev");  
  const nextPage = document.getElementById("next");
  var currPage = 1;
  
  clearBtn.addEventListener("click", clear)
  searchBtn.addEventListener("click", (e) => {
    results.innerHTML = ""
    pageNav.style.display = "block"
    currPage = 1
    fetch_news()
  })
  
  prevPage.addEventListener("click", (e) => {
      currPage--
      fetch_news()
  })
  nextPage.addEventListener("click", (e) => {
      currPage++
      fetch_news()
  })

  function fetch_news() {
    fetch("/api/search?query="+inputArea.value+"&page="+currPage)
    .then(res => res.json())
    .then(data => {
      console.log(data)
      data.forEach((element) => {
        let children = searchOut.content.cloneNode(true).children
        let title = children[0]
        title.innerHTML = element.title
        results.appendChild(title)
      })
    })
  }
  
  function clear(){
    inputArea.value = "";
  }
}