import octofitterpy as octo

astrom_like = octo.PlanetRelAstromLikelihood(
    # MJD
    epoch = [50000,50120,50240,50360,50480,50600,50720,50840],
    # delta RA, milliarcseconds (East is positive)
    ra = [-505.7,-502.5,-498.2,-492.6,-485.9,-478.1,-469.0,-458.8],
    # delta DEC, milliarcseconds (North is positive)
    dec = [-66.9,-37.4,-7.9,21.6,51.1,80.5,109.7,138.6],
    # Uncertainty on RA, milliarcseconds
    σ_ra = [10,10,10,10,10,10,10,10.0],
    # Uncertainty on DEC, milliarcseconds
	σ_dec = [10,10,10,10,10,10,10,10],
    # Corelation between RA and DEC uncertainties
	cor= [0,0,0,0,0,0,0,0.0]
)

# You can also use separation (milliarcseconds) and position angle (RADIANS):
# astrom_like = octo.PlanetRelAstromLikelihood(
#     # MJD
#     epoch = [50000,50120],
#     # separation from star, milliarcseconds (East is positive)
#     sep = [505.7,600.1],
#     # position angle, RADIANS (!!) (NOT DEGREES)
#     pa = [0.0,0.4,],
#     # Uncertainty on sep, milliarcseconds
#     σ_sep = [10,10],
#     # Uncertainty on pa, RADIANS
# 	  σ_pa = [0.01,0.01],
#     # Corelation between PA and SEP uncertainties
#     cor= [0,0.2]
# )

# To convert dates:
#  *  octo.mjd("2020-01-01") -> to MJD
#  *  octo.years2mjd("2020.0") -> to MJD
#  *  octo.mjd2date(50000) -> datetime.date(1995, 10, 10)

b = octo.Planet(
    name="b",
    basis="Visual{KepOrbit}",
    priors=
    """            
        a ~ LogUniform(0.1, 500)
        e ~ Uniform(0.0, 0.99)
        i ~ Sine()
        ω ~ UniformCircular()
        Ω ~ UniformCircular()
        θ ~ UniformCircular()
        tp = θ_at_epoch_to_tperi(system,b,50000) # use MJD epoch of your data here!!
    """,
    likelihoods=[astrom_like]
)

# The name of your system determines the output file names
sys = octo.System(
    name="HIP100123",
    priors = 
    """
        M ~ truncated(Normal(1.2, 0.1), lower=0)
        plx ~ truncated(Normal(50.0, 0.02), lower=0)
    """,
    likelihoods=[],
    companions=[b]
)

model = octo.LogDensityModel(sys)

# defaults: adaptation=1000, iterations=1000. Increase both for more points.
chain = octo.octofit(model)

## Summary
summary = repr(chain)
print(summary)

## Plotting
octo.octoplot(model,chain)
octo.octocorner(model,chain,small=True)

## Saving (use octo.loadchain to restore)
octo.savechain("mychain.fits", chain)