$(document).ready(function() {
   $("#star5").click(function(){
           let postId = $('#postID').val()
           $('#result').empty()
           $('#result').append("<h2>Đánh giá : 5/5</h2>")
           let value = 5;
           $.ajax({
                  type : 'POST',
                  url : "/rating",
                  data : {'data':value, 'postId': postId}
                });
   })
   $("#star4").click(function(){
   let postId = $('#postID').val()
           $('#result').empty()
           $('#result').append("<h2>Đánh giá : 4/5</h2>")
           let value = 4;
           $.ajax({
                  type : 'POST',
                  url : "/rating",
                  data : {'data':value, 'postId': postId}
                });
   })
   $("#star3").click(function(){
    let postId = $('#postID').val()
           $('#result').empty()
           $('#result').append("<h2>Đánh giá : 3/5</h2>")
           let value = 3;
           $.ajax({
                  type : 'POST',
                  url : "/rating",
                  data : {'data':value, 'postId': postId}
                });
   })
   $("#star2").click(function(){
   let postId = $('#postID').val()
           $('#result').empty()
           $('#result').append("<h2>Đánh giá : 2/5</h2>")
           let value = 2;
           $.ajax({
                  type : 'POST',
                  url : "/rating",
                  data : {'data':value, 'postId': postId}
                });
   })
   $("#star1").click(function(){
    let postId = $('#postID').val()
           $('#result').empty()
           $('#result').append("<h2>Đánh giá : 1/5</h2>")
           let value = 1;
           $.ajax({
                  type : 'POST',
                  url : "/rating",
                  data : {'data':value, 'postId': postId}
                });
   })
//   $("#btnLove").click(function(){
//   let postId = $('#postID').val()
//           $.ajax({
//                  type : 'POST',
//                  url : "/add-wishlist",
//                  data : {'postId': postId}
//                });
//   })
//    $("#btnRemoveLove").click(function(){
//   let postId = $('#postID').val()
//           $.ajax({
//                  type : 'POST',
//                  url : "/delete-wishlist",
//                  data : {'postId': postId}
//                });
//   })


});