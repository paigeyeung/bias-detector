setTimeout(function() {

//     // let elements = await self.page.$$('#siteTable > div[class*="thing"]')

//     // for(let element of elements) {
//     //     let title = await element.$eval(('p[class="title"]'), node => node.innerText.trim());
//     //     console.log(title);

        
//     // }

    let posts = document.querySelectorAll("div[class='top-matter']");
    //let titles = document.querySelectorAll("p[class='title'");

    posts.forEach(function(post){
      let title = post.querySelector("p[class='title']");
      console.log(title.querySelector("a"));

      let warning = document.createElement("div")
      warning.classList.add("warning");

      let warningText = document.createElement("p");
      warningText.textContent = `This post may be biased`;
      warning.appendChild(warningText);

      post.before(warning);
    })
  
  }, 3000);