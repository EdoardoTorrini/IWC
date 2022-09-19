
setTimeout(function(){
    document.body.className="";
},500);


function timerReloadEmail() {
    /* window.location.reload(); */
    setTimeout(timerReloadEmail, 500000)
}

function showPhoneMenu() {
    document.getElementById("phoneMenu").style.display = "block";
    document.getElementsByClassName("aside_alt")[0].innerHTML = "X";
    document.getElementsByClassName("aside_alt")[0].onclick = function() {
        hidePhoneMenu();
    };
}

function hidePhoneMenu() {
    document.getElementById("phoneMenu").style.display = "none";
    document.getElementsByClassName("aside_alt")[0].innerHTML = "MENU";
    document.getElementsByClassName("aside_alt")[0].onclick = function() {
        showPhoneMenu();
    };
}

function btnWriteClicked() {
    document.getElementById("wroteEmailDiv").style.display = "block";

}

function closePopWrtEmail() {
    /* gestire il salvataggio sulle bozze */
    document.getElementById("wroteEmailDiv").style.display = "none";
}

function selBox(sId, sToken) {
    console.log(sId, sToken);
    document.getElementById("sId").submit();
}

function selFileFromSystem() {
    document.getElementById("fileChooser").click();
}

function btnViewMailDetails() {
    document.getElementById("myDropdown").classList.toggle("show");
    console.log("show");
}

function ChangeAttach() {
    var elem = document.getElementById("fileChooser").files;
    var div = document.getElementById("fileAttach");
    div.innerHTML = "";

    if (elem.length < 2) {
        for (let i=0; i<elem.length; i++) {
            var str = "<label>" + elem[i].name + "</label><br>";
            div.innerHTML += str;
        }
    }
    else {
        var str = "<button class=\"dropbtn\" onmouseover=\"over()\" onmouseout=\"not_over()\">Allegati: " + elem.length + "</button><br>";
        str += "<div id=\"dropdown-content\">";

        for (let i=0; i<elem.length; i++) {
            var sLab = "<label>" + elem[i].name + "</label><br>";
            str += sLab;
        }
        str += "</div>"

        div.innerHTML += str;
    }
}

function over() {
    var div = document.getElementById("dropdown-content").style.display = "block";
}

function not_over() {
    var div = document.getElementById("dropdown-content").style.display = "none";
}

function OpenWindLogOut() {
    var nav = document.getElementById("navUser");

    if (nav.style.display == "block") {
        nav.style.display = "none";
    }
    else
        nav.style.display = "block"
}

function OpenFile(sUrl) {

    var sFUrl = "/mail/" + sUrl;
    
    window.open(sFUrl, '_blank').focus();
}

function downloadFile(sId) {
    document.getElementById(sId).submit();
}

function logOut() {
    document.getElementById("logOut").submit();
}

function ChangeHtmlDiv(sDict) {
    console.log(sDict);
}