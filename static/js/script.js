//load all products
$("#all_products_link").click(function(){
    $("#product_div").load("all_products #product_div");
});

//load fruit
$("#fruits_link").click(function(){
    $("#product_div").load("fruits #product_div");
});

//load vegetables
$("#vegetables_link").click(function(){
    $("#product_div").load("vegetables #product_div");
});
