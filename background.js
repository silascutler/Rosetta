
/*
const url = chrome.runtime.getURL('mapping.json');
console.log(url);

document.onload = 

document.body.innerHTML = document.body.innerHTML.replace("FancyBear", "hunter");
*/

const url = chrome.runtime.getURL('mapping.json');
const actor_mapping = LoadJson(url)


function update_page () {


  var elements = document.getElementsByTagName('*');

  for (var i = 0; i < elements.length; i++) {
    var element = elements[i];

    for (var j = 0; j < element.childNodes.length; j++) {
      var node = element.childNodes[j];
      console.log(node.name)
      if (node.nodeType === 3) {
        for(let i = 0; i < actor_mapping.length; i++){
          for(let a = 0; a < actor_mapping[i].aliases.length; a++){

            var text = node.nodeValue;
            
            var re = new RegExp(actor_mapping[i].aliases[a],"gi");

            var replacedText = text.replace(re, function () {
              return "<div> REPLACEMENT TEXT"
            });

            if (replacedText !== text) {
              element.replaceChild(document.createTextNode(replacedText), node);
            }
          }
        }
      }
    }
  }
}


function LoadJson(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return JSON.parse(Httpreq.responseText);          
}

document.onreadystatechange = function () {
  if (document.readyState === 'complete') {
    update_page();
  }
};


window.onload = function() {
    update_page();
}

/*
window.setInterval(function () {
  update_page();
}, 800);
*/
