$(document).ready(function() {
  
    $("#search").click(function() {
      var searchReq = $.get("/sendRequest/" + $("#points").val()+ "x" + $("#adjacency").val() + "y" + $("#startEndPoint").val());
      
    });
  
  });