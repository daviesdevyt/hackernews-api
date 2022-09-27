window.onload = (e) => {
  
  const clearBtn = document.getElementById("clearBtn");
  const inputArea = document.getElementById("queryFind");
  const searchBtn = document.getElementById("search");
  const searchOut = document.querySelector("[search-out]");
  const pageNav = document.querySelector("[page]");
  const results = document.getElementById("comments");
  const nextPage = document.getElementById("next");
  const form = document.querySelector(".input_con");
  var currPage = 1;
  
  clearBtn.addEventListener("click", clear)
  searchBtn.addEventListener("click", (e) => {
    results.innerHTML = ""
    pageNav.style.display = "block"
    currPage = 1
    fetch_news()
  })
  
  nextPage.addEventListener("click", (e) => {
    currPage++
    fetch_news()
  })
  
  form.addEventListener("submit", (e) => { 
    e.preventDefault()
    results.innerHTML = ""
    pageNav.style.display = "block"
    fetch_news()
  })

  function fetch_news() {
    fetch("/api/search?query="+inputArea.value+"&page="+currPage)
    .then(res => res.json())
    .then(data => {
      console.log(data)
      data.forEach((element) => {
        if (element.has_next != undefined) {
          if (element.has_next != true){
              nextPage.style.display = "none"
          }
          return
        }
        let children = searchOut.content.cloneNode(true).children
        let title = children[0]
        title.innerHTML = `<a href="/api/view-comments/${element.id}">${element.title}</a>`
        if (element.time == null) date = "No date"
        else date = new Date(element.time).toDateString()
        title.innerHTML += ` <sub>${date}</sub> <cmts class='close' style="font-size:20px;">comments: ${element.comments.length}</cmts>`
        results.appendChild(title)
      })
    })
  }
  
  function clear(){
    inputArea.value = "";
  }
}