import json
import seaborn as sns
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import Props

# Some globals
labels = {
              "mwkda": "protein size (kDa)",
              "ncd1000": "net charge density x 1000 (eÅ-2)",
              "fCharged": "charged residues fraction",
              "NetCh": "net charge",
              "SASAmiller": "solvent accessible surface area (Miller)",
              "fFatty": "fraction hydrophobic",
              "GC": "G+C content %",
              "fPos": "fraction positive",
              "fNeg": "fraction negative",
              "seqnum": "protein count"
        }
RANKS = ["kingdom","phylum", "taxClass","order","family","genus","species"]
palette = sns.color_palette('tab10', 10).as_hex()


def index(request):
    """
    Load the main page.
    """
    return render(request, "explore/home.html")


def take_subset(request):
    """
    Interpret POST query, retrieve data from DB and serve.
    """
    if request.method != "POST":
        return JsonResponse({"message" : 'POST method required'}, status = 403)
    else:
        # extract info from request
        data = json.loads(request.body)
        varx = data['varx']
        vary = data['vary']
        idx = int(data['idx'])
        rank = data['rank']
        value = data['value']
        myFilter = {"dataset": data["origin"]}
        if rank == "kingdom" and value == "all":
            # null query to start chart
            color = "lightgray"
        else:
            # make query to DB
            myFilter.update({rank : value})
            color = palette[idx]

        matches = [item.serialize()
                   for item in Props.objects.filter(**myFilter).all()
                ]
        # format a dataset for chart.js
        dataset = {
                    "data": [  {"x" : item[varx], "y" : item[vary]}
                                for item in matches
                            ],
                    "label": f"{value} (N = {len(matches)})",
                    "pointBorderColor": "white",
                    "order": 20 - idx,
                    "backgroundColor": color,
                    "borderColor": "white",
                    # extra fields - not for chart.js
                    "rank": rank,
                    "value": value,
                    "idx": idx,
                  }
        response = {
                    "dataset": dataset,
                    "axislabels": {"x": labels[varx], "y": labels[vary]},
                   }
        return JsonResponse(response, status = 200)



def find_options(request):
    """
    Serve options for lineage tables upon value change.
    """
    if request.method != "POST":
        return JsonResponse({"message" : 'POST method required'}, status = 403)

    data  = json.loads(request.body)
    rank  = data['rank']
    value = data['value']
    myFilter = {rank: value}
    lowerRank = RANKS[RANKS.index(rank) + 1]
    options = set([
                    item.serialize()[lowerRank]
                    for item in Props.objects.filter(**myFilter)
                ])

    if None in options:
        options.remove(None)

    counts = [
                len( Props.objects.filter(**{lowerRank : option}) )
                for option in options
            ]
    response = [
                {"name" : option, "count" : count}
                for option, count in zip(options, counts)
            ]
    response = sorted(  response,
                        key = lambda item: item["count"],
                        reverse = True
                    )
    return JsonResponse(response, safe = False, status = 200)


def taxa_search(request):
    """
    Serve 10 options for taxa searchbox.
    """
    ranks = RANKS.copy()
    ranks.remove("kingdom")
    query = request.GET.get("q")
    p = Props.objects.all()
    allOps = []
    for rank in ranks:
        myFilter = {rank + "__icontains": query}
        matches = p.filter(**myFilter)
        for match in matches:
            value = match.serialize()[rank]
            kingdom = match.serialize()["kingdom"]
            allOps.append((rank , value, kingdom))

    uniqueOps = list(set(allOps))
    uniqueOpsSorted = []
    for rank in ranks:
        for pair in uniqueOps:
            if pair[0] == rank:
                uniqueOpsSorted.append(pair)
    uniqueOpsJson = [
                        {"rank" : r, "value" : v, "kingdom" : k}
                        for r, v, k in uniqueOpsSorted
                    ]
    return JsonResponse(uniqueOpsJson[:10], safe=False, status = 200)
