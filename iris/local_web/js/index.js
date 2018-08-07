function start()
{
    var progressDiv = document.getElementById('progress-bar');
    var progress = document.getElementById('progress');
    var label1 = document.getElementById('label-1');
    var label2 = document.getElementById('label-2');

    try
    {
        var obj = {};
        var url = String(window.location);
        var queryString = url.split("?")[1];
        var params = queryString.split("&");
        for (var value in params)
        {
            var temp = params[value].split("=");
            obj[temp[0]] = temp[1]
        }
        var total = obj["total"];
        var current = obj["current"];
        var title = obj["title"];
        progress.max = total;
        progress.value = current;  
        label1.innerHTML = title;
        label2.innerHTML = current + " / " + total;
    } catch (e)
    {
        progressDiv.style.visibility = "hidden";
    }
}
