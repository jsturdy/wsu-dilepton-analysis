import ROOT as r

# keep a pointer to the original TCanvas constructor
caninit = r.TCanvas.__init__

# define a new TCanvas class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentCanvas(r.TCanvas):
  def __init__(self, *args):
    caninit(self,*args)
    r.SetOwnership(self,False)

# replace the old TCanvas class by the new one
r.TCanvas = GarbageCollectionResistentCanvas

# keep a pointer to the original TPad constructor
padinit = r.TPad.__init__

# define a new TPad class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentCanvas(r.TPad):
  def __init__(self, *args):
    padinit(self,*args)
    r.SetOwnership(self,False)

# replace the old TPad class by the new one
r.TPad = GarbageCollectionResistentCanvas

# keep a pointer to the original TH1D constructor
th1dinit = r.TH1D.__init__

# define a new TH1D class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentH1D(r.TH1D):
  def __init__(self, *args):
    th1dinit(self,*args)
    r.SetOwnership(self,False)

# replace the old TH1D class by the new one
r.TH1D = GarbageCollectionResistentH1D

# keep a pointer to the original TLegend constructor
leginit = r.TLegend.__init__

# define a new TLegend class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentLegend(r.TLegend):
  def __init__(self, *args):
    leginit(self,*args)
    r.SetOwnership(self,False)

# replace the old TLegend class by the new one
r.TLegend = GarbageCollectionResistentLegend

# keep a pointer to the original TFile constructor
fileinit = r.TFile.__init__

# define a new TFile class (inheriting from the original one),
# setting the memory ownership in the constructor
class GarbageCollectionResistentFile(r.TFile):
  def __init__(self, *args):
    fileinit(self,*args)
    r.SetOwnership(self,False)

# replace the old TFile class by the new one
r.TFile = GarbageCollectionResistentFile

def makeNicePlot(hist,params,debug=False):
    """makeNicePlot: takes a histogram object and a set of parameters and applies the settings
    params: a map of parameters
    params keys:
        "color": color to make the line/marker
        "marker": marker to draw at each point
        "stats": options to pass to SetOptStat
        "coords": x[x1,x2] and y[y1,y2] coordinates of the stats box
    """

    if debug:
        print hist
        print params

        #color,marker,coords,stats,
    hist.SetLineWidth(2)
    hist.SetLineColor(params["color"])
    hist.SetMarkerStyle(params["marker"])
    hist.SetMarkerColor(params["color"])
    hist.SetMarkerStyle(params["marker"])
    hstat = hist.FindObject("stats")
    if debug:
        print hstat
    hstat.SetTextColor(params["color"])
    hstat.SetOptStat(params["stats"])
    if params["coords"]["x"][0] > -0.1:
        hstat.SetX1NDC(params["coords"]["x"][0])
    if params["coords"]["x"][1] > -0.1:
        hstat.SetX2NDC(params["coords"]["x"][1])
    if params["coords"]["y"][0] > -0.1:
        hstat.SetY1NDC(params["coords"]["y"][0])
    if params["coords"]["y"][1] > -0.1:
        hstat.SetY2NDC(params["coords"]["y"][1])
    return hist

def styleHistogram(hist,params,debug=False):

    hist.SetMarkerColor(params["marker"]["color"])
    hist.SetMarkerStyle(params["marker"]["style"])
    hist.SetLineColor(params["line"]["color"])
    hist.SetLineStyle(params["line"]["style"])
    hist.SetLineWidth(params["line"]["width"])

    return hist
