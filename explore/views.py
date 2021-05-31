import json
import seaborn as sns
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Props
from django.db.models import Q

# Some globals
labels = {"mwkda" : "protein size (kDa)",
          "ncd1000" : "net charge density x 1000 (eÅ-2)",
          "fCharged" : "charged residues fraction",
          "NetCh" : "net charge",
          "SASAmiller" : "solvent accessible surface area (Miller)",
          "fFatty" : "fraction hydrophobic",
          "GC" : "G+C content %",
          "fPos" : "fraction positive",
          "fNeg" : "fraction negative",
          "seqnum" : "protein count"
          }
palette = sns.color_palette('tab10', 10).as_hex()


def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request, "explore/home.html")
    else:
        return render(request, "explore/login.html")



# Serve data
def take_subset(request):
    """Interpret POST query and retrieve data from DB"""
    if request.method != "POST":
        return JsonResponse({"message" : 'POST method required'}, status = 403)

    else:
        # extract info from request
        data = json.loads(request.body)
        varx = data['varx']
        vary = data['vary']
        pos = int(data['pos'])
        rank = data['rank']
        value = data['value']
        if rank == "kingdom" and value == "all":
            # null query to start chart
            matches  = [item.serialize() for item in Props.objects.all()]
            color = "lightgray"
        else:
            # make query to DB
            myFilter = {rank : value}
            matches  = [item.serialize() for item in Props.objects.filter(**myFilter).all()]
            # choose a color
            color = palette[pos]

        # format a dataset for chart.js
        dataset = {
                    "data" : [{"x" : item[varx], "y" : item[vary]} for item in matches],
                    "label" : f"{value} (N = {len(matches)})",
                    "pointBorderColor" : "white",
                    "order" : 20 - pos,
                    "backgroundColor" : color,
                    "borderColor" : "white",
                    # extra fields - not for chart.js
                    "rank" : rank,
                    "value" : value,
                  }
        response = {
                    "dataset" : dataset,
                    "axislabels" : {"x" : labels[varx], "y" : labels[vary]},
                   }

        return JsonResponse(response, status = 200)



def find_options(request):
    ranks = ["kingdom", "phylum", "taxClass", "order", "family", "genus", "species"]
    if request.method != "POST":
        return JsonResponse({"message" : 'POST method required'}, status = 403)
    else:
        data  = json.loads(request.body)
        rank  = data['rank']
        value = data['value']
        myFilter = {rank : value}
        lowerRank = ranks[ranks.index(rank) + 1]
        options = set([item.serialize()[lowerRank] for item in Props.objects.filter(**myFilter)])
        if None in options:
            options.remove(None)

        counts = [len( Props.objects.filter(**{lowerRank : option}) ) for option in options]

        response = [{"name" : option, "count" : count} for option, count in zip(options, counts)]

        response = sorted(response, key = lambda item: item["count"], reverse = True)

        return JsonResponse(response, safe = False, status = 200)


def taxa_search(request):
    ranks = ["phylum", "taxClass", "order", "family", "genus", "species"]
    query = request.GET.get("q")
    p = Props.objects.all()
    allOps = []
    for rank in ranks:
        myFilter = {rank + "__icontains" : query}
        matches = p.filter(**myFilter)
        for match in matches:
            value = match.serialize()[rank]
            kingdom = match.serialize()["kingdom"]
            allOps.append((rank , value, kingdom))

        uniqueOps = list(set(allOps))
        uniqueOpsJson = [{"rank" : r, "value" : v, "kingdom" : k} for r, v, k in uniqueOps]

    return JsonResponse(uniqueOpsJson[:10], safe=False, status = 200)


############################## Authentication ##################################

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "explore/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "explore/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# def register(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         email = request.POST["email"]
#
#         # Ensure password matches confirmation
#         password = request.POST["password"]
#         confirmation = request.POST["confirmation"]
#         if password != confirmation:
#             return render(request, "network/register.html", {
#                 "message": "Passwords must match."
#             })
#
#         # Attempt to create new user and corresponding profile
#         try:
#             user = User.objects.create_user(username, email, password)
#             user.save()
#             profile = Profile(user = user)
#             profile.save()
#         except IntegrityError:
#             return render(request, "network/register.html", {
#                 "message": "Username already taken."
#             })
#         login(request, user)
#         return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "network/register.html")
