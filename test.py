from fasthtml.common import *
from monsterui.all import *
import random

# Using the "slate" theme with Highlight.js enabled
hdrs = Theme.slate.headers(highlightjs=True)
app, rt = fast_app(hdrs=hdrs)

################################
### Example Data and Content ###
################################
trips = [
    {"name": "Beach Getaway", "price": "$499", "category": "Beach"},
    {"name": "Mountain Hiking", "price": "$599", "category": "Adventure"},
    {"name": "City Tour", "price": "$399", "category": "Urban"},
    {"name": "Safari Expedition", "price": "$999", "category": "Wildlife"},
    {"name": "Cruise Trip", "price": "$1299", "category": "Luxury"},
    {"name": "Skiing Adventure", "price": "$799", "category": "Winter Sports"},
    {"name": "Desert Safari", "price": "$699", "category": "Adventure"},
    {"name": "Island Hopping", "price": "$899", "category": "Beach"},
    {"name": "Cultural Immersion", "price": "$499", "category": "Culture"},
    {"name": "Road Trip", "price": "$299", "category": "Budget"},
    {"name": "Road Trip", "price": "$299", "category": "Awit"},
]

CATEGORIES = sorted(set(t["category"] for t in trips))
ITEMS_PER_PAGE = 10

def TripCard(t, img_id=1):
    return Card(
        PicSumImg(w=500, height=100, id=img_id),
        DivFullySpaced(
            H4(t["name"]),
            P(Strong(t["price"], cls=TextT.sm)),
            P(Em(t["category"], cls=TextT.xs, style="color: gray; font-weight: bold;"))  # Category indicator
        ),
        Button("Details", cls=(ButtonT.primary, "w-full"))
    )

################################
### Navigation ###
################################

scrollspy_links = (
    A("Explore", href="/"),
    A("Booking", href="/booking"),
    A("Profile", href="/profile"),
    Button("Logout",    cls=ButtonT.destructive)
)

def category_tabs(active_category):
    return TabContainer(
        *[
            Li(
                A(
                    cat, 
                    href=f"/?category={cat}", 
                    cls=('uk-active uk-text-bold uk-text-primary' if cat == active_category else 'uk-text-muted'),
                    style="border-bottom: 2px solid black;" if cat == active_category else ""
                )
            ) 
            for cat in CATEGORIES
        ]
    )


################################
### Simplified Pagination Controls ###
################################

def pagination_controls(page, total_pages, category):
    """Generates simple and clean pagination controls."""
    return DivCentered(
        Div(
            A("← Prev", href=f"/?page={page - 1}&category={category}" if page > 1 else "#", cls=ButtonT.primary if page > 1 else "uk-disabled"),
            Span(f" Page {page} of {total_pages} ", cls="uk-text-bold uk-margin-small"),
            A("Next →", href=f"/?page={page + 1}&category={category}" if page < total_pages else "#", cls=ButtonT.primary if page < total_pages else "uk-disabled"),
            cls="uk-flex uk-flex-center uk-gap-small uk-margin-large"
        )
    )

################################
### Explore Page ###
################################

@rt
def index(page: int = 1, category: str = ""):
    """ Explore Page with Pagination """
    filtered_trips = [t for t in trips if category == "" or t["category"] == category]
    total_pages = (len(filtered_trips) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    paginated_trips = filtered_trips[start_idx:end_idx]

    return Container(
        NavBar(
            *scrollspy_links,
            brand=DivLAligned(H3("Trip Explorer"), UkIcon('map', height=30, width=30)),
            sticky=True, uk_scrollspy_nav=True,
            scrollspy_cls=ScrollspyT.bold
        ),
        Container(
            DivCentered(
                H1("Discover Amazing Trips!"), 
                Subtitle("Explore various trips with pagination."), 
                id="welcome-section"
            ),
            category_tabs(category),
            Section(
                H2(f"Trips in {category}" if category else "All Trips"),  # Dynamic title based on category
                Grid(*[TripCard(t, img_id=i) for i, t in enumerate(paginated_trips)], cols_lg=2),
                pagination_controls(page, total_pages, category),
                id="trips-section"
            ),
            cls=(ContainerT.xl, 'uk-container-expand')
        )
    )

################################
### Booking Page ###
################################
# Dummy data for user bookings
def get_user_bookings():
    return [
        {"id": 1, "title": "Beach Adventure", "description": "A relaxing beach trip.", "date": "2025-04-10", "tags": ["Beach", "Relaxing", "Sunset"], "price": "$499"},
        {"id": 2, "title": "Mountain Hike", "description": "A thrilling hike up the mountains.", "date": "2025-05-15", "tags": ["Hiking", "Adventure", "Nature"], "price": "$599"}
    ]

def Tags(cats): return DivLAligned(map(Label, cats))

@rt("/booking")
def booking():
    """ Booking Page """
    bookings = get_user_bookings()  # Fetch user bookings from dummy data
    
    booking_cards = [
        Card(
            DivLAligned(
                A(Img(src="https://picsum.photos/200/200?random={}".format(booking["id"]), style="width:200px"), href="#"),
                Div(cls='space-y-3 uk-width-expand')(
                    H4(booking["title"]),
                    P(booking["description"]),
                    P(Strong(booking["price"], cls=TextT.sm)),
                    DivFullySpaced(map(Small, ["Traveler", booking['date']]), cls=TextT.muted),
                    DivFullySpaced(
                        Tags(booking["tags"]),
                        Button("View Details", cls=(ButtonT.primary, 'h-6'), on_click=f"/booking/{booking['id']}")
                    )
                )
            ),
            cls=CardT.hover
        )
        for booking in bookings
    ]
    
    return Container(
        NavBar(
            A("Explore", href="/"),
            A("Booking", href="/booking"),
            A("Profile", href="/profile"),
            Button("Logout",    cls=ButtonT.destructive)
        ),
        DivCentered(H1("Booking Page"), P("Here you can manage your trip bookings.")),
        Div(*booking_cards)  # Display booking cards
    )



################################
### Profile Page ###
################################

@rt("/profile")
def profile():
    """ Profile Page """
    sidebar = NavContainer(
        Li(A("Profile")),
        uk_switcher="connect: #component-nav; animation: uk-animation-fade",
        cls=(NavT.secondary, "space-y-4 p-4 w-1/5"))

    def FormSectionDiv(*c, cls='space-y-2', **kwargs): return Div(*c, cls=cls, **kwargs)

    def FormLayout(title, subtitle, *content, cls='space-y-3 mt-4'):
        return Container(Div(H3(title), Subtitle(subtitle, cls="text-primary"), DividerLine(), Form(*content, cls=cls)))

    def profile_form():
        content = (
            FormSectionDiv(
                LabelInput("Username", placeholder='sveltecult', id='username'),
                P("This is your public display name. You can change it once every 30 days.", cls="text-primary")),
            FormSectionDiv(
                LabelTextArea("Bio", id="bio", placeholder="Tell us about yourself"),
                P("You can @mention other users and organizations.", cls="text-primary")),
            FormSectionDiv(
                FormLabel("URLs"),
                P("Add links to your website or social media profiles.", cls="text-primary"),
                Input(value="https://example.com"),
                Button("Add URL")),
            Button('Update profile', cls=ButtonT.primary))
        
        return FormLayout('Profile', 'This is how others will see you.', *content)

    return Container(
        NavBar(
            A("Explore", href="/"),
            A("Booking", href="/booking"),
            A("Profile", href="/profile"),
            Button("Logout",    cls=ButtonT.destructive)
        ),
        Div(cls="flex gap-x-12")(
            sidebar,
            Ul(id="component-nav", cls="uk-switcher max-w-2xl")(
                Li(cls="uk-active")(profile_form())
            )
        )
    )

# Run the app
serve()
