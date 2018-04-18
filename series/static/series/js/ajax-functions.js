function showHint(str) {
  var xhttp;
  if (str.length < 3) {
    document.getElementById("txtHint").innerHTML = "";
    return;
  }
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      // Először szabaduljunk meg a korábbi child elemektől
      var oldtitles = document.getElementById("titles");
      while(oldtitles.firstChild){ oldtitles.removeChild(oldtitles.firstChild); }

      // Frissítsük a listát az új címekkel
      var json_res = JSON.parse(this.responseText);
      var i = 0;
      console.log(json_res["total_results"]);
      while(i<5 && i<json_res["total_results"]){
          var title = document.createElement("option");
          console.log(i + "  " + json_res["results"][i]["original_name"]);
          var name = json_res["results"][i]["original_name"];
          title.setAttribute("value", name);
          document.getElementById("titles").appendChild(title);
          i++;
      }
    }
  };
  xhttp.open("GET", "get-hint/"+str+"/", true);
  xhttp.send();
}