
window.onload = (e) => {
  
  const clearBtn = document.getElementById("clearBtn");
  const inputArea = document.getElementById("queryFind");
  const searchBtn = document.getElementById("search");
  const searchOut = document.querySelector("[search-out]");
  const results = document.getElementById("comments");
  
  clearBtn.addEventListener("click", clear)
  searchBtn.addEventListener("click", (e) => {
    results.innerHTML = ""
    fetch("/api/search?query="+inputArea.value)
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
  })

  function clear(){
    inputArea.value = "";
  }
}