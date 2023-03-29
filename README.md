# RCMP
A recipe catalogue and meal planner application with a variety of functions. The name is a WIP! Suggestions Welcome :)

## Description
This program is built for all the lazy people out there, like me, who find meal planning and thinking of what to eat to be mundane tasks. But why stop there? In addition to determining what meals to eat for the week, RCMP will automatically determine shopping days according to what is out of stock, or if a key item is out of stock. A preferred shopping day can also be set. In order to choose random meals each week, RCMP has the ability to store and extract recipe information from your favorite cooking blog/website; all you need is the url. RCMP is meant to be a highly customizable application, including, but not limited to: recipe serving adjustments, how many/type of meals chosen per week, recipe ingredients, and more. If you would like to see a particular feature customizable, let us know! 

In addition to recipes and shopping, we have plans to include a "social media" aspect where you can share favorite recipes, recipe alterations, ideas, nice food photos, and more! Depending on feasability, you would also be able to see what recipes are trending, and even suggestions for recipes based on past viewed, time of the year (holidays and traditions), or what friends are eating. Lastly, we plan to implement a calender system to make scheduling easier to view and potentially link to google calender for easier viewing and daily workflow integration.

This code is the backend functioning spaghetti to the website: 

Lastly, I am a relatively new coder (started in January 2022) so ANY and ALL critiques and suggestions are welcome. If you see anything in how my code is coded or organized, or even aspects of this README that can be better, please reach out! I am always looking to learn more about coding and the proper procedures and etiquette of programming and software development.

## Sections and Features
### Kitchen Inventory
* Create blank or templated inventory of kitchen items
* Can mark key items that necessitate a shopping trip when empty
* Can upload existing inventory from CSV file
* For meats, can choose a "meat of the month/week" or some specified period
    * All possible meat options will be listed in inventory, but only selected one(s) will be "active"

### Shopping List
* Autopopulates out of stock items according to kitchen inventory
* Can manually add to list

### Meal Randomizer
* Randomly chooses a specified numbers of meals per week or specified period. The default is set to 3 meals per week.
* Can choose to "cross off" meals that have been chosen, and reset crossed off items after a specified period of time (e.g. every month)
* Can include "leftovers" and "eating out" as optional attributes (e.g. in addition to 3 meals per week, 3 days are for leftovers, and 1 day is for eating out.)
* Can decrease randomization for specification
    * Customize randomization to pull for specific category(s) (e.g. all meals pulled from one category, or 2 from one category and 1 from another, etc)

### Recipe Archive
* Automatically extract recipe name, info, ingredients, and instructions via url
* Add/modify recipes manually

### Calendar System
* Allows easier viewing of scheduled shopping days or meal schedule
* Can customize when to generate shopping trip
    * e.g. create shopping trip after x% of inventory (or specific categories) are out of stock
    * set a preferred day(s) and time for shopping scheduling
* Link to google calender for workflow integration

### Restaurant Randomization
* Same as meal randomization but with restaurants


## Help

## Authors
Contributors names and contact info:

Therry Malone - therrymalone@gmail.com

## Version History

* pre-release

## License

This project is licensed under the GPL-3.0 License - see the LICENSE.md file for details
