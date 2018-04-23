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

function myseries(){
  var xhttp;
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 1) {
        document.getElementById("myserieslink").innerHTML = "<i class=\"fa fa-circle-o-notch fa-spin\" style=\"font-size:12px\"></i>";
    }
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("myserieslink").style = "display: none";
        document.getElementById("searchlink").style = "display: inline-block";
        document.getElementById("search-page").style.display = "none";
        document.getElementById("my-series-table").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "my-series/", true);
  xhttp.send();
}

function unsubscribe(id) {
  var xhttp;
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 1) {
        document.getElementById("unsubButton" + id).innerHTML = "<i class=\"fa fa-circle-o-notch fa-spin\"" +
                                                            "style=\"font-size:24px; color:white\"></i>"
    }
    if (this.readyState == 4 && this.status == 200) {
        myseries();
    }
  };
  xhttp.open("GET", "unsubscribe/" + id + "/", true);
  xhttp.send();
}

function get_myprofile() {
  var xhttp;
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("searchlink").style = "display: inline-block";
        document.getElementById("myserieslink").style = "display: inline-block";
        document.getElementById("myserieslink").innerHTML = "Sorozataim";
        document.getElementById("search-page").style.display = "none";
        document.getElementById("my-series-table").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "myprofile/", true);
  xhttp.send();
}

function post_myprofile(){
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("my-series-table").innerHTML = this.responseText;
        }
    };
    var formData = new FormData(document.getElementById("profileform"));
    xhttp.open("POST", "myprofile/", true);
    xhttp.send(formData);
}

/*function submitSearch() {
    console.log("valami");
  var xhttp;
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("search-page").style.display = "none";
        document.getElementById("my-series-table").innerHTML = this.responseText;
    }
  };
  xhttp.open("POST", "", true);
  xhttp.send("title=" + document.getElementById("title").value);
}*/
