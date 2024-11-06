# Basic Orbit Fitting Example

This example demonstrates how to fit a Keplerian orbit to relative astrometry data using octofitterpy.

```python
import octofitterpy as octo
import numpy as np

# Create relative astrometry data
astrom_like = octo.PlanetRelAstromLikelihood(
    # MJD dates of observations
    epoch = [50000, 50120, 50240, 50360, 50480, 50600, 50720, 50840],
    # Delta RA in milliarcseconds (East is positive)  
    ra = [-505.7, -502.5, -498.2, -492.6, -485.9, -478.1, -469.0, -458.8],
    # Delta Dec in milliarcseconds (North is positive)
    dec = [-66.9, -37.4, -7.9, 21.6, 51.1, 80.5, 109.7, 138.6],
    # Uncertainties in milliarcseconds
    σ_ra = [10.0] * 8,
    σ_dec = [10.0] * 8,
    # Correlation between RA/Dec uncertainties
    cor = [0.0] * 8 
)

# Define planet model
planet_b = octo.Planet(
    name="b",
    basis="Visual{KepOrbit}",
    priors="""
        a ~ LogUniform(0.1, 500)      # Semi-major axis (AU)
        e ~ Uniform(0.0, 0.5)         # Eccentricity  
        i ~ Sine()                    # Inclination (radians)
        ω ~ UniformCircular()         # Argument of periastron (radians)
        Ω ~ UniformCircular()         # Longitude of ascending node (radians)
        θ ~ UniformCircular()         # Mean anomaly reference angle
        tp = θ_at_epoch_to_tperi(system,b,50000)  # Time of periastron passage
    """,
    likelihoods=[astrom_like]
)

# Define system model
system = octo.System(
    name="Example",
    priors="""
        M ~ truncated(Normal(1.2, 0.1), lower=0.1)  # Total mass (solar masses)
        plx ~ truncated(Normal(50.0, 0.02), lower=0.1)  # Parallax (mas)
    """,
    likelihoods=[],
    companions=[planet_b]
)

# Create model and sample from posterior
model = octo.LogDensityModel(system)
chain = octo.octofit(model)

# Plot results
octo.octoplot(model, chain) # saves it to a file
octo.octocorner(model, chain, small=True) # saves it to a file

# Save chain
octo.savechain("example_chain.fits", chain)
```

This example shows:
1. Creating a relative astrometry likelihood object
2. Defining a planet model with Keplerian orbital elements
3. Creating a system model with stellar parameters
4. Sampling from the posterior using Hamiltonian Monte Carlo
5. Visualizing and saving the results

The priors are specified using "Distribution" objects. Some available distributions include:
- `Uniform(min, max)`
- `LogUniform(min, max)` 
- `Normal(mean, std)`
- `truncated(dist, lower=val)`
- `Sine()` 
- `UniformCircular()`

Dates can be provided in Modified Julian Date (MJD) format, or converted using:
```python
mjd = octo.mjd("2020-01-01")
mjd = octo.years2mjd(2020.0)
date = octo.mjd2date(58849)
```
