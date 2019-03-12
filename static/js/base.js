$(document).ready(function () {

    $(".navList").slideToggle("slow", function () {
        if ($("#door").hasClass("fa-door-open")) {
          $(".fas").removeClass("fa-door-open");
          $(".fas").addClass("fa-door-closed");
          console.log("inside");
        } else {
          $(".fas").removeClass("fa-door-closed");
          $(".fas").addClass("fa-door-open");
        }
      });
    
    $("#t-button").click(function () {
      console.log("inside0");
      $(".navList").slideToggle("slow", function () {
        if ($("#door").hasClass("fa-door-open")) {
          $(".fas").removeClass("fa-door-open");
          $(".fas").addClass("fa-door-closed");
          console.log("inside");
        } else {
          $(".fas").removeClass("fa-door-closed");
          $(".fas").addClass("fa-door-open");
        }
      });
    });
  
  
    $("a.active").removeClass("active");
  
    if (window.location.pathname.includes("view_tasks")) {
      $("#view_tasks").addClass("active");
    } else if (window.location.pathname.includes("edit_tasks")) {
      $("#edit_tasks").addClass("active");
    } else if (window.location.pathname.includes("create_tasks")) {
      $('#create_tasks').addClass('active');
    }


    $(".markTaskFinished").click(function(){
      console.log("hello")
      console.log($(this).find("i").attr("data-title"))
      $.ajax({
				url: "/markTaskFinished/",
				method: 'GET', // or another (GET), whatever you need
				data: {
          task_title : $(this).find('i').attr("data-title")
          
				},
				success: function (data) {
          console.log(data)
          if(data == "done"){
            // fix me:- color doesn't change upon clicking the button
            $(this).siblings(".btn").find("i").css("color","red")
          }
        }});
        
    });
  
  
  
  });