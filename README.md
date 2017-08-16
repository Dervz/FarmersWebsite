<h1>Farmers Fruits and Vegetables Fair Trade</h1> 
  
<b><i> General idea:</b> </i>
	<p>In this project I have implemented the e-commerce website called FreeTradeFruitAndVeg. 
  <p>The essential idea of it is selling farmer’s fruits and vegetables for a free trade price. 
  <p>The uniqueness of the website is that it aims to improve farmers’ life by charging more for products
 <p>it sells and dedicate all of the extra profit to the farmers to support their families. 
  
  
<b><i> Extra features:</b> </i>
<p>The bootstrap is implemented on the main page, products page, login page, sign up page and basket pages.
<p>The bootstrap chosen is rather simple but sufficient to fulfill our needs. I decided to introduce bootstrap 
<p>on all of the mention pages instead of just the main page in order to make the website look professional. 
  
  
	Ajax script is used on the products page. 
<p> Ajax’s job is to send the request to the server and inject the content into .html page dynamically. 
<p> Therefore, I implemented Ajax on the products page in order to allow user to switch between the tabs 
<p> (All products/Fruits/Vegetables) without page refreshing. 
<p> Thus, Ajax makes the website operate more efficiently by avoiding spending extra time for page refreshes 
<p> which might be especially costly to the users with slow internet/traffic. 
  
  
	To provide a Web API for the application:
<p> I used Django’s built in rest framework library to allow client 
<p> applications to retrieve data about the website. The API has the ability to serve data from the database relating
<p> to products that are currently in stock. This could be used for client applications such as price comparison websites
<p> The API whilst classing as a web API is not technically a restful API as the resources are not referential
<p> and not fully connected. The API used can be found here: /api/products
  
  
	Also, in addition to emailing user at the checkout
 <p> the email system is also implemented to confirm the registration 
 <p> by sending user’s username and password to the user. 
