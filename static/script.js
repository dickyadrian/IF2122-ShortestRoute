$(document).ready(function() {
  
    $("#search").click(function() {
      var searchReq = $.get("/sendRequest/" + $("#query").val()+ "x" + $("#test").val() + "y" + $("#hai").val());
      
    });
  
  });