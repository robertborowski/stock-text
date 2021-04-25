window.addEventListener("scroll", function(){
  var header = document.querySelector("header");
  header.classList.toggle("sticky_header", window.scrollY > 0);
})