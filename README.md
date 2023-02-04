- [Templates:](#templates)
  - [index.html template:](#indexhtml-template)
  - [search.html template:](#searchhtml-template)
  - [rentals.html template:](#rentalshtml-template)
  - [Ratings component](#ratings-component)
  - [comments.html template](#commentshtml-template)
  - [login.html template:](#loginhtml-template)
  - [register.html template:](#registerhtml-template)
- [Database: rentals.db](#database-rentalsdb)
  - [Tables:](#tables)
    - [users](#users)
    - [rentals](#rentals)
    - [posts](#posts)
    - [comments](#comments)
    - [ratings](#ratings)
- [Maps](#maps)

# Templates:

index.html
search.html
rentals.html
login.html
register.html

## index.html template:

*  Display rental apartments
*  Every post has:
    *  images that show what rentals have been listed
    *  description(name, rental price, location)
    *  ratings
    *  comments under it
*  comments cannot contain phone numbers to prevent scammers
*  Posts can have many comments
*  Users can have many comments
*  Users can only rate a rental post once
*  Rentals can have many ratings
*  ratings belong to one user
*   each rental post is clickable and can be opened

## search.html template:

*  Display search results
*  Includes a map for users to locate rentals

## rentals.html template:

*  Display available rentals
*  Users can register a rental by adding the following information:
    *  name of rental building
    *  location details
    *  Images
    *  Rental price
    *  Number of rooms available
*  Rentals submitted will only be added after they have been approved by an admin
*  Rentals are divided into areas
*  Rentals have ratings based on the following criteria:
    *  Landlord strictness
    *  Quality of rooms
    *  Size of rooms
    *  Security of the area and residence
    *  Rental price


## Ratings component
*  Rentals have ratings based on the following criteria:
    *  Landlord strictness
    *  Quality of rooms
    *  Size of rooms
    *  Security of the area and residence
    *  Rental price


*   `location forms option should be two buttons, one that fetches current location and one that user   can pin location on map. the pin location might be harder since user cannot add location address, probably nearest location, shops, directions?`

## comments.html template
*   references rentals_id
*   has a comment form
*

## login.html template:

*  Allows existing users to log in
*  Gmail authentication as an option

## register.html template:

*  Allows new users to create a profile
*  Profile includes a username, email, and password
*  email should be hidden for privacy


The new information added that users can now submit their own rentals with all required details location, images, number of rooms available and the rental price. This rental will only be added to the website after it has been approved by an admin. It has been specified under the register rentals idea on rentals.html template. This way the website administrator can approve the listings before they are visible on the website.



# Database: rentals.db

## Tables:

### users
   * id (Primary key)
   * username
   * email (Must have a gmail suffix)
   * password

### rentals
  * id (Primary key)
  * images
  * number_of_rooms
  * name of rental building
  * rent price
  * location(since we can't delete a column)
  * latitude
  * longitude

### posts
  * id (Primary key)
  * rental_id (Foreign key referencing rentals table)
  * comments

### comments
   * id (Primary key)
   * post_id (Foreign key referencing posts table)
   * rental_property_id (Foreign key referencing rentals table)
   * user_id(references users(id))
   * time

### ratings
   * id (Primary key)
    * user_id (Foreign key referencing users table)
    * rental_id (Foreign key referencing rentals table)
    * landlord_strictness
    * quality_of_rooms
    * size_of_rooms
    * security_of_area_and_residence
    * rental_price relative to quality of room

Each table includes fields that are appropriate for storing information specific to that table:


*users*: includes fields for storing user account information such as username, email and password.

*rentals*: includes fields for storing information about available rentals such as images, location_address, and number_of_rooms.

*posts*: includes fields for linking rental properties to a specific post, and for storing comments about those rental properties.

*comments*: includes fields for linking comments to a specific rental property.

*ratings*: includes fields for storing rating information about a rental property and linking that information to both users and rentals table where a user can rate a rental once, rentals have many ratings and users can rate multiple rentals only once.

The database also includes primary keys and foreign keys to maintain referential integrity, and to ensure that each row in the database has a unique identifier and that it can be related to other rows in other tables.

This is a general idea of how a database schema could be designed to support the rental application, the final decision on the exact database design would depend on the specific requirements and constraints of your application. And it would be a good idea to test and monitor the database performance as the number of users and rentals increase to ensure the application scales well.


#   Maps
   (https://dev.virtualearth.net/REST/v1/Imagery/Map/imagerySet?pushpin={pushpin_1}&pushpin={pushpin_2}&pushpin={pushpin_n}&mapLayer={mapLayer}&format={format}&mapMetadata={mapMetadata}&key={BingMapsKey})
   The Bing Maps Imagery API allows developers to access a variety of map imagery and metadata for use in their applications.

The URL includes several query parameters that can be used to customize the request:

*   imagerySet: specifies the type of imagery to be returned (e.g. "Aerial", "Road")
*   pushpin: specifies one or more locations on the map to be marked with a pushpin. The pushpin_1, pushpin_2, and pushpin_n are placeholders for the actual locations, which should be specified in latitude and longitude.
*   mapLayer: specifies any additional layers to be included on the map (e.g. "TrafficFlow")
*   format: specifies the format of the image to be returned (e.g. "png", "jpeg")
*   mapMetadata: specifies if metadata such as image dimensions, copyright, and image date should be included in the response
*   key: a Bing Maps API key that is required for authentication and usage tracking.
This API can be used to retrieve map imagery for different purposes like:

*   Showing an aerial or road view of an area in an application
*   Displaying a pushpin on a location in a map
*   Displaying additional layers like Traffic Flow on a map
*   Retrieving metadata such as copyright information and image date.
To use this API, developers will need to obtain a Bing Maps API key and provide it in the key parameter of the URL.
