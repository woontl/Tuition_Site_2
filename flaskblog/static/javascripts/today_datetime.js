var time = new Date();
var date = time.getFullYear()+'-'+(time.getMonth()+1)+'-'+time.getDate();
document.getElementById('date-time').innerHTML=date;