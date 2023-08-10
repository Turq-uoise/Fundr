# Fundr ReadMe


## Description

For our third project at General Assembly, we were asked to think of a website that could “solve” a problem. The idea we came up with attempted to resolve the so-called “death of the high street”; that being the concept that small shops on the high street are being outcompeted by large franchises.

Our idea of “Fundr” tries to remedy this by allowing small business owners to advertise their business to people in the local area in a “Tinder” style swiping app, and allow locals to fund it. This would both increase investment into that business, as well as possible foot traffic. 

## Deployment link

https://fundr.fly.dev/

Install the code (links to github), then run “python3 manage.py run” in the console, and navigate to localhost:8000.


## Timeframe & Working Team (Solo/Pair/Group)

I was working in a group with 2 other programmers, and it took around 5 days to complete.



## Technologies Used

I used Python, HTML, CSS, Django and PostgreSQL to write this program.



## Brief

I was told to create a working full-stack app that meets or exceeds the below technical requirements, built by me, and hosted online (originally Heroku, but then switched to fly.io).

Your app must:

☐ Be a full-stack Django application.

☐ Connect to and perform data operations on a PostgreSQL database (the default SQLLite3 database is not acceptable).

☐ If consuming an API (OPTIONAL), have at least one data entity (Model) in addition to the built-in User model. The related entity can be either a one-to-many (1:M) or a many-to-many (M:M) relationship.

☐ If not consuming an API, have at least two data entities (Models) in addition to the built-in User model. It is preferable to have at least one one-to-many (1:M) and one many-to-many (M:M) relationship between entities/models.

☐ Have full-CRUD data operations across any combination of the app's models (excluding the User model). For example, creating/reading/updating posts and creating/deleting comments qualifies as full-CRUD data operations.

☐ Authenticate users using Django's built-in authentication.

☐ Implement authorization by restricting access to the Creation, Updating & Deletion of data resources using the login_required decorator in the case of view functions; or, in the case of class-based views, inheriting from the LoginRequiredMixin class.

☐ Be deployed online using Heroku. Presentations must use the deployed application.

The app may optionally:

☐ Upload images to AWS S3

☐ Consume an API (installation of the Requests package will be necessary)

Other Requirements:

☐ Your team must manage team contributions and collaboration using Git/GitHub team work-flow. 

☐ All team members need to have significant contributions to the project via git commits.

A README.md file with these sections (here's a basic template):

☐ App Title: Contains a description of what the app does and optional background info.

☐ Screenshot(s): A screenshot of your app's landing page and any other screenshots of interest.

☐ Technologies Used: List of the technologies used.

☐ Getting Started: That Includes:

A link to the deployed app (Heroku)
A link to the Trello board used for the project's planning that includes user stories, wireframes & an ERD.
A link to the pitch-deck.

## Planning
### Entity Relationship Diagram

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/474b78e6-a039-4d9b-abe5-70b130db542e)

### Wireframes

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/628d7c2e-4556-48e0-abec-0359d7c280b1)
![image](https://github.com/Turq-uoise/Fundr/assets/107884520/0d9b2862-5d9d-431b-8b5d-5321d208fd52)


### Initial Brainstorming Stages

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/cc686034-3dfc-4087-8c22-8de9dccf259a)

After the initial planning stages, I put together a To Do list for our team to follow. I set up labels that the team members could use to allocate themselves to certain tasks, and tried to keep everyone on top of updating their labels using Slack and Zoom, with daily standups and code-alongs.

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/0e9a0e4d-7d15-4efe-bcf9-6e69e809b218)

I was given the initial Home Page, the Explore Page and the Following Page, as well as the overall routing for the website. The others mostly focused on the design and polish, such as sorting the Fundrs on the explore page by distance, “lazy loading” the home page, and managing the desktop vs mobile templates.


## Build/Code Process

The first thing I worked on was the explore page. The base.html page was completed, so I needed to build on it to create the primary “swiping” functionality for our website. To be able to do this on a single page without reloading, I had to use some JavaScript on top of my Python and HTML. The HTML displays the information from a Fundr in a simple card that is sent as an array using Python. 

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/617e62f7-4d7d-411b-a358-184e3427cfd9)

However, iterating through the array was done using JavaScript, as HTML cannot update itself, and Python cannot update the HTML without reloading the page. The Python array was parsed as JSON so that the JavaScript could access each field, and then the JavaScript uses those fields to populate the various HTML components. It also stores the index of the current Fundr in the array, so that the Python can then use it to “Save” a Fundr.

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/5c754116-44e3-45ff-afa2-204a4ad7c9bf)
![image](https://github.com/Turq-uoise/Fundr/assets/107884520/e261a4a2-3004-45ec-bc65-fa8ad31f905e)


If the “Save” button is clicked, the index is sent to the Python code, instead of being handled by the JavaScript. This is because there’s no way to update the models without reloading the page, so the best approximation is to send the array of Fundrs as normal, but start at the point of the array that matches the current index.

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/fb5f2fc7-0946-4785-bdd0-d946fef799e3)

That is, if an index of “2” is sent back by the JavaScript (because the user has tried to save the third Fundr), the Python saves that Fundr, reloads the page, and starts the newly sent array at the index of “2”. Therefore, even though pressing the “Save” button reloads the page, it saves the place of the user so they have a more seamless experience.

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/64246d24-74dd-4933-8701-dc9759026235)

After completing this, I was ready to work on the Following and Home pages. The Home page displays each “Post” from every Fundr that you’ve saved in a fairly straightforward way. 

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/69b186ba-cbfc-4ba2-b0d3-24a6ed869b1d)
![image](https://github.com/Turq-uoise/Fundr/assets/107884520/23d73bd3-f76a-4c19-8f33-715099e4219c)



The Python code gets all of the Fundrs that are being followed by the user, and then gets all the posts within those Fundrs, and then sends them to the HTML. The following page is similarly simple.

![image](https://github.com/Turq-uoise/Fundr/assets/107884520/62ee14ac-0481-463c-b035-27d93cc9e677)
![image](https://github.com/Turq-uoise/Fundr/assets/107884520/d44bb51e-3333-46fd-8e29-efa413878831)
![image](https://github.com/Turq-uoise/Fundr/assets/107884520/2f119d0b-3621-463c-beea-b67374a01d71)

## Challenges

The initial idea was based off of “Tinder”, which has a seamless, reactive swiping component. Replicating this with Python and Django proved difficult, and completing it entirely without reloading ended up being impossible, but I feel that I ended up with as seamless an experience as I could have gotten when trying to replicate this behaviour. Mixing the use of Python and JavaScript caused some issues, but using various different methods of JSON parsing, I ended up being able to use Python arrays within JavaScript. 

The CSS and HTML was also quite challenging, in particular when trying to switch between mobile and desktop views. We ended up using a non-responsive solution, which checks to see what device the user is on, and then renders that base template, rather than reacting to the screen size changing. This appears to work most times, but is a fairly inelegant solution, especially because it lead us to neglect responsiveness on the desktop view entirely.


## Wins

I was told that there was no way I would be able to have the Tinder “swiping” feature seamlessly, and while that ended up being true (saving a Fundr without reloading was impossible with this stack as far as I can tell), I ended up with a close to seamless experience, without having to provide extra packages/libraries.

## Key Learnings/Takeaways

- Planning for a more responsive view from the start is difficult and requires more care. The team and I did plan for it, but due to being somewhat unfamiliar with Python/Django, we ended up having a lot of trouble. 
- Using Trello is incredibly powerful when working in a team, and even when working on your own. Trello in particular is something I will likely use going forward.
- I have always known that Github/Git is powerful, but using it in a team with branches and merges showed me just how useful it can be, but also how carefully it needs to be used. Our team didn’t run into too many merge conflicts as we were usually working on entirely separate files, but the few that we did run into were valuable lessons.
- Having a strong vision for a project (in this case, the Tinder Swiping) can lead to finding new ways of solving things, and can provide motivation when you run into walls.

## Bugs
The Fundr cards on the Explore page are different sizes depending on the length of the text; it would look nicer for the cards to be the same size no matter what (either truncating long text, or sizing it according to the maximum possible size of the text). Other “bugs” are visual and are more a sign of necessary improvement rather than mistakes.

## Future Improvement
- As shown on the Trello, there were a few stretch goals that we wanted to reach if we were ever to continue on this project.
- Pledging to a Fundr: For a fundraising website, it’s strange not to have the ability to at least pledge to a Fundr (even if we don’t implement actual payment)
- Commenting on Fundrs: It would be nice to have comments/ratings for Fundrs once people save them, so that people can, for example, spot scams.
- Sorting Fundrs by user: Going to a user’s page and viewing their Fundrs/Comments could be useful, and could help foster a community.
- Google maps: After saving a Fundr, having either a link to the location on google maps, or an embedded map could be quite nice.





