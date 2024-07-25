from octofitterpy import Octofitter
from octofitterpy import jl
from .julia_helpers import jl_array
import sys

# Inside Planet and System blocks, which are resolved in the Main module,
# we need various names available to the user
jl.seval("using Octofitter, Distributions, OctofitterRadialVelocity")

gaia_plx = Octofitter.gaia_plx
HGCALikelihood = Octofitter.HGCALikelihood
HipparcosIADLikelihood = Octofitter.HipparcosIADLikelihood
LogDensityModel = Octofitter.LogDensityModel
octofit = Octofitter.octofit
octoquick = Octofitter.octoquick
loadchain = Octofitter.loadchain
savechain = Octofitter.savechain
mjd = Octofitter.mjd
mjd2date = Octofitter.mjd2date
years2mjd = Octofitter.years2mjd
projectpositions = Octofitter.projectpositions
pointwise_like = Octofitter.pointwise_like
KDEDist = Octofitter.KDEDist

loadhdf5 = Octofitter.loadhdf5
savehdf5 = Octofitter.savehdf5
Whereistheplanet_astrom = Octofitter.Whereistheplanet_astrom
ObsPriorAstromONeil2019 = Octofitter.ObsPriorAstromONeil2019

# Expose some libraries to the user
Distributions = jl.Distributions

def Planet(
    name,
    basis,
    priors,
    likelihoods=[]
):
    try:
        len(likelihoods)
    except:
        raise ValueError("likelihoods must be a list of likelihood objects (even if you are only providing one value)")
    jl.Main._obs = tuple(likelihoods)
    expr = f"""
        @planet {name} {basis} begin
            {priors}
        end (_obs...)
    """
    planet = jl.seval(expr)
    return planet

def System(
    name,
    priors,
    likelihoods=[],
    companions=[],
):
    try:
        len(likelihoods)
    except:
        raise ValueError("likelihoods must be a list of likelihood objects (even if you are only providing one value)")
    try:
        len(companions)
    except:
        raise ValueError("companions must be a list of Planet objects (even if you are only providing one value)")
    jl.Main._obs = tuple(likelihoods)
    jl.Main._plnt = tuple(companions)
    expr = f"""
        @system {name} begin
            {priors}
        end (_obs...) (_plnt...)
    """
    # _plnt
    sys = jl.seval(expr)
    return sys

def PlanetRelAstromLikelihood(**data):
    for k,v in data.items():
        data[k] = jl_array(v)
    return Octofitter.PlanetRelAstromLikelihood(Octofitter.Table(**data))

def PlanetRelativeRVLikelihood(**data):
    for k,v in data.items():
        data[k] = jl_array(v)
    return jl.OctofitterRadialVelocity.PlanetRelativeRVLikelihood(Octofitter.Table(**data))

def StarAbsoluteRVLikelihood(**data):
    for k,v in data.items():
        data[k] = jl_array(v)
    return jl.OctofitterRadialVelocity.StarAbsoluteRVLikelihood(Octofitter.Table(**data))

def PhotometryLikelihood(**data):
    for k,v in data.items():
        data[k] = jl_array(v)
    return Octofitter.PhotometryLikelihood(Octofitter.Table(**data))

# These functions require us to load a plotting backend, which is a little
# slow. Only load it when we need it.
def octoplot(*args, **kwargs):
    jl.seval("using CairoMakie: Makie")
    fig = Octofitter.octoplot(*args, **kwargs)
    if isipynb():
        fname = jl.tempname()+".png"
        jl.Main.Makie.save(fname, fig)
        from IPython.display import Image
        return Image(filename=fname) 

# These functions require us to load a plotting backend, which is a little
# slow. Only load it when we need it.
def rvpostplot(*args, **kwargs):
    jl.seval("using CairoMakie: Makie")
    fig = Octofitter.rvpostplot(*args, **kwargs)
    if isipynb():
        fname = jl.tempname()+".png"
        jl.Main.Makie.save(fname, fig)
        from IPython.display import Image
        return Image(filename=fname) 

def octocorner(*args, **kwargs):
    jl.seval("using CairoMakie: Makie")
    jl.seval("using PairPlots")
    fig = Octofitter.octocorner(*args, **kwargs)
    if isipynb():
        fname = jl.tempname()+".png"
        jl.Main.Makie.save(fname, fig)
        from IPython.display import Image
        return Image(filename=fname) 

def octofit_pigeons(*args, **kwargs):
    jl.seval("using Pigeons")
    return Octofitter.octofit_pigeons(*args, **kwargs)

def increment_n_chains(pt, extra_rounds):
    jl.seval("using Pigeons")
    return jl.Pigeons.increment_n_rounds_b(pt, extra_rounds)


def isipynb():
    try:
        get_ipython = sys.modules["IPython"].get_ipython
        if "IPKernelApp" not in get_ipython().config:
            raise ImportError("console")
        return True
    except Exception:
        return False