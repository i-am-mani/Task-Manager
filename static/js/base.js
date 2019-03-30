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
  
  
    
    // $("a.active").removeClass("active");
    if (window.location.pathname.includes("ViewTasks")) {
      $("#view_tasks").addClass("active");
    } 
    else if (window.location.pathname.includes("CreateTasks")) {
      $("a.active").removeClass("active");
      $('#create_tasks').addClass('active');
    }

    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    })

    // $(".markTaskFinished").click(function(){
    //   console.log("hello")
    //   console.log($(this).find("i").attr("data-title"))
    //   $.ajax({
		// 		url: "/markTaskFinished/",
		// 		method: 'GET', // or another (GET), whatever you need
		// 		data: {
    //       task_title : $(this).find('i').attr("data-title")
          
		// 		},
		// 		success: function (data) {
    //       console.log(data)
    //       if(data == "done"){
    //         // fix me:- color doesn't change upon clicking the button
    //         $(this).siblings(".btn").find("i").css("color","red")
    //       }
    //     }});
        
    // });

    $(".alert").alert();

    $('#loadToolbar-modal').one('click',function(){
      console.log("inside the onclikc")
      var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        ['blockquote', 'code-block'],
      
        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'direction': 'rtl' }],                         // text direction
      
        [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
      
        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'align': [] }],
      
        ['clean']                                         // remove formatting button
      ];
      
      var quill = new Quill('.editor', {
        modules: {
          toolbar: toolbarOptions
        },
        theme: 'snow'
      });
    
    });


    $("#TaskForm").on("submit", function () {
      var hvalue = $("#TaskForm div .ql-editor").html();
      var area = $("#TaskForm .descArea");
      area.val(hvalue);
     }); 
  });


